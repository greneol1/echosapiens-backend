from pathlib import Path

CORPUS_DIR = "corpus"

print("EchoSapiens Corpus Loader")
print("-------------------------")

files = Path(CORPUS_DIR).glob("*")

for file in files:
    print(f"Loaded: {file.name}")