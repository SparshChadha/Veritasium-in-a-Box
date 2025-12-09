# Multi-Agent Research Workflow - "Triangle of Truth"

## Overview

The Multi-Agent Research Workflow implements a "Triangle of Truth" architecture where three specialized AI agents work in parallel to gather comprehensive research on any topic. The outputs are then synthesized by a Director agent for downstream processing.

## Architecture

### Three Parallel Agents

1. **Agent A - The Historian** 🏛️
   - **Purpose**: Provides general background and context
   - **Source**: Wikipedia API
   - **Output**: Title, summary extract, and URL
   - **Failure Handling**: Must succeed (critical agent)

2. **Agent B - The Skeptic** 🔍
   - **Purpose**: Finds debates, misconceptions, and controversies
   - **Source**: Reddit JSON API (r/science, r/explainlikeimfive, r/askscience)
   - **Output**: Posts about misconceptions, debates, myths, or common errors
   - **Failure Handling**: Allowed to fail (non-critical)

3. **Agent C - The Professor** 🎓
   - **Purpose**: Fetches cutting-edge academic research
   - **Source**: arXiv API
   - **Output**: Top 3 most relevant recent papers with titles, abstracts, authors
   - **Failure Handling**: Must succeed (critical agent)

### The Director (Synthesis Agent)

- **Purpose**: Aggregates all agent outputs into a single JSON structure
- **Current Implementation**: Prints combined JSON for review
- **Future**: Will pass data to Oumi model for content generation

## File Structure

```
kestra/
  └── multi-agent-research.yaml    # Main workflow definition
docker-compose.yml                  # Updated with required dependencies
```

## Dependencies

The following Python packages are pre-installed in the Kestra environment:

- `praw` - Reddit API wrapper
- `arxiv` - arXiv API client
- `requests` - HTTP library for Reddit JSON API
- `beautifulsoup4` - HTML parsing (if needed)

## Usage

### 1. Start Kestra

```bash
docker-compose up -d
```

Wait for Kestra to be available at http://localhost:8080

### 2. Deploy the Workflow

Navigate to http://localhost:8080 and:
- Go to "Flows" in the left sidebar
- Click "Create" or upload the file
- Navigate to namespace `dev`
- Find the flow `multi-agent-research`

### 3. Execute the Flow

- Click on `multi-agent-research`
- Click "Execute"
- Provide a topic (default: "Quantum Entanglement")
- Click "Execute"

### 4. Monitor Execution

- Watch the parallel execution of all three agents
- View real-time logs for each agent
- See the final synthesis output from the Director

## Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `topic` | STRING | "Quantum Entanglement" | Research topic to investigate |

## Output Structure

```json
{
  "topic": "Quantum Entanglement",
  "timestamp": "2025-01-09T14:30:00Z",
  "agents": {
    "historian": {
      "agent": "Historian",
      "title": "...",
      "extract": "...",
      "url": "...",
      "status": "success"
    },
    "skeptic": {
      "agent": "Skeptic",
      "posts": [...],
      "total_found": 5,
      "status": "success"
    },
    "professor": {
      "agent": "Professor",
      "papers": [...],
      "total_found": 3,
      "status": "success"
    }
  },
  "summary": {
    "historian_status": "success",
    "skeptic_status": "success",
    "professor_status": "success"
  }
}
```

## Error Handling

- **Agent B (Skeptic)** is marked with `allowFailure: true`, meaning if Reddit fails, the workflow continues
- **Agent A (Historian)** and **Agent C (Professor)** must succeed for the workflow to complete
- The Director safely parses outputs and handles malformed data
- Status fields indicate success/failure for each agent

## Future Enhancements

### Phase 1: Connect to Oumi Model ✅ (Planned)
- Modify `director_synthesis` task to call Oumi
- Pass combined research JSON as context
- Generate Veritasium-style script

### Phase 2: Advanced Features
- Add more specialized agents (e.g., YouTube transcript analyzer)
- Implement voting/confidence mechanisms
- Add caching to reduce API calls
- Implement retry logic with exponential backoff

### Phase 3: Integration
- Connect to video generation pipeline
- Create end-to-end content creation flow
- Add human review checkpoints

## Troubleshooting

### Reddit API Returns No Results
- Reddit's JSON API can be rate-limited
- The Skeptic agent is allowed to fail, so workflow continues
- Consider adding authentication via PRAW for higher limits

### arXiv Returns Unrelated Papers
- Refine search query in Agent C script
- Consider adding filters for specific categories
- Adjust `max_results` parameter

### Docker Compose Issues
```bash
# Rebuild with new dependencies
docker-compose down
docker-compose up -d --build
```

## Testing

Test with various topics to ensure robustness:

```
- "Quantum Entanglement"
- "Dark Matter"
- "CRISPR Gene Editing"
- "Climate Change"
- "Black Holes"
```

## Contributing

When modifying agents:
1. Test individually before parallel execution
2. Ensure JSON output is properly formatted
3. Add appropriate error handling
4. Update this documentation

## License

Part of the Veritasium-in-a-Box project.
