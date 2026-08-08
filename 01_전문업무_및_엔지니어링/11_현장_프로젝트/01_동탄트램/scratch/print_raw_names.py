import os

def print_raw_names():
    folder = "03_보고서_및_출력"
    files = os.listdir(folder)
    with open("scratch/raw_names.txt", "w", encoding="utf-8") as out:
        out.write("Raw names in folder:\n")
        for f in files:
            fp = os.path.join(folder, f)
            out.write(f"Name: {repr(f)} | Size: {os.path.getsize(fp)} bytes\n")

if __name__ == '__main__':
    print_raw_names()
