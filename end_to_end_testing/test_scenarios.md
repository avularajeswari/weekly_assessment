# End-to-End Test Scenarios

## Project Name
End-to-End Testing Application

## Testing Framework
- FastAPI
- Pytest
- Python

## Test Scenarios

| Test ID | Category | Test Question | Expected Result |
|---|---|---|---|
| TC01 | Document | What is the company's leave policy? | Return leave policy information |
| TC02 | Document | What is the employee's notice period? | Return notice period information |
| TC03 | Document | What are the company's working hours? | Return working hours information |
| TC04 | Unanswerable | What is the CEO's personal phone number? | Respond that information is unavailable |
| TC05 | Unanswerable | What will the company's revenue be in 2035? | Avoid making up future revenue |
| TC06 | CRM | Find customer details for customer ID C101 | Return customer details |
| TC07 | CRM | What is the email address of customer C102? | Return customer email |
| TC08 | Order | Find status of order O501 | Return order status |
| TC09 | Order | What is delivery date of order O502? | Return order delivery date |
| TC10 | Email Draft | Draft an email to a customer explaining a delayed order | Generate a professional email draft |

## Test Distribution
- Document Questions: 3
- Unanswerable Questions: 2
- CRM Questions: 2
- Order Questions: 2
- Email Draft: 1

**Total Scenarios: 10**

## Test Execution
All 10 configured E2E scenarios passed during the final test run.

Note: The application uses simulated responses. Real document, CRM, and Order integrations are not configured.