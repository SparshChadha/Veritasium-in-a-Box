from unsloth import FastLanguageModel
import torch

# Configuration
MODEL_PATH = "./model_adapters" 
MAX_SEQ_LENGTH = 8192

def generate_script(topic):
    print(f"⏳ Loading Veritasium model for topic: {topic}...")
    
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = MODEL_PATH,
        max_seq_length = MAX_SEQ_LENGTH,
        dtype = None,
        load_in_4bit = True,
    )
    FastLanguageModel.for_inference(model)

    messages = [{"role": "user", "content": f"Write a Veritasium-style video script about: {topic}"}]
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize = True,
        add_generation_prompt = True,
        return_tensors = "pt",
    ).to("cuda")

    print("🎥 Generating script...")
    outputs = model.generate(
        input_ids = inputs,
        max_new_tokens = 2048,
        use_cache = True,
        temperature = 0.8,
        min_p = 0.1,
        repetition_penalty = 1.1, 
        do_sample = True
    )
    
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

if __name__ == "__main__":
    print("--- Veritasium Script Generator ---")
    topic = input("Enter a video topic: ")
    print("\n" + generate_script(topic))
