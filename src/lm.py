from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

class LM:
    # Sample models:
    # "google/gemma-3-270m" 575.5 MB
    # "google/gemma-3-1b-it" 2.04 GB
    # "ibm-granite/granite-3.1-3b-a800m-instruct" 6.6 GB
    def __init__(self, model_name="google/gemma-3-1b-it"):
        self.device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
        print(f"Model: {model_name}")
    
    def generate_text(self, prompt, desired_output_tokens=256):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        prompt_len = inputs["input_ids"].shape[1]
        print(f"Prompt Length: {prompt_len}")
        
        context_window = self.model.config.max_position_embeddings
        print(f"Context Window: {context_window}")
        
        available_tokens = context_window - prompt_len
        
        max_new_tokens = max(16, min(desired_output_tokens, available_tokens))
        
        if max_new_tokens <= 0:
            raise ValueError(f"Prompt too long ({prompt_len} tokens) for model context window ({context_window}).")
        print(f"Max New Tokens: {max_new_tokens}")
        
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)

        return self.tokenizer.decode(outputs[0])