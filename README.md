
# 🤖 HCL Internal Assistant Chatbot

A local AI-powered chatbot that uses Cohere for response generation and ChromaDB for knowledge retrieval from your internal `.txt` files.

---

## 📁 Project Structure

chatbott-main/
├── app.py # Main chatbot interface
├── ingest_data.py # Data ingestion script for ChromaDB
├── data/ # Folder containing .txt knowledge files
├── chroma_db/ # Auto-generated ChromaDB database
├── requirements.txt # Python dependencies
└── README.md # This file

yaml
Copy
Edit

---

## 🔧 Setup Instructions

### 1. Clone the Repository

bash
git clone https://github.com/yourusername/chatbott-main.git
cd chatbott-main

### 2. Install pyenv (if not already installed)
bash
brew install pyenv
Then add to ~/.zshrc (if using Zsh):

bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
Restart shell:

bash
source ~/.zshrc

### 3. Install Python 3.10 (PyTorch doesn't yet support 3.13)
bash
pyenv install 3.10.13
pyenv local 3.10.13

### 4. Create a Virtual Environment
bash
python -m venv venv
source venv/bin/activate

### 📦 Install Dependencies
bash
pip install --upgrade pip
pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
If you don’t have a requirements.txt, use:

bash
pip install torch==2.2.2 \
            sentence-transformers==2.2.2 \
            chromadb==0.4.22 \
            cohere==4.42 \
            numpy==1.26.4 \
            huggingface-hub==0.14.1 \
            transformers==4.30.2 \
            tokenizers==0.13.3 \
            urllib3==1.26.18
🔐 Set Your API Key
Set your Cohere API key (required for generation):

bash
export COHERE_API_KEY="your-cohere-api-key"
Or create a .env file with this:

ini
COHERE_API_KEY=your-cohere-api-key
And add this to the top of app.py if using .env:

python
from dotenv import load_dotenv; load_dotenv()
📚 Ingest Knowledge Files
Put your .txt documents in the data/ folder.

Run the ingestion script:

bash
python ingest_data.py
This builds the ChromaDB index.

💬 Run the Chatbot
bash
python app.py
Ask anything based on the documents you've ingested!

🧠 Troubleshooting
❌ COHERE_API_KEY environment variable is not set
Solution: export COHERE_API_KEY="your-api-key"

❌ no such column: collections.topic
Cause: ChromaDB database schema is outdated
Solution:

bash
rm -rf chroma_db
python ingest_data.py
❌ module 'torch' has no attribute 'get_default_device'
Cause: Using PyTorch with unsupported Python version (e.g., 3.13)
Solution: Use Python 3.10 via pyenv

📃 License
MIT License — free to use, modify, and distribute.

✨ Credits
Built with:

Cohere

ChromaDB

Sentence-Transformers


