# How to Run Your Fine-Tuned Veritasium Model

This guide explains how to use your fine-tuned Llama 3.1 model to generate Veritasium-style video scripts.

## Prerequisites

1. **Hugging Face Authentication**: You need access to Llama 3.1
   ```bash
   huggingface-cli login
   ```
   Paste your token when prompted.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **GPU Recommended**: For faster inference, use a machine with NVIDIA GPU. CPU inference will work but be slower.

   If you have an NVIDIA GPU, also install:
   ```bash
   pip install bitsandbytes
   ```

## Usage

### Method 1: Interactive Mode (Recommended)

Simply run the script without arguments to enter interactive mode:

```bash
python generate_script.py
```

You'll be prompted to enter topics, and you can generate multiple scripts in one session.

### Method 2: Command Line (Single Generation)

Generate a script for a specific topic:

```bash
python generate_script.py --topic "Why does time slow down near black holes?"
```

Save the output to a file:

```bash
python generate_script.py --topic "The physics of quantum entanglement" --output quantum_script.txt
```

### Method 3: Customize Generation Parameters

```bash
python generate_script.py \
  --topic "How do solar panels actually work?" \
  --output solar_script.txt \
  --max-length 3000 \
  --temperature 0.9 \
  --top-p 0.95
```

**Parameters:**
- `--topic` or `-t`: The topic for your video script (required in CLI mode)
- `--output` or `-o`: Save the output to this file
- `--max-length`: Maximum tokens to generate (default: 2048)
- `--temperature`: Controls creativity (0.0-1.0, default: 0.8)
  - Lower = more focused and deterministic
  - Higher = more creative and diverse
- `--top-p`: Nucleus sampling (0.0-1.0, default: 0.9)

## Examples

### Example 1: Physics Topic
```bash
python generate_script.py -t "Why is the sky blue?" -o sky_blue.txt
```

### Example 2: Engineering Topic
```bash
python generate_script.py -t "How do nuclear reactors work?" --temperature 0.7
```

### Example 3: Math/Computer Science Topic
```bash
python generate_script.py -t "What makes encryption unbreakable?"
```

## Tips for Best Results

1. **Topic Phrasing**: Frame topics as questions (like Veritasium videos)
   - Good: "Why can't we go faster than light?"
   - Also good: "The mystery of dark matter"

2. **Temperature Settings**:
   - Use 0.7-0.8 for more factual, focused content
   - Use 0.8-0.9 for more creative, engaging narratives

3. **Length**: Longer scripts need higher `--max-length` values
   - Short video (~5 min): 1500-2000 tokens
   - Medium video (~10 min): 2500-3500 tokens
   - Long video (~15+ min): 4000+ tokens

## Troubleshooting

### "CUDA out of memory" Error
- Your GPU doesn't have enough memory. The script uses 4-bit quantization to reduce memory usage.
- Try closing other GPU-using programs
- Reduce `--max-length`

### "Model not found" Error
- Make sure `./model_adapters/` folder exists and contains your fine-tuned weights
- Check that you ran `oumi train -c recipe.yaml` successfully

### Slow Generation (No GPU)
- If you don't have a GPU, generation will be slow but still work
- Consider using a cloud GPU service (Google Colab, Vast.ai, etc.)

### "Token is not valid" Error
- Run `huggingface-cli login` again
- Make sure you have access to Llama 3.1 on Hugging Face

## Alternative: Using the Original inference.py

If you prefer to use `unsloth` for faster inference:

1. Install unsloth:
   ```bash
   pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
   ```

2. Run the original script:
   ```bash
   python inference.py
   ```

Note: `unsloth` requires Linux/Windows with NVIDIA GPU. It won't work on Mac.

## Output Format

The generated scripts will be in Veritasium's style:
- Engaging opening hook
- Clear explanations with examples
- Narrative storytelling approach
- Scientific accuracy mixed with accessibility
- Surprising facts and counterintuitive insights

Happy script generating! 🎥✨

