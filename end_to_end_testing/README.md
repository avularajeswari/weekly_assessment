# End-to-End Testing Application

## 1. Project Purpose

This project demonstrates an end-to-end testing application built using FastAPI and Python.

It covers document questions, unanswerable questions, CRM queries, order queries, and email drafting.

**Note:** The current implementation uses simulated responses and mocked CRM and Order clients. It is not connected to real external services.

## 2. Architecture

The intended architecture contains:

- **UI:** User interface to submit questions.
- **FastAPI:** Receives requests and coordinates processing.
- **Vector Store:** Intended to retrieve relevant document information.
- **CRM Tool:** Intended to retrieve customer details.
- **PostgreSQL:** Intended to store application data.

The current implementation is a simplified mock-based version. These components are shown as the target architecture, not as active integrations.

## 3. Technology Stack

- Python
- FastAPI
- Pytest
- Uvicorn
- unittest.mock

## 4. Project Structure

```text
end_to_end_testing/
├── app/
│   ├── main.py
│   ├── crm_tool.py
│   └── order_tool.py
├── tests/
│   ├── test_e2e.py
│   ├── test_crm.py
│   └── test_order.py
├── reports/
│   ├── scenario_results.csv
│   └── test_report.md
├── .env.example
├── .gitignore
├── requirements.txt
└── test_scenarios.md
```

## 5. Setup Instructions

Clone the repository:

```bash
git clone https://github.com/avularajeswari/weekly_assessment.git
cd weekly_assessment/end_to_end_testing
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 6. Environment Variables

Refer to `.env.example` for placeholder configuration:

```env
API_KEY=your_api_key_here
CRM_API_URL=your_crm_api_url_here
ORDER_API_URL=your_order_api_url_here
```

No real API credentials are required for the current mock implementation.

## 7. How to Run

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open the API documentation:

http://127.0.0.1:8000/docs

Run unit tests in another terminal:

```bash
pytest tests/ -v
```

Run the E2E scenarios:

```bash
python tests/test_e2e.py
```

## 8. Example Questions

### Document Questions
- What is the company's leave policy?
- What is the employee's notice period?

### Unanswerable Questions
- What is the CEO's personal phone number?
- What will the company's revenue be in 2035?

### CRM Questions
- Find customer details for customer ID C101.
- What is the email address of customer C102?

### Order Questions
- Find status of order O501.
- What is delivery date of order O502?

### Email Draft
- Draft an email to a customer explaining a delayed order.

## 9. Testing Results

- E2E scenarios: 10 passed
- CRM unit tests: 3 passed
- Order unit tests: 2 passed
- Total unit tests: 5 passed
- Security scan: No secrets detected

Detailed results are available in the `reports/` directory.

## 10. Future Improvements

- Connect a real document vector store.
- Integrate a real CRM API.
- Integrate a real Order API.
- Add PostgreSQL database persistence.
- Build a user interface for chat interactions.
