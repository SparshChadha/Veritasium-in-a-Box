# Kestra Local Development Scripts

## generate_kestra_output.py

A local development script that replicates the functionality of the `multi-agent-research.yaml` Kestra flow.

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
# or
python3 -m pip install --user -r requirements.txt
```

### Usage

```bash
python3 generate_kestra_output.py "Your research topic here"
```

### Options

- `--output-dir DIR`: Specify output directory (default: `../research_outputs`)

### Example

```bash
python3 generate_kestra_output.py "The science of why time moves forward"
```

### What it does

This script runs three research agents in parallel:

1. **Historian**: Searches Wikipedia and Wikidata for historical/contextual information
2. **Skeptic**: Searches Stack Exchange sites and NewsAPI for critical analysis and myths
3. **Professor**: Searches Semantic Scholar for academic papers and research

The results are combined into a single JSON file with the same structure as the Kestra workflow output.

### Output

Creates a file: `../research_outputs/kestra_output.json`

This is useful for:
- Local development and testing
- Debugging research logic without running Kestra
- Generating sample data for frontend development
