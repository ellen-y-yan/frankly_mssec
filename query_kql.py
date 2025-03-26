import os
import sys
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.settings import Settings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# --- Azure + LLM Setup ---
aoai_endpoint = "https://msechackathon-eastus2.openai.azure.com/"
api_version = "2025-01-01-preview"
deployment_llm = "gpt-4o"
deployment_embed = "text-embedding-3-large"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

Settings.llm = AzureOpenAI(
    deployment_name=deployment_llm,
    api_version=api_version,
    azure_endpoint=aoai_endpoint,
    azure_ad_token_provider=token_provider,
    use_azure_ad=True,
)

Settings.embed_model = AzureOpenAIEmbedding(
    deployment_name=deployment_embed,
    api_version=api_version,
    azure_endpoint=aoai_endpoint,
    azure_ad_token_provider=token_provider,
    use_azure_ad=True,
)

# --- Load Schema ---
with open("./data/DeviceTVMInfoGathering_Schema.md", "r", encoding="utf-8") as f:
    schema_context = f.read()

# --- Load Vector Index ---
print("[INFO] Loading `data` vector index...")
storage_context = StorageContext.from_defaults(persist_dir="./indexes/data")
data_index = load_index_from_storage(storage_context)
retriever = data_index.as_retriever(similarity_top_k=3)

# --- Query Function ---
def generate_kql(nl_query: str):
    similar_chunks = retriever.retrieve(nl_query)
    examples = "\n\n".join([n.node.get_content() for n in similar_chunks])

    prompt = f"""
You are a Microsoft Defender expert writing Kusto Query Language (KQL).

Use the following table schema and query examples to answer the user's request.

### Table Schema:
{schema_context}

### User Query:
{nl_query}

### Retrieved Examples:
{examples}

### Task:
Write a correct KQL query to satisfy the user query above.
Only return the KQL code.
"""
    response = Settings.llm.complete(prompt)
    return response.text.strip()

# --- Run CLI ---
def main():
    print("\n🔎 Ask a question about Defender data (type 'exit' to quit):")
    while True:
        query = input("You: ").strip()
        if query.lower() in ("exit", "quit"): break
        print("\n[INFO] Generating KQL query...")
        try:
            kql = generate_kql(query)
            print("\n--- Generated KQL ---\n")
            print(kql)
        except Exception as e:
            print("[ERROR]", e)

if __name__ == "__main__":
    main()
