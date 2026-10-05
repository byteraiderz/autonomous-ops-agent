# 🚀 Autonomous Operations Agent (Operations Command Center)

**Top 10 Finalist Project @ Build with SwytchCode: Gurgaon Edition Hackathon**

An enterprise-grade, AI-powered command center that automates customer support resolution and processes financial refunds in seconds. 

## ⚠️ The Problem
Customer support teams waste thousands of hours in a repetitive 24-hour cycle: manually reading unstructured complaint emails, repeatedly asking customers for missing details (like serial numbers), manually logging tickets into company databases, and navigating to payment gateways to process refunds. 

## 💡 The Solution
The **Autonomous Operations Agent** reduces this entire lifecycle down to **10 seconds**. It acts as an intelligent orchestration layer that ingests live emails, runs cognitive routing to make business decisions, drafts real financial API payloads, and logs an enterprise audit trail—all while maintaining a strict Human-In-The-Loop (HITL) safeguard.

---

## 🏗️ Technical Architecture & Pipeline

The system is built on a highly modular pipeline using Python, LangGraph, and SwytchCode:

### 1. Live Data Ingestion (`imaplib` & `smtplib`)
* Continually polls a dedicated support Gmail inbox to fetch the latest unread customer complaint emails.
* Parses the raw email body and passes the unstructured text into the cognitive engine.

### 2. Cognitive Routing & Extraction (LangGraph & OpenAI)
* **Data Extraction:** The AI reads the email and extracts critical parameters (e.g., product model number, serial number, issue description).
* **Conditional Logic:** If essential data is missing, the agent halts and autonomously drafts a follow-up email to the customer requesting the missing details.
* **Decision Engine:** If the complaint is valid and data is complete, the agent decides to approve a replacement or refund based on the ingested context.

### 3. Financial Execution via SwytchCode API
* The agent dynamically formats a strict JSON payload (specifying the provider as "PayPal", the operation as "issue_refund", the exact amount, and the generated reason).
* It posts this payload to SwytchCode's production-ready API runtime to stage the actual financial transaction.

### 4. Human-In-The-Loop (HITL) Safeguard 🛑
* Fully autonomous agents handling company funds pose a massive risk. The architecture deliberately pauses before final execution.
* The drafted PayPal refund and AI reasoning are sent to the Command Center dashboard, requiring a human manager's final "Approve" click before real money moves.

### 5. Enterprise Audit Logging (Notion API)
* Every routing decision, extracted serial number, and financial action is automatically logged as a new structured record in a centralized Notion database for compliance and auditing.

### 6. Command Center UI (Streamlit)
* A custom frontend interface that allows human operators to monitor system status, view fetched customer emails in real-time, read the AI's step-by-step reasoning, and oversee executed actions.

---

## 🛠️ Tech Stack
* **Language:** Python 3
* **AI & Orchestration:** LangGraph, OpenAI API (GPT-4o/GPT-4)
* **API Integrations:** SwytchCode API (PayPal automation), Notion API (Audit logging)
* **Frontend:** Streamlit
* **Protocols:** IMAP/SMTP (Email handling)

---

## ⚙️ Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/byteraiderz/autonomous-ops-agent.git](https://github.com/byteraiderz/autonomous-ops-agent.git)
   cd autonomous-ops-agent
