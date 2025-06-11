import os

REQUIRED_FILES = [
    "config.json",
    "tokenizer.json",
    "tokenizer_config.json"
]

# Accept either a single large file or shards
MODEL_FILE_PATTERNS = [
    "pytorch_model.bin",
    "pytorch_model-00001-of-00001.bin",
    "pytorch_model-00001-of-00002.bin"  # Example shard name
]

OPTIONAL_FILES = [
    "special_tokens_map.json",
    "generation_config.json"
]

MODEL_DIR = os.path.join("models", "llama-2-7b")

def check_files():
    missing = []
    present = []
    for fname in REQUIRED_FILES:
        fpath = os.path.join(MODEL_DIR, fname)
        if os.path.isfile(fpath):
            present.append(fname)
        else:
            missing.append(fname)
    # Check for at least one model file
    model_file_found = False
    for pattern in MODEL_FILE_PATTERNS:
        if any(f.startswith(pattern.split('-')[0]) for f in os.listdir(MODEL_DIR)):
            model_file_found = True
            present.append(pattern + " (or shard)")
            break
    if not model_file_found:
        missing.append("pytorch_model.bin (or shards)")
    # Optional files
    for fname in OPTIONAL_FILES:
        fpath = os.path.join(MODEL_DIR, fname)
        if os.path.isfile(fpath):
            present.append(fname + " (optional)")
    return present, missing

def main():
    present, missing = check_files()
    print("Checked:", MODEL_DIR)
    print("\nPresent files:")
    for f in present:
        print(f"  - {f}")
    print("\nMissing files:")
    for f in missing:
        print(f"  - {f}")
    if not missing:
        print("\nAll required files are present!")
    else:
        print("\nSome required files are missing. Please add them before running inference.")

if __name__ == "__main__":
    main() 