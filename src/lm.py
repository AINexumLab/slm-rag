"""
The Language Model (LM) takes the constructed prompt and generate answer.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

class LM:
    # Sample models:
    # "google/gemma-3-270m" 575.5 MB
    # "google/gemma-3-1b-it" 2.04 GB
    # "ibm-granite/granite-3.1-3b-a800m-instruct" 6.6 GB
    def __init__(self, model_name="google/gemma-3-1b-it"):
        print(f"Model: {model_name}")

        self.device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def generate_text(self, prompt, max_length=256):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=max_length)
        return self.tokenizer.decode(outputs[0])