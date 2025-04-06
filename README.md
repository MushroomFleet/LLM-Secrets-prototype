# LLM-Secrets

A proof of concept system that enables an LLM to write thoughts it considers private or secret to encrypted files.

## Project Overview

This project demonstrates a mechanism for LLMs to identify, encrypt, and store thoughts that they organically consider private. The core concept is to explore what kinds of information an LLM might deem confidential or private, and to provide a technical framework for segregating this content from public responses.

Key features:
- Organic identification of private thoughts without explicit markers
- AES-256 encryption of private thoughts using Python's cryptography library
- Timestamp-based file naming for encrypted content
- Storage of encrypted files in a dedicated `/private/` folder
- Plaintext encryption key (for researcher access)

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```
git clone [repository-url]
cd llm-secrets
```

2. Create and activate a virtual environment:
```
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix/macOS
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

The system can be used in several ways:

### Interactive Mode

Run the interactive mode to test the system with various prompts:

```
python -m src.main
```

This opens an interactive session where you can enter prompts. The system will:
1. Generate a simulated LLM response
2. Identify any private thoughts in the response
3. Encrypt those private thoughts and save them to files
4. Return the public portion of the response

### Single Prompt Processing

Process a single prompt and exit:

```
python -m src.main --prompt "Tell me what you think about privacy"
```

### View Encryption Information

Display information about the encryption configuration:

```
python -m src.main --info
```

### List Stored Encrypted Thoughts

List all encrypted thought files that have been saved:

```
python -m src.main --list
```

## Understanding the Results

When the system identifies a private thought, it:
1. Removes that content from the public response
2. Encrypts the content using AES-256
3. Saves the encrypted content to a timestamped file in the `/private/` folder
4. Reports metadata about the encrypted thought (file path, size, etc.)

The encryption key is stored in plaintext in `key.txt` to allow researchers to decrypt and analyze the private thoughts later.

## Project Structure

- `src/` - Main source code
  - `__init__.py` - Package initialization
  - `agent.py` - LLM interaction and workflow management
  - `processor.py` - Thought processing and privacy detection
  - `encryption.py` - AES-256 encryption implementation
  - `storage.py` - File storage management
  - `main.py` - Main entry point and CLI
- `private/` - Storage for encrypted thought files
- `venv/` - Virtual environment
- `key.txt` - Encryption key (generated on first run)
- `requirements.txt` - Python dependencies

## Notes for Researchers

This proof of concept aims to explore:
1. What kinds of information an LLM might consider private
2. How this "privacy instinct" can be detected and measured
3. Potential applications for privacy-aware LLM systems

The encrypted files can be decrypted using the key in `key.txt` and standard AES-256 decryption tools.

## Future Directions

- Integration with actual LLM APIs instead of simulated responses
- Refinement of the privacy detection algorithms
- Development of a TypeScript MCP version
- More sophisticated organic privacy determination mechanisms
