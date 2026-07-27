import ast
import csv
from importlib import import_module
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
runtime = import_module("dongtan_runtime")


class RuntimeConfigTests(unittest.TestCase):
    def test_local_config_uses_safe_defaults(self):
        config = runtime.load_local_database_config({})

        self.assertEqual(config.uri, "bolt://localhost:7687")
        self.assertIsNone(config.auth)

    def test_local_config_treats_blank_uri_as_unset(self):
        config = runtime.load_local_database_config({"DONGTAN_LOCAL_URI": ""})

        self.assertEqual(config.uri, "bolt://localhost:7687")

    def test_local_config_rejects_partial_credentials(self):
        with self.assertRaisesRegex(runtime.ConfigurationError, "DONGTAN_LOCAL_PASSWORD"):
            _ = runtime.load_local_database_config({"DONGTAN_LOCAL_USER": "user"})

    def test_cloud_config_requires_every_value(self):
        with self.assertRaisesRegex(runtime.ConfigurationError, "DONGTAN_CLOUD_URI"):
            _ = runtime.load_cloud_database_config({})

    def test_cloud_config_reads_environment(self):
        config = runtime.load_cloud_database_config(
            {
                "DONGTAN_CLOUD_URI": "bolt+ssc://example.invalid:7687",
                "DONGTAN_CLOUD_USER": "user",
                "DONGTAN_CLOUD_PASSWORD": "secret",
            }
        )

        self.assertEqual(config.uri, "bolt+ssc://example.invalid:7687")
        self.assertEqual(config.auth, ("user", "secret"))

    def test_project_paths_are_project_relative(self):
        paths = runtime.load_project_paths({})

        self.assertEqual(paths.nodes_csv, PROJECT_ROOT / "00_원본_데이터" / "rfp_nodes.csv")
        self.assertEqual(
            paths.relationships_csv,
            PROJECT_ROOT / "00_원본_데이터" / "rfp_relationships.csv",
        )
        self.assertEqual(
            paths.ontology_output,
            PROJECT_ROOT / "03_보고서_및_출력" / "ontology.json",
        )

    def test_default_csv_files_match_import_contract(self):
        paths = runtime.load_project_paths({})

        self.assertTrue(paths.nodes_csv.is_file())
        self.assertTrue(paths.relationships_csv.is_file())
        with paths.nodes_csv.open(encoding="utf-8", newline="") as nodes_file:
            node_headers = next(csv.reader(nodes_file))
        with paths.relationships_csv.open(
            encoding="utf-8",
            newline="",
        ) as relationships_file:
            relationship_headers = next(csv.reader(relationships_file))

        self.assertEqual(
            node_headers,
            ["id", "label", "section", "keywords", "content", "risk_level"],
        )
        self.assertEqual(relationship_headers, ["source", "target", "type"])

    def test_project_paths_accept_environment_overrides(self):
        custom_path = PROJECT_ROOT / "custom.csv"
        paths = runtime.load_project_paths({"DONGTAN_NODES_CSV": str(custom_path)})

        self.assertEqual(paths.nodes_csv, custom_path)

    def test_python_script_runner_never_uses_a_shell(self):
        with mock.patch("dongtan_runtime.subprocess.run") as run:
            _ = runtime.run_python_script(
                PROJECT_ROOT,
                "example.py",
                "위치",
                "301 & calc.exe",
            )

        run.assert_called_once_with(
            [
                sys.executable,
                str(PROJECT_ROOT / "example.py"),
                "위치",
                "301 & calc.exe",
            ],
            check=False,
        )


class RefactorRegressionTests(unittest.TestCase):
    secret_files: tuple[str, ...] = (
        "01_로컬_도커(로도)/backup_graph.py",
        "02_클라우드_원격/cloud_graph_agent.py",
        "02_클라우드_원격/reconnect_cloud_graph.py",
        "02_클라우드_원격/upload_to_cloud.py",
        "02_클라우드_원격/make_sheets_txt.py",
        "03_보고서_및_출력/export_to_excel.py",
    )

    def test_cloud_scripts_do_not_assign_literal_credentials(self):
        credential_names = {"URI", "USER", "PASSWORD", "uri", "user", "password"}

        for relative_path in self.secret_files:
            with self.subTest(path=relative_path):
                source_path = PROJECT_ROOT / relative_path
                tree = ast.parse(source_path.read_text(encoding="utf-8"))
                assignments = (
                    node
                    for node in ast.walk(tree)
                    if isinstance(node, ast.Assign)
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                    and node.value.value
                )
                assigned_names = {
                    target.id
                    for assignment in assignments
                    for target in assignment.targets
                    if isinstance(target, ast.Name)
                }
                self.assertTrue(
                    credential_names.isdisjoint(assigned_names),
                    f"{relative_path} still assigns a literal credential",
                )

    def test_cloud_drivers_use_shared_runtime_config(self):
        for relative_path in self.secret_files:
            with self.subTest(path=relative_path):
                source_path = PROJECT_ROOT / relative_path
                tree = ast.parse(source_path.read_text(encoding="utf-8"))
                config_assignments = [
                    node
                    for node in ast.walk(tree)
                    if isinstance(node, ast.Assign)
                    and any(
                        isinstance(target, ast.Name) and target.id == "config"
                        for target in node.targets
                    )
                ]
                self.assertEqual(len(config_assignments), 1)
                config_call = config_assignments[0].value
                if not isinstance(config_call, ast.Call):
                    self.fail(f"{relative_path} config is not loaded by a function call")
                if not isinstance(config_call.func, ast.Attribute):
                    self.fail(f"{relative_path} config loader is not a runtime attribute")
                self.assertEqual(
                    ast.unparse(config_call.func),
                    "runtime.load_cloud_database_config",
                )

                driver_calls = [
                    node
                    for node in ast.walk(tree)
                    if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "driver"
                ]
                self.assertEqual(len(driver_calls), 1)
                driver_call = driver_calls[0]
                self.assertEqual(ast.unparse(driver_call.args[0]), "config.uri")
                self.assertEqual(len(driver_call.keywords), 1)
                self.assertIsNone(driver_call.keywords[0].arg)
                self.assertEqual(
                    ast.unparse(driver_call.keywords[0].value),
                    "config.driver_kwargs()",
                )

    def test_rodo_does_not_call_os_system(self):
        tree = ast.parse(
            (PROJECT_ROOT / "01_로컬_도커(로도)" / "rodo.py").read_text(
                encoding="utf-8"
            )
        )

        calls_os_system = any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
            and node.func.attr == "system"
            for node in ast.walk(tree)
        )

        self.assertFalse(calls_os_system)

    def test_help_does_not_require_database_dependencies_or_credentials(self):
        scripts = (
            PROJECT_ROOT / "01_로컬_도커(로도)" / "rodo.py",
            PROJECT_ROOT / "02_클라우드_원격" / "cloud_graph_agent.py",
        )
        clean_environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("DONGTAN_")
        }

        for script in scripts:
            with self.subTest(script=script.name):
                result = subprocess.run(
                    [sys.executable, "-S", str(script), "--help"],
                    cwd=script.parent,
                    env=clean_environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_cloud_scripts_import_from_their_own_directories(self):
        clean_environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("DONGTAN_")
        }

        for relative_path in self.secret_files:
            script = PROJECT_ROOT / relative_path
            command = (
                "import runpy; "
                f"runpy.run_path({str(script)!r}, run_name='runtime_import_test')"
            )
            with self.subTest(path=relative_path):
                result = subprocess.run(
                    [sys.executable, "-S", "-c", command],
                    cwd=script.parent,
                    env=clean_environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_cloud_agent_fails_cleanly_without_configuration(self):
        script = PROJECT_ROOT / "02_클라우드_원격" / "cloud_graph_agent.py"
        clean_environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("DONGTAN_")
        }

        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=PROJECT_ROOT,
            env=clean_environment,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("DONGTAN_CLOUD_URI", result.stderr)
        self.assertNotIn("ModuleNotFoundError", result.stderr)


if __name__ == "__main__":
    _ = unittest.main()
