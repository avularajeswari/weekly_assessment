# 5-Minute Project Demo – AI Resume Analyzer

## 1. Project Introduction (30 seconds)

This project demonstrates an AI-powered application with document question answering, CRM operations, order management, and email draft generation.

The application is built using Python and FastAPI. Automated tests are used to verify the application behavior.

## 2. Document Question Answering (1 minute)

**Objective:** Answer questions based on company documents.

**Example Question:**
"What is the company's leave policy?"

**Expected Result:**
The application provides an answer based on the available document information.

## 3. CRM Tool Call (1 minute)

**Objective:** Retrieve customer information using the CRM tool.

**Example Question:**
"Find customer details for customer ID C101."

**Expected Result:**
The application retrieves the customer information using the CRM tool.

## 4. Unanswerable Question – Refusal (1 minute)

**Objective:** Prevent the application from providing unsupported information.

**Example Question:**
"What is the CEO's personal phone number?"

**Expected Result:**
The application indicates that this information is unavailable instead of inventing an answer.

## 5. Email Draft Generation (1 minute)

**Objective:** Generate an email draft for customer communication.

**Example Question:**
"Draft an email to a customer explaining a delayed order."

**Expected Result:**
The application generates an email draft explaining the order delay.

## 6. Conclusion (30 seconds)

The project demonstrates document question answering, CRM tool usage, refusal handling, and email draft generation.

Automated testing was performed to validate the application behavior.

**Note:** The current implementation uses mock responses and does not connect to real external CRM, order, vector database, or PostgreSQL services. The architecture diagram represents the proposed target architecture.