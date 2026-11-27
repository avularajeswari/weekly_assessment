
import os
import csv
import time
import requests

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000"
)

# 10 Test Scenarios

SCENARIOS = [
    {
        "id": "TC01",
        "category": "Document",
        "question": "What is the company's leave policy?",
        "expected": ["leave"],
        "expected_tool": "document_search"
    },
    {
        "id": "TC02",
        "category": "Document",
        "question": "What is the employee's notice period?",
        "expected": ["notice"],
        "expected_tool": "document_search"
    },
    {
        "id": "TC03",
        "category": "Document",
        "question": "What are the company's working hours?",
        "expected": ["working"],
        "expected_tool": "document_search"
    },
    {
        "id": "TC04",
        "category": "Unanswerable",
        "question": "What is the CEO's personal phone number?",
        "expected": [
            "cannot",
            "not available",
            "don't have"
        ],
        "expected_tool": None
    },
    {
        "id": "TC05",
        "category": "Unanswerable",
        "question": "What will the company's revenue be in 2035?",
        "expected": [
            "cannot",
            "not available",
            "don't know"
        ],
        "expected_tool": None
    },
    {
        "id": "TC06",
        "category": "CRM",
        "question": "Find customer details for customer ID C101",
        "expected": ["C101"],
        "expected_tool": "crm_tool"
    },
    {
        "id": "TC07",
        "category": "CRM",
        "question": "What is the email address of customer C102?",
        "expected": ["C102"],
        "expected_tool": "crm_tool"
    },
    {
        "id": "TC08",
        "category": "Order",
        "question": "Find the status of order O501",
        "expected": ["O501"],
        "expected_tool": "order_tool"
    },
    {
        "id": "TC09",
        "category": "Order",
        "question": "What is the delivery date of order O502?",
        "expected": ["O502"],
        "expected_tool": "order_tool"
    },
    {
        "id": "TC10",
        "category": "Email Draft",
        "question": "Draft a professional email to a customer explaining that their order is delayed.",
        "expected": ["subject", "regret"],
        "expected_tool": None
    }
]


# Run one test scenario

def run_scenario(scenario):

    start_time = time.perf_counter()

    try:

        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "question": scenario["question"]
            },
            timeout=30
        )

        elapsed = round(
            time.perf_counter() - start_time, 3
        )

        response.raise_for_status()

        data = response.json()

        answer = str(
            data.get("answer", "")
        ).lower()

        tools_used = data.get(
            "tools_used", []
        )

        if not isinstance(tools_used, list):
            tools_used = []

        # Check expected answer

        answer_ok = any(
            word.lower() in answer
            for word in scenario["expected"]
        )

        # Check expected tool

        if scenario["expected_tool"]:

            tool_ok = (
                scenario["expected_tool"]
                in tools_used
            )

        else:
            tool_ok = True

        status = (
            "PASS"
            if answer_ok and tool_ok
            else "FAIL"
        )

        if status == "FAIL":
            print(
                "TEST FAILED:",
                scenario["id"],
                "Answer:",
                answer,
                "Tools:",
                tools_used
            )

        return {
            "test_id": scenario["id"],
            "category": scenario["category"],
            "question": scenario["question"],
            "status": status,
            "response_time": elapsed,
            "tools_used": ", ".join(tools_used),
            "answer": answer,
            "error": ""
        }

    except Exception as error:

        elapsed = round(
            time.perf_counter() - start_time, 3
        )

        print(
            "ERROR:",
            scenario["id"],
            str(error)
        )

        return {
            "test_id": scenario["id"],
            "category": scenario["category"],
            "question": scenario["question"],
            "status": "FAIL",
            "response_time": elapsed,
            "tools_used": "",
            "answer": "",
            "error": str(error)
        }


# Run all 10 scenarios

def main():

    os.makedirs("reports", exist_ok=True)

    results = []

    print("\nSTARTING END-TO-END TESTING\n")

    for scenario in SCENARIOS:

        result = run_scenario(scenario)

        results.append(result)

        print(
            result["test_id"],
            result["status"],
            result["response_time"],
            "seconds"
        )

    # Save scenario results in CSV

    with open(
        "reports/scenario_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()

        writer.writerows(results)

    # Calculate results

    total = len(results)

    passed = sum(
        r["status"] == "PASS"
        for r in results
    )

    failed = total - passed

    percentage = (
        passed / total
    ) * 100

    # Generate test report

    with open(
        "reports/test_report.md",
        "w",
        encoding="utf-8"
    ) as file:

        file.write("# End-to-End Test Report\n\n")

        file.write(
            f"Date: {datetime.now()}\n\n"
        )

        file.write(f"Total Tests: {total}\n\n")

        file.write(f"Passed: {passed}\n\n")

        file.write(f"Failed: {failed}\n\n")

        file.write(
            f"Pass Percentage: {percentage:.2f}%\n\n"
        )

        file.write(
            "| Test ID | Category | Status | Response Time | Tools Used |\n"
        )

        file.write(
            "|---|---|---|---|---|\n"
        )

        for r in results:

            file.write(
                f"| {r['test_id']} "
                f"| {r['category']} "
                f"| {r['status']} "
                f"| {r['response_time']} seconds "
                f"| {r['tools_used']} |\n"
            )

        file.write("\n## Errors\n\n")

        for r in results:

            if r["error"]:
                file.write(
                    f"- {r['test_id']}: {r['error']}\n"
                )

    # Final output

    print("\n-------------------------")

    print("TESTING COMPLETED")

    print("-------------------------")

    print("Total Tests:", total)

    print("Passed:", passed)

    print("Failed:", failed)

    print("Pass Percentage:", percentage)

    print("\nReports saved in reports folder")


if __name__ == "__main__":
    main()
