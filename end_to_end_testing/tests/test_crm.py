
from unittest.mock import Mock
from app.crm_tool import get_customer


def test_get_customer_success():
    mock_crm = Mock()
    mock_crm.get_customer.return_value = {
        "id": "C101",
        "name": "Ravi",
        "email": "ravi@gmail.com"
    }

    result = get_customer("C101", mock_crm)

    assert result["success"] is True
    assert result["data"]["name"] == "Ravi"


def test_customer_not_found():
    mock_crm = Mock()
    mock_crm.get_customer.return_value = None

    result = get_customer("C999", mock_crm)

    assert result["success"] is False
    assert result["message"] == "Customer not found"


def test_empty_customer_id():
    mock_crm = Mock()

    result = get_customer("", mock_crm)

    assert result["success"] is False
    assert result["message"] == "Customer ID is required"
    mock_crm.get_customer.assert_not_called()