# 💼 Frankly: Microsoft Defender Text-to-KQL with RAG

This project builds a Retrieval-Augmented Generation (RAG) system that translates natural language questions into Kusto Query Language (KQL) for the `DeviceTvmInfoGathering` table in Microsoft Defender.

Powered by Azure OpenAI and LlamaIndex, it allows IT admin and security engineer personas to query Defender insights using plain English.

---

## 🚀 Features

- 🔎 **Natural language to KQL** conversion
- 📚 **Context-aware reasoning** using business logic and update logs
- 🧠 **Semantic retrieval** from:
  - Data schema
  - Business context
  - Update documentation
- 🧼 Intelligent field mapping
- ❌ Fallback protection when the query is not supported by schema

---

## 📁 Project Structure

```
frankly_mssec/
├── data/
│   └── DeviceTVMInfoGathering_Schema.md        # Main table schema
├── business_context/                           # Business logic markdowns
├── update_logs/                                # Defender update changelogs
├── indexes/
│   ├── business/                               # Persisted vector index
│   ├── data/
│   └── update_logs/
├── generate_index.py                           # Builds vector stores
├── query_kql.py                                # Main CLI for text-to-KQL
├── vector.py                                   # CLI for exploring context indexes
└── requirements.txt                            # Dependencies
```

---

## 🛠 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Authenticate with Azure
```bash
az login
```
Ensure your identity can access Azure OpenAI with Microsoft Entra credentials.

### 3. Generate vector indexes
```bash
python generate_index.py
```
This indexes `business_context`, `update_logs`, and `data` using `text-embedding-3-large`.

---

## 💬 Run Query CLI
```bash
python query_with_context.py
```
Example prompts:
- `list all devices with passive AV mode`
- `show devices with outdated engine`
- `get devices missing AV signature refresh`

If the query references unsupported fields or only exists in business context, you’ll get:
```
-- ❌ This request references unsupported fields or concepts not found in the schema.
```

---

## 🧠 How It Works

- 🧾 **Schema-aware prompt**: schema is passed to guide valid fields
- 🧩 **Retriever-enhanced examples**: relevant documents from all 3 indexes
- 🗣️ **LLM synthesis**: LLM generates clean, safe KQL code
- 🧱 **Guardrails**: block invalid fields or hallucinated logic

---

## 🧪 Evaluate Context Index

You can explore index answers using:
```bash
python vector.py
```

---

## 📌 Notes

- Built with LlamaIndex >= 0.10
- Uses `gpt-4o` for synthesis and `text-embedding-3-large` for search
- Auth via Azure AD (`DefaultAzureCredential`)

---

## 📬 Future Ideas

- Integration with live Defender API
- Feedback loop for model correction
- 


