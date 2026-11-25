# ClaimCheck — Financial Report Fact-Checking Assistant

**IAT 360 (NLP) | Group 3:** Martina Hokama, Eugene Yu, Ritah Hu, Vinay Kumar

**ClaimCheck** is a Retrieval-Augmented Generation (RAG) chatbot designed to help everyday investors fact-check claims about public companies against official SEC 10-K annual reports. Users can paste a claim (e.g., *"Apple's revenue dropped 10% in 2023"*) or ask a financial question, and the assistant responds with **Supported**, **Contradicted**, or **Not found in the reports**, quoting the exact report section used to verify the answer.

---

## Architecture & Approach

- **Base Model:** [Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) (Meta, 2024; 8B parameters, Meta Llama 3 Community License). Because its pretrained knowledge cuts off at March 2023 and it cannot cite sources natively, all answers are grounded strictly in retrieved 10-K text.
- **Retrieval Strategy:**
  - **Metadata Pre-Filtering:** Extracts the company (ticker) and fiscal year from the user's query to filter the search space before retrieval. If no year is specified, the system defaults to the latest available year in the dataset and states this explicitly (e.g., *"as of December 31, 2024"*).
  - **Question-to-Question Matching:** Matches user queries against existing dataset questions in addition to document chunks to surface the most relevant financial facts.
- **Guardrails:**
  - Refuses investment advice (e.g., *"Should I buy this stock?"*).
  - Returns *"Not found in the reports"* when a company, year, or metric is out of scope.
  - Prompts the user for clarification when a claim is vague.
- **Deployment:** Interactive web interface built with Gradio and hosted on Hugging Face Spaces.

---

## Datasets

1. **[Multi-Doc-2025](https://huggingface.co/datasets/Anonymous-Team-HC-RAG/Multi-doc-2025)** *(CC BY 4.0)*  
   Public SEC 10-K annual reports from 87 S&P 500 companies across 12 sectors (FY 2022–2024), containing 2,327 Q&A pairs covering facts, calculations, YoY trends, and company comparisons with source sections.
2. **[Financial Q&A 10-K](https://www.kaggle.com/datasets/yousefsaeedian/financial-q-and-a-10k/data)** *(Kaggle)*  
   Supplementary 10-K financial Q&A dataset for expanded coverage and retrieval testing.

---

## Pipeline

1. **Baseline Testing:** Evaluate `Meta-Llama-3-8B-Instruct` without RAG.
2. **Data Cleaning & Pre-processing:** Parse and structure 10-K reports and Q&A pairs.
3. **Knowledge Base Construction:** Define the document corpus and metadata tags (ticker, year).
4. **Embeddings & Indexing:** Generate dense embeddings and build the vector index.
5. **RAG & Guardrails:** Integrate retrieval, prompt constraints, and refusal logic.
6. **Evaluation:** Compare baseline LLM vs. RAG-enabled LLM performance.
7. **Deployment:** Export and deploy the application to Hugging Face Spaces.

---

## Evaluation Plan

- **Test Sets:**
  - Balanced true/false claims adapted from the dataset's test Q&A pairs.
  - **~50 Custom Test Questions** covering Yes/No claims, open-ended questions, paraphrased variations, out-of-scope queries (expected *"I don't know"*), and edge cases designed to test for hallucinations.
- **Metrics:**
  - **Binary Accuracy (True/False):** Whether the response accurately contains the requested fact.
  - **LLM-as-a-Judge:** Automated grading (1–5 scale) by a separate LLM to assess factual accuracy and faithfulness to the retrieved context.

---

## Bias, Privacy & Ethical Considerations

- **Scope & Coverage:** Limited to large US S&P 500 companies (FY 2022–2024); does not cover smaller or international firms.
- **Hallucination Risk:** Mislabeling a false claim as *"Supported"* carries financial risk, which is why exact source citations and strict refusal guardrails are prioritized.
- **Dataset Quality:** Some AI-generated Q&A pairs in the source dataset may contain minor labeling errors despite expert review.
- **Privacy & Disclaimer:** No user queries or personal financial holdings are stored. **ClaimCheck is for educational purposes only and does not constitute financial advice.**

---

## Timeline & Task Distribution

| Milestone | Owner(s) | Target Date |
| :--- | :--- | :--- |
| Discussion post | Martina | Nov 22 |
| Model selection | Eugene | Nov 23 |
| Data cleaning & pre-processing | Ritah, Vinay | Nov 24 |
| RAG pipeline & guardrails | Eugene, Vinay | Nov 28 |
| Interface design | Ritah, Martina | Nov 28 |
| Integration, testing & evaluation | Eugene, Vinay (link); All (test) | Nov 30 |
| Presentation slides | Ritah (draft); Martina (edit) | Dec 2–4 |
| Final presentation | All | Dec 5 |
| Final report | Martina, Ritah | Dec 8 |
