from typing import List, Dict
from llama_cpp import Llama

class TextGenerator:
    def __init__(self, model_url: str = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"):
        """Initialize the text generator with a local LLaMA model using llama-cpp-python.
        
        Args:
            model_url: URL to download the GGUF model file
        """
        import os
        import requests
        from pathlib import Path

        # Create models directory if it doesn't exist
        model_dir = Path("models/llama-2-7b")
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Download model if it doesn't exist
        model_path = model_dir / "llama-2-7b-chat.Q4_K_M.gguf"
        if not model_path.exists():
            print(f"Downloading model from {model_url}...")
            response = requests.get(model_url, stream=True)
            response.raise_for_status()
            with open(model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Model downloaded successfully!")

        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=2048,  # Reduced context window for faster processing
            n_threads=8,  # Number of CPU threads to use
            n_gpu_layers=-1,  # Use all GPU layers if available
            n_batch=512,  # Increased batch size for faster processing
            verbose=False  # Disable verbose output for better performance
        )
        
    def generate(self, prompt: str, max_tokens: int = 128) -> str:  # Reduced max_tokens for faster responses
        """Generate text based on the prompt using the local LLaMA model."""
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.95,
            top_k=40,  # Added top_k for better performance
            repeat_penalty=1.1,  # Added repeat penalty to avoid repetitive text
            stop=["<s>", "[INST]", "[/INST]"],
            echo=False
        )
        return output["choices"][0]["text"].strip() 