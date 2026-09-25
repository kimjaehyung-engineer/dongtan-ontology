import importlib.util

print("google.genai:", importlib.util.find_spec("google.genai") is not None)
print("google.generativeai:", importlib.util.find_spec("google.generativeai") is not None)
