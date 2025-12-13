# 🚀 Quick Start - Generate Your First Script

Get up and running with your fine-tuned Veritasium model in 3 steps!

## Step 1: Authenticate with Hugging Face

```bash
huggingface-cli login
```

Enter your token when prompted. Get your token from: https://huggingface.co/settings/tokens

## Step 2: Install Dependencies (if not already done)

```bash
cd ai-engine
pip install -r requirements.txt
```

**Optional** - For GPU users (faster inference):
```bash
pip install bitsandbytes
```

## Step 3: Generate a Script!

### Method 1: Interactive Mode (Easiest)

```bash
python generate_script.py
```

Then just follow the prompts! 🎉

### Method 2: Command Line

```bash
python generate_script.py --topic "Why does time slow down near black holes?"
```

## Example Topics to Try

- "Why is the speed of light constant?"
- "How does quantum entanglement work?"
- "What makes nuclear fusion so difficult?"
- "Why can't we build a space elevator?"
- "How do computers understand language?"
- "What is the many worlds interpretation?"

## Need Help?

- **Full documentation**: See `USAGE.md`
- **Examples**: Run `./example_usage.sh` or `bash example_usage.sh`
- **Training info**: See `README.md`

## Troubleshooting One-Liners

**Can't login to Hugging Face?**
```bash
# Make sure you have access to Llama 3.1 on HuggingFace first
huggingface-cli whoami  # Check if logged in
```

**Model not found?**
```bash
# Check if adapters exist
ls -la model_adapters/
# Should see: adapter_config.json, adapter_model.safetensors, etc.
```

**Out of memory error?**
```bash
# Use shorter max length
python generate_script.py --topic "Your topic" --max-length 1500
```

---

Happy script generating! 🎥✨

For more advanced usage and customization, see `USAGE.md`.

