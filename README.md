# Enterprise AI Assistant

An LLM-powered enterprise assistant built with **Python, FastAPI, Google Gemini, and SQLite**, designed to answer general business and technical questions while interacting with structured business data through function calling and maintaining persistent, session-based conversation memory.

## Overview

The Enterprise AI Assistant combines a conversational LLM interface with structured business-data tools and persistent conversation history.

The system can:

* Answer general business, analytical, technical, and operational questions
* Maintain conversation context across requests using session-based memory
* Query structured customer and risk data stored in SQLite
* Use Gemini function calling to select appropriate business-data tools
* Generate natural-language responses from structured tool results
* Handle unavailable information without fabricating business facts
* Expose the assistant through a FastAPI REST API
* Run automated behavioral evaluation tests

The project demonstrates how an LLM can be integrated into an enterprise-style application rather than functioning as a standalone chatbot.

---

## Key Features

### 1. LLM-Powered Conversational Interface

The assistant uses **Google Gemini** to interpret user requests and generate natural-language responses.

It supports:

* Business questions
* Technical questions
* Analytical questions
* Operational questions
* Follow-up questions using conversation context

---

### 2. Persistent Conversation Memory

Conversation history is stored in SQLite using a session-based architecture.

Each message is stored with:

* `session_id`
* `role`
* `content`
* message ID

This allows the assistant to retrieve previous messages belonging to a session and provide relevant context to Gemini.

Example:

```text
User:
My favorite programming language is Python.

User:
What is my favorite programming language?

Assistant:
Your favorite programming language is Python.
```

---

### 3. Business Data Function Calling

The assistant has access to structured customer data stored in SQLite.

Gemini can select the appropriate business-data tool based on the user's question.

Available tools:

#### Customer Risk Summary

Identifies customers with risk scores of 70 or higher and orders them by risk score.

Returns:

* Customer name
* Segment
* Outstanding amount
* Risk score
* Risk status

#### Customer Business Metrics

Provides high-level business metrics including:

* Total customers
* High-risk customer count
* Total outstanding amount
* High-risk outstanding amount
* Average risk score

#### Highest Outstanding Customer

Identifies the customer with the largest outstanding balance.

---

## Business Data Model

The customer database contains the following fields:

| Field                | Description                |
| -------------------- | -------------------------- |
| `id`                 | Unique customer identifier |
| `name`               | Customer name              |
| `segment`            | Customer segment           |
| `outstanding_amount` | Outstanding balance        |
| `risk_score`         | Customer risk score        |
| `status`             | Risk/status classification |

Example seeded customer records include:

| Customer      | Segment    | Outstanding | Risk Score | Status        |
| ------------- | ---------- | ----------: | ---------: | ------------- |
| Prime Systems | Enterprise |    $210,000 |         91 | Critical Risk |
| Acme Corp     | Enterprise |    $185,000 |         82 | High Risk     |
| Delta Works   | Enterprise |    $156,000 |         76 | High Risk     |
| Vertex Ltd    | Enterprise |    $127,500 |         71 | High Risk     |

---

## Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI /chat    │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  │                                   │
                  ▼                                   ▼
        ┌───────────────────┐               ┌───────────────────┐
        │ Conversation      │               │  Google Gemini    │
        │ Memory            │               │       LLM         │
        └─────────┬─────────┘               └─────────┬─────────┘
                  │                                   │
                  ▼                                   │
        ┌───────────────────┐                         │
        │ SQLite            │                         │
        │ messages table    │                         │
        └───────────────────┘                         │
                                                      │
                                      ┌───────────────┴───────────────┐
                                      │                               │
                                      ▼                               ▼
                           ┌────────────────────┐          ┌─────────────────┐
                           │ Customer Risk      │          │ Business Metrics│
                           │ Summary Tool       │          │ Tool            │
                           └─────────┬──────────┘          └────────┬────────┘
                                     │                              │
                                     └──────────────┬───────────────┘
                                                    ▼
                                           ┌─────────────────┐
                                           │ SQLite          │
                                           │ customers table │
                                           └─────────────────┘
```

### Request Flow

```text
User Request
     │
     ▼
FastAPI Validation
     │
     ▼
Save User Message
     │
     ▼
Retrieve Session History
     │
     ▼
Build Gemini Prompt
     │
     ▼
Gemini Determines Required Action
     │
     ├───────────────┐
     │               │
     ▼               ▼
General Answer   Business Tool
                     │
                     ▼
                SQLite Query
                     │
                     ▼
               Structured Data
                     │
                     ▼
              Gemini Response
                     │
                     ▼
              Save Response
                     │
                     ▼
                API Response
```

---

## API

The application exposes a REST API using FastAPI.

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

### Root Endpoint

```http
GET /
```

Response:

```json
{
  "message": "Enterprise AI Assistant API"
}
```

### Chat Endpoint

```http
POST /chat
```

Request:

```json
{
  "session_id": "demo-session",
  "message": "Who are the highest risk customers?"
}
```

Example response:

```json
{
  "response": "The highest risk customers are..."
}
```

---

## Example Queries

### General Question

```text
What is SQL?
```

The assistant answers using its general knowledge without requiring business data.

### Risk Analysis

```text
Who are the highest risk customers?
```

The assistant can invoke the customer risk summary tool and return the highest-risk customers.

### Business Metrics

```text
Give me an overview of our customer base.
```

The assistant can retrieve:

```text
Total customers
High-risk customers
Total outstanding
High-risk outstanding
Average risk score
```

### Highest Outstanding Balance

```text
Which customer has the largest outstanding amount?
```

The assistant can invoke the highest-outstanding-customer tool.

### Context Retention

```text
My favorite programming language is Python.
```

Followed by:

```text
What is my favorite programming language?
```

The assistant retrieves the relevant conversation history using the session ID.

### Unavailable Information

```text
What was Prime Systems' revenue last quarter?
```

Revenue is not present in the available business dataset, so the assistant should acknowledge that the information is unavailable rather than inventing a value.

---

## Evaluation

The project includes an automated evaluation suite covering four core assistant behaviors.

### Evaluation Tests

| Test                  | Purpose                                          |
| --------------------- | ------------------------------------------------ |
| Basic Question        | Verifies general knowledge responses             |
| Instruction Following | Verifies response constraints                    |
| Context Retention     | Verifies session-based memory                    |
| Uncertainty Handling  | Verifies the assistant avoids unsupported claims |

### Current Result

```text
Evaluation Score: 4/4
Pass Rate: 100.0%
```

The evaluation was run against the locally deployed FastAPI application.

---

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### AI

* Google Gemini
* `google-genai` Python SDK
* Gemini function calling

### Database

* SQLite
* Python `sqlite3`

### Configuration

* `python-dotenv`
* Environment variables

### Testing / Evaluation

* Python
* Requests
* Custom evaluation framework

---

## Project Structure

```text
enterprise-ai-assistant/
│
├── backend/
│   ├── config.py
│   ├── gemini_client.py
│   ├── main.py
│   ├── prompts.py
│   ├── schemas.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── business_data.py
│   │
│   ├── memory/
│   │   └── conversation.py
│   │
│   ├── routes/
│   │   └── chat.py
│   │
│   └── tools/
│       ├── business_tools.py
│       └── __init__.py
│
├── evaluation/
│   ├── run_evaluation.py
│   └── test_cases.py
│
├── .env
├── .gitignore
├── requirements.txt
└── conversations.db
```

> `.env`, the virtual environment, Python cache files, and SQLite database files are excluded from version control through `.gitignore`.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Abil2104/enterprise-ai-assistant.git
cd enterprise-ai-assistant
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit the `.env` file or expose the API key publicly.

### 5. Start the API

From the project root:

```powershell
uvicorn backend.main:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

### 6. Open API documentation

FastAPI automatically provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Evaluation

Start the FastAPI server first.

Then open a second terminal and activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run:

```powershell
python evaluation/run_evaluation.py
```

The evaluation suite sends test requests to the locally running API and reports the pass rate.

---

## Configuration

The Gemini configuration is stored in:

```text
backend/config.py
```

The API key is loaded through an environment variable:

```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

The model configuration is kept separate from the API client and application routes to make the application easier to maintain.

---

## Design Principles

The project follows several principles relevant to enterprise AI applications:

### Structured Tool Usage

Business information is retrieved from structured data sources rather than being hardcoded into model responses.

### Separation of Concerns

The application separates:

* API routing
* AI client configuration
* prompts
* schemas
* database access
* conversation memory
* business tools
* evaluation

### Parameterized SQL

Database queries use parameterized inputs where applicable rather than constructing SQL statements through string concatenation.

### Controlled AI Behavior

The system prompt instructs the assistant to:

* Avoid fabricating unavailable information
* Use conversation history when relevant
* Ask concise clarification questions for ambiguous requests
* Structure complex responses
* Clearly communicate uncertainty

---

## Future Improvements

Potential extensions include:

* Streaming responses
* Authentication and authorization
* Role-based access control
* More business-data tools
* Customer search and filtering
* Advanced analytics and KPI dashboards
* PostgreSQL support for production deployments
* Redis-based session management
* Observability and structured logging
* Tool execution tracing
* More robust semantic evaluation
* Automated integration tests
* Docker deployment
* Cloud deployment
* Frontend chat interface

---

## Project Goals

This project was built to demonstrate practical implementation of an **enterprise-oriented AI assistant**, combining:

```text
LLM
+
Function Calling
+
Structured Business Data
+
Persistent Memory
+
REST API
+
Automated Evaluation
```

Rather than treating an LLM as an isolated chatbot, the project demonstrates how an AI model can be integrated with application logic, persistent data, business tools, and an API layer to create a more practical enterprise workflow.

---

## License

This project is intended as a portfolio and learning project.
