### still in progress, additional optimization feature


# chunk_preview.py (Azure OpenAI-enabled)


from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import (
    SimpleNodeParser,
    SentenceSplitter,
    SentenceWindowNodeParser
)
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.settings import Settings
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from pathlib import Path
import argparse

# ---- Azure OpenAI Setup ----
aoai_endpoint = "https://msechackathon-eastus2.openai.azure.com/"
model = "gpt-4o"
api_version = "2025-01-01-preview"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

llm = AzureOpenAI(
    engine = "msechackathon-eastus2",
    model=model,
    api_version=api_version,
    azure_endpoint=aoai_endpoint,
    azure_ad_token_provider=token_provider
)

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    api_version=api_version,
    azure_endpoint=aoai_endpoint,
    azure_ad_token_provider=token_provider
)
Settings.llm = llm
Settings.embed_model = embed_model

# -------- Helper: Load and Parse Documents --------
def load_docs(folder):
    reader = SimpleDirectoryReader(input_dir=folder)
    return reader.load_data()

def apply_parser(parser, docs):
    return parser.get_nodes_from_documents(docs)

# -------- CLI Entrypoint --------
def main():
    parser = argparse.ArgumentParser(description="Preview chunking strategies")
    parser.add_argument("folder", type=str, help="Path to the folder containing .md or .txt files")
    parser.add_argument("--strategy", type=str, default="sentence_window",
                        choices=["simple", "sentence_split", "sentence_window"],
                        help="Chunking strategy to use")
    parser.add_argument("--window_size", type=int, default=5, help="Window size for sentence_window parser")
    parser.add_argument("--overlap", type=int, default=2, help="Window overlap for sentence_window parser")
    parser.add_argument("--preview", type=int, default=5, help="Number of chunks to preview")

    args = parser.parse_args()
    docs = load_docs(args.folder)

    if args.strategy == "simple":
        node_parser = SimpleNodeParser()
    elif args.strategy == "sentence_split":
        node_parser = SentenceSplitter()
    else:
        node_parser = SentenceWindowNodeParser.from_defaults(
            window_size=args.window_size,
            llm=llm
        )



    nodes = apply_parser(node_parser, docs)

    for i, node in enumerate(nodes[:args.preview]):
        print("\n" + "=" * 60)
        print(f"Chunk {i+1}:")
        print("=" * 60)
        print(node.text.strip())

if __name__ == "__main__":
    main()
