# GetSig

GetSig is a Python script that retrieves method signatures from Python files in a GitHub repository and saves them to a text file. It requires a GitHub Personal Access Token (PAT) to function.

## Usage

1. Make sure you have Python 3.6+ installed.
2. Clone or download this repository.
3. Install the required dependencies:

```bash
pip install PyGithub
```

Run the main.py script:

```bash
python main.py
```

Follow the prompts to provide the GitHub repository URL and your GitHub Personal Access Token (PAT).
The method signatures will be saved to a file named <username>_<repository>_signatures.txt in the output directory.
