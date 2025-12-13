# Veritasium Llama 3.1 Fine-Tuning Pipeline

This project sets up a fine-tuning pipeline for the Llama-3.1-8B model using transcripts from the Veritasium YouTube channel. It uses a hybrid approach: **Oumi** for robust training and **Unsloth** for high-performance 4-bit inference.

## Prerequisites

- Python 3.10+
- NVIDIA GPU (T4, A10G, or better)
- Hugging Face Account (with access to Llama 3.1)

## 1. Installation

First, install the required Python packages (including Oumi, Unsloth, and PyTorch):

```bash
pip install -r requirements.txt
```

## 2. Authentication (CRITICAL)

Llama-3.1-8B-Instruct is a gated model. You must authenticate with your Hugging Face token to download it.

1. Get your access token from [Hugging Face Settings](https://huggingface.co/settings/tokens).
2. Run the login command:

```bash
huggingface-cli login
```

3. Paste your token when prompted.

## 3. Data Preparation

Fetch the last 50 video transcripts from the Veritasium channel and format them for training:

```bash
python fetch_data.py
```

This will create a `veritasium_train.jsonl` file in the current directory. The script automatically removes sound descriptions like `[Music]` or `[Applause]`.

## 4. Fine-Tuning (Oumi)

Start the fine-tuning process using Oumi and the provided configuration. This uses QLoRA to fine-tune the model efficiently.

```bash
oumi train -c recipe.yaml
```

**Note:** The fine-tuned model adapters will be saved directly to the `model_adapters/` folder.

## 5. Inference - Generate Scripts

There are two ways to generate Veritasium-style scripts with your fine-tuned model:

### Option A: generate_script.py (Recommended - Cross-Platform)

Uses standard `transformers` + `peft` libraries, works on any system (Mac, Linux, Windows):

```bash
# Interactive mode (recommended)
python generate_script.py

# Or generate directly from command line
python generate_script.py --topic "Why is the sky blue?"

# Save to file
python generate_script.py -t "How do black holes work?" -o blackhole_script.txt
```

**Features:**
- Works on Mac, Linux, Windows
- Works with or without GPU
- Interactive mode for easy use
- Flexible generation parameters
- Automatic script saving

See `USAGE.md` for detailed instructions and examples.

### Option B: inference.py (Faster - Linux/Windows GPU only)

Uses **Unsloth** (`FastLanguageModel`) for faster inference on Linux/Windows systems with NVIDIA GPUs:

```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
python inference.py
```

**Note:** Unsloth only works on Linux/Windows with NVIDIA GPU. Use `generate_script.py` for Mac or CPU-only systems.

### How Inference Works:

Both scripts:
1. Load the base Llama 3.1 model in 4-bit quantization (if GPU available)
2. Attach your custom LoRA adapters from `model_adapters/`
3. Use a chat template to prompt the model to "Write a Veritasium-style video script"
4. Generate creative, educational content in Derek's signature style
