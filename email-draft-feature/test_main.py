
import os

# Allow tests to run without a real API key
os.environ.setdefault("OPENAI_API_KEY", "test-key")

from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


# Test 1: Order delivery conversation
def test_order_email(monkeypatch):

    def mock_ai(conversation, tone):
        return main.EmailDraft(
            subject="Update Regarding Your Laptop Order",
            body=(
                "Dear Customer,\n\n"
                "Thank you for contacting us regarding "
                "order 12345. We apologize for the delivery "
                "delay. Your order is expected to arrive tomorrow.\n\n"
                "Please let us know if you need further assistance.\n\n"
                "Best regards,\nCustomer Support"
            )
        )

    monkeypatch.setattr(
        main,
        "create_draft_with_ai",
        mock_ai
    )

    response = client.post(
        "/draft-email",
        json={
            "session_id": "session_1",
            "tone": "formal"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subject"] == "Update Regarding Your Laptop Order"
    assert "12345" in data["body"]
    assert "tomorrow" in data["body"]


# Test 2: Python course conversation
def test_course_email(monkeypatch):

    def mock_ai(conversation, tone):
        return main.EmailDraft(
            subject="Details About Our Python Course",
            body=(
                "Hello,\n\n"
                "Thank you for your interest in our Python course. "
                "The course runs for 8 weeks and costs Rs. 5000.\n\n"
                "You mentioned that you are interested in joining "
                "next month. Please let us know if you would like "
                "to proceed with registration.\n\n"
                "Best regards,\nCourse Support Team"
            )
        )

    monkeypatch.setattr(
        main,
        "create_draft_with_ai",
        mock_ai
    )

    response = client.post(
        "/draft-email",
        json={
            "session_id": "session_2",
            "tone": "friendly"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subject"] == "Details About Our Python Course"
    assert "8 weeks" in data["body"]
    assert "5000" in data["body"]
    assert "next month" in data["body"]
