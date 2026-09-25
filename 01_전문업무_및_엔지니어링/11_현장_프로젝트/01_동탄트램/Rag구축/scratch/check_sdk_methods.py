from google import genai
import inspect

print("GenAI Client:", hasattr(genai, "Client"))
client = genai.Client(api_key="TEST_DUMMY_KEY")
print("Files attribute:", hasattr(client, "files"))
print("Files upload signature:", inspect.signature(client.files.upload))
print("Models generate_content signature:", inspect.signature(client.models.generate_content))
