from unsloth import FastLanguageModel
import torch
import os

# Configuration
MODEL_PATH = "model_adapters"  # Relative to fine_tuned_model directory
MAX_SEQ_LENGTH = 8192

# GPU check and device configuration
try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    if DEVICE == "cuda":
        print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️  No GPU available, using CPU (may be slower)")
except ImportError:
    print("⚠️  PyTorch not available, using CPU")
    DEVICE = "cpu"

# --- THE FIX: Standard Llama 3 Chat Template ---
# We define this here because your tokenizer_config.json is missing it.
LLAMA_3_CHAT_TEMPLATE = (
    "{% set loop_messages = messages %}"
    "{% for message in loop_messages %}"
        "{% set content = message['content'] %}"
        "{% if message['role'] == 'user' %}"
            "{{ '<|start_header_id|>user<|end_header_id|>\n\n' + content | trim + '<|eot_id|>' }}"
        "{% elif message['role'] == 'assistant' %}"
            "{{ '<|start_header_id|>assistant<|end_header_id|>\n\n' + content | trim + '<|eot_id|>' }}"
        "{% elif message['role'] == 'system' %}"
            "{{ '<|start_header_id|>system<|end_header_id|>\n\n' + content | trim + '<|eot_id|>' }}"
        "{% endif %}"
    "{% endfor %}"
    "{% if add_generation_prompt %}"
        "{{ '<|start_header_id|>assistant<|end_header_id|>\n\n' }}"
    "{% endif %}"
)

def generate_script(topic):
    print(f"⏳ Loading Veritasium model for topic: {topic}...")
    
    if not os.path.exists(os.path.join(MODEL_PATH, "adapter_config.json")):
        return f"Error: Model adapters not found at {MODEL_PATH}"

    # Load the model and tokenizer from your local folder
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = MODEL_PATH,
        max_seq_length = MAX_SEQ_LENGTH,
        dtype = None,
        load_in_4bit = True,
    )
    
    # --- APPLY THE FIX ---
    # If the loaded tokenizer doesn't have a template (which yours doesn't), we add it now.
    if tokenizer.chat_template is None:
        print("⚠️  Chat template missing in tokenizer_config.json. Applying fix...")
        tokenizer.chat_template = LLAMA_3_CHAT_TEMPLATE
        
    FastLanguageModel.for_inference(model)

    messages = [{"role": "user", "content": f"Write a Veritasium-style video script about: {topic}"}]
    
    # Now this line will work because we fixed the template above
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
    
    generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    
    # Cleanup output
    if "assistant\n" in generated_text:
        return generated_text.split("assistant\n")[-1].strip()
    elif "assistant" in generated_text:
        return generated_text.split("assistant")[-1].strip()
        
    return generated_text

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, help="Video topic")
    args = parser.parse_args()

    topic = args.topic
    if not topic:
        print("--- Veritasium Script Generator ---")
        topic = input("Enter a video topic: ")
    
    script = generate_script(topic)
    
    print("\n" + "="*60)
    print("✨ FINAL SCRIPT ✨")
    print("="*60)
    print(script)
    
    # Save output
    output_path = "../research_outputs/finetuned_script.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"\n💾 Saved draft to: {output_path}")