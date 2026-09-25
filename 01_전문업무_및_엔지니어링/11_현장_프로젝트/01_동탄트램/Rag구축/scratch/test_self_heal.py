import sys
import os
import subprocess

py314 = r"C:\Users\sskjh\AppData\Local\Programs\Python\Python314\python.exe"
print("Initial interpreter:", sys.executable)

try:
    from google import genai
    print("google.genai is directly importable!")
except ImportError:
    print("google.genai missing in current interpreter! Relaunching with Python 3.14...")
    if os.path.exists(py314) and sys.executable.lower() != py314.lower():
        sys.exit(subprocess.call([py314] + sys.argv))
    else:
        raise

print("Final interpreter running:", sys.executable)
