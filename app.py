import os
import chromadb
import cohere
from chromadb.utils import embedding_functions
from pathlib import Path
from typing import List, Dict

class HCLChatbot:
    def __init__(self, data_folder="data"):
        self.data_folder = Path(__file__).parent / data_folder
        self.documents = []
        self._load_data()
        self._initialize_chroma()

        # Load Cohere API key and initialize client
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set.")
        self.cohere_client = cohere.Client(self.cohere_api_key)

    def _load_data(self):
        if not self.data_folder.exists():
            raise RuntimeError(f"Data folder not found: {self.data_folder}")

        self.documents = []
        for file in os.listdir(self.data_folder):
            if file.endswith(".txt"):
                file_path = self.data_folder / file
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.documents.append({"content": content, "id": file})
        print(f"Loaded {len(self.documents)} text files from {self.data_folder}")

    def _initialize_chroma(self) -> None:
        print("Initializing ChromaDB...")

        self.chroma_client = chromadb.PersistentClient(path="chroma_db")

        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="my_docs",
            embedding_function=self.embedding_func,
            metadata={"hnsw:space": "cosine"}
        )

        if len(self.collection.get()['ids']) == 0:
            print("Indexing documents in ChromaDB...")
            documents = []
            metadatas = []
            ids = []

            for doc in self.documents:
                documents.append(doc["content"])
                metadatas.append({
                    "category": doc.get("category", "general"),
                    "source": "hcl_internal",
                    "doc_id": doc["id"]
                })
                ids.append(str(doc["id"]))

            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

    def retrieve_documents(self, query: str, k: int = 3) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            include=["documents", "metadatas"]
        )

        return [{
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        } for i in range(len(results["documents"][0]))]

    def generate_with_cohere(self, prompt: str) -> str:
        try:
            response = self.cohere_client.chat(
                message=prompt,
                model="command-r-plus",
                temperature=0.3
            )
            return response.text
        except Exception as e:
            return f"Error generating response with Cohere: {str(e)}"

    def generate_response(self, query: str, context: List[str]) -> str:
        context_str = "\n".join([f"• {text}" for text in context])

        prompt = f"""
Context from HCL internal documents:
{context_str}

User Question: {query}

Instructions:
1. Analyze the question and context
2. If answer exists in context, summarize it
3. If information is missing, state you don't know
4. Use professional business tone
5. Never invent information
"""

        return self.generate_with_cohere(prompt)

    def chat_interface(self):
        print("\nHCL Internal Assistant (AI-Powered)")
        print("Type 'exit' to end the conversation\n")

        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break

                docs = self.retrieve_documents(user_input)
                context = [doc["content"] for doc in docs]

                response = self.generate_response(user_input, context)
                print(f"\nAssistant: {response}\n")

            except KeyboardInterrupt:
                print("\nSession ended.")
                break


if __name__ == "__main__":
    chatbot = HCLChatbot()
    chatbot.chat_interface()
