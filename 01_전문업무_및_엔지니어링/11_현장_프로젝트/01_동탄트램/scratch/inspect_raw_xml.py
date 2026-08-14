# -*- coding: utf-8 -*-
import zipfile, xml.etree.ElementTree as ET, sys, os
sys.stdout.reconfigure(encoding="utf-8")

p_xlsm = r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼 BODY (집행단계)v8.xlsm"

with zipfile.ZipFile(p_xlsm, 'r') as z:
    wb_xml = z.read("xl/workbook.xml").decode("utf-8")
    root = ET.fromstring(wb_xml)
    ns = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    
    sheet_map = {}
    for s in root.findall(".//ns:sheet", ns):
        name = s.attrib.get("name")
        r_id = s.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        sheet_map[name] = r_id
    
    print("Sheets in workbook.xml:")
    for k, v in sheet_map.items():
        print(f"  {k}: {v}")

    # Read sheet rels to find target sheet xml file
    wb_rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    root_rels = ET.fromstring(wb_rels)
    rel_map = {}
    for rel in root_rels.findall(".//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
        rel_map[rel.attrib["Id"]] = rel.attrib["Target"]

    earth_sheet_file = "xl/" + rel_map[sheet_map["사전토공사"]]
    print(f"\n사전토공사 XML 파일: {earth_sheet_file}")

    # Read 사전토공사 sheet XML
    sheet_xml = z.read(earth_sheet_file).decode("utf-8")
    sheet_root = ET.fromstring(sheet_xml)

    # Read shared strings if any
    shared_strings = []
    if "xl/sharedStrings.xml" in z.namelist():
        sst_xml = z.read("xl/sharedStrings.xml").decode("utf-8")
        sst_root = ET.fromstring(sst_xml)
        for si in sst_root.findall(".//ns:si", ns):
            t = si.find(".//ns:t", ns)
            if t is not None:
                shared_strings.append(t.text or "")
            else:
                # concatenated runs
                texts = [r_t.text or "" for r_t in si.findall(".//ns:t", ns)]
                shared_strings.append("".join(texts))

    print(f"Shared strings count: {len(shared_strings)}")

    # Check cells O2, Q2, S2 in sheet XML
    for target_cell in ["O2", "Q2", "S2", "O3", "Q3", "S3"]:
        c = sheet_root.find(f".//ns:c[@r='{target_cell}']", ns)
        if c is not None:
            t_type = c.attrib.get("t")
            v_tag = c.find("ns:v", ns)
            f_tag = c.find("ns:f", ns)
            val_text = v_tag.text if v_tag is not None else "None"
            if t_type == "s" and val_text.isdigit():
                display_val = shared_strings[int(val_text)]
            else:
                display_val = val_text
            f_text = f_tag.text if f_tag is not None else "None"
            print(f"Cell {target_cell}: type={t_type}, val='{display_val}', formula='{f_text}'")
        else:
            print(f"Cell {target_cell}: NOT FOUND in XML!")
