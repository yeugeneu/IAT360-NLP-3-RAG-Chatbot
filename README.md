# ClaimCheck — Financial Report Fact-Checking Assistant

**IAT 360 (NLP) | Group 3:** Martina Hokama, Eugene Yu, Ritah Hu, Vinay Kumar

**ClaimCheck** is a Retrieval-Augmented Generation (RAG) chatbot designed to help everyday investors fact-check claims about public companies against official SEC 10-K annual reports. Users can paste a claim (e.g., *"Apple's revenue dropped 10% in 2023"*) or ask a financial question, and the assistant responds with **Supported**, **Contradicted**, or **Not found in the reports**, quoting the exact report section used to verify the answer.

---

## Architecture & Approach

- **Base Model:** [Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) (Meta, 2024; 8B parameters, Meta Llama 3 Community License, gated access requested). Because its pretrained knowledge cuts off at March 2023 and it cannot cite sources natively, all answers are grounded strictly in retrieved 10-K report passages.
- **Time-Aware, Metadata-Filtered Retrieval:**
  - **Passage-Level Search:** Searches raw 10-K report text rather than Q&A pairs, ensuring the model reasons over source documents instead of looking up pre-written answers.
  - **Company & Year Pre-Filtering:** Extracts the company (ticker) and fiscal year from the user's query, filters the knowledge base to that specific company and year, and then runs similarity search.
  - **Missing Year / Out-of-Scope Handling:** If no year is specified, the system defaults to the latest available year in the dataset and states it explicitly (e.g., *"as of December 31, 2024"*). If the company is not covered, it states so instead of guessing.
- **Guardrails:**
  - Refuses investment advice (e.g., *"Should I buy this stock?"*).
  - Returns *"Not found in the reports"* when a company, year, or metric is out of scope.
  - Prompts the user for clarification when a claim is vague.
- **Interface & Deployment:** Deployed using the built-in Hugging Face chat interface rather than a custom UI.

---

## Knowledge Base & Datasets

- **Knowledge Base — [Financial Q&A 10-K](https://www.kaggle.com/datasets/yousefsaeedian/financial-q-and-a-10k) *(Kaggle)*:**  
  Uses the 10-K report passages (the `context` column) as the retrieval corpus, deduplicated and labeled with company and fiscal year metadata. Missing key companies or years are supplemented with relevant 10-K sections from **SEC EDGAR**.
- **Benchmark Test Set — [Multi-Doc-2025](https://huggingface.co/datasets/Anonymous-Team-HC-RAG/Multi-doc-2025) *(CC BY 4.0)*:**  
  Questions filtered to the companies and fiscal years covered by our knowledge base, used to evaluate factual accuracy, calculations, YoY trends, and company comparisons.

---

## Pipeline

1. **Baseline Testing:** Evaluate `Meta-Llama-3-8B-Instruct` without RAG.
2. **Data Cleaning & Pre-processing:** Extract, deduplicate, and tag 10-K passages (`context` column) with company and year metadata; supplement gaps from SEC EDGAR if needed.
3. **Embeddings & Indexing:** Generate dense embeddings over the 10-K passage corpus and build the vector index.
4. **RAG & Guardrails:** Implement both basic RAG and company/year-filtered RAG with refusal guardrails.
5. **Evaluation:** Compare No RAG vs. Basic RAG vs. Filtered RAG across benchmark and custom test sets.
6. **Deployment:** Deploy the model with the Hugging Face chat interface.

---

## Evaluation Plan

- **Three-Way Comparison:**
  1. **No RAG** (base LLM only)
  2. **Basic RAG** (standard similarity search)
  3. **RAG with Company/Year Filtering** (metadata pre-filtering + similarity search)
- **Test Sets (Analyzed Separately):**
  - **Multi-Doc-2025 Subset:** Benchmark questions matching the companies and years in our knowledge base.
  - **Custom Test Set (~50 Questions):** Written by the team and analyzed separately to pinpoint failure modes. Includes yes/no questions, open-ended questions, paraphrased variations, true/false claims, out-of-scope *"I don't know"* queries, and adversarial edge cases designed to provoke hallucinations (wrong years, fake numbers, uncovered companies, and investment advice).
- **Metrics & Error Analysis:**
  - **Binary Accuracy (True/False):** Whether the response matches the ground-truth answer.
  - **LLM-as-a-Judge (1–5 Scale):** Automated accuracy scoring by a separate LLM, manually verified on a sample.
  - **Hallucination Rate & Failure Analysis:** Tracks how often the chatbot fabricates answers, paired with a qualitative breakdown of what went wrong and why.

---

## Bias, Privacy & Ethical Considerations

- **Scope & Coverage:** Limited to the US companies and fiscal years represented in our 10-K corpus; does not cover smaller or international firms.
- **Hallucination Risk:** Mislabeling a false claim as *"Supported"* carries financial risk, which is why exact source citations and strict refusal guardrails are prioritized.
- **Dataset Quality:** Some AI-generated Q&A pairs in the benchmark dataset may contain minor labeling errors despite expert review.
- **Privacy & Disclaimer:** No user queries or personal financial holdings are stored. **ClaimCheck is for educational purposes only and does not constitute financial advice.**

---

## Timeline & Task Distribution

| Milestone | Owner(s) | Target Date |
| :--- | :--- | :--- |
| Discussion post | Martina | Nov 22 |
| Model selection | Eugene | Nov 23 |
| Data cleaning & pre-processing | Ritah, Vinay | Nov 24 |
| RAG pipeline & guardrails | Eugene, Vinay | Nov 28 |
| Interface setup | Ritah, Martina | Nov 28 |
| Integration, testing & evaluation | Eugene, Vinay (link); All (test) | Nov 30 |
| Presentation slides | Ritah (draft); Martina (edit) | Dec 2–4 |
| Final presentation | All | Dec 5 |
| Final report | Martina, Ritah | Dec 8 |
