
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
├── query_with_context.py                                # Main CLI for text-to-KQL
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

- Integration with live Defender Advanced hunting/ IT operations API
- Feedback loop for model correction
- Apply evaluation framework using BIRD

---
## Story

### 👤 Target Persona:
Frank, a security engineer or IT admin responsible for monitoring and managing Defender for Endpoint deployments, configurations and updates across an enterprise. Frank needs fast, reliable insights and a way to stay ahead of issues — without digging through dashboards all day.

### 🌐 Context:
Frankly lives inside Project Franktown, the unified operations center for Defender for Endpoint. It’s part of the broader vision to simplify and centralize operational workflows for Defender for Endpoint.

### 🎯 Problem Statement:
Security engineers spend too much time clicking through tabs, chasing down documentation, switching contexts, and piecing together data just to perform routine checks on Defender agents. This friction makes it difficult to get a clear view of the environment, maintain a healthy device fleet, and scale operational excellence effectively. 

### 💡 Solution:
Frankly is an AI-powered assistant that turns natural language into operational insight. Built with RAG, LlamaIndex, and Defender business context, Frankly enables users to:

 - Query Defender operational health using everyday language

 - Get contextual, actionable answers from unified telemetry

 - Automate routine documentation updates

### ⚙️ Technologies Used:

 - Retrieval-Augmented Generation (RAG) for grounding answers

 - LlamaIndex for indexing business context and querying Defender ops data

 - BIRD Framework for evaluation of query qualities 

### 📌 Outcomes:

 - Reduce time-to-insight and manual investigation

 - Enable non-expert users to interact confidently with security data

 - Help teams scale operations without scaling headcount

Frankly makes Defender operations feel intuitive, conversational, and efficient — turning one security engineer into ten. 🚀

