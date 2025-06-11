# LLaMA Model Directory

Place your LLaMA model files in this directory. The following files are required:

- config.json
- pytorch_model.bin (or model shards, e.g., pytorch_model-00001-of-00002.bin, etc.)
- tokenizer.json
- tokenizer_config.json
- (optional) special_tokens_map.json
- (optional) generation_config.json

Example structure:

models/
└── llama-2-7b/
    ├── config.json
    ├── pytorch_model.bin
    ├── tokenizer.json
    ├── tokenizer_config.json
    ├── special_tokens_map.json
    └── generation_config.json 