
from unittest.mock import Mock
from app.order_tool import get_order


def test_get_order_success():
    mock_order = Mock()

    mock_order.get_order.return_value = {
        "order_id": "O501",
        "status": "Shipped",
        "delivery_date": "2026-12-01"
    }

    result = get_order("O501", mock_order)

    assert result["success"] is True
    assert result["data"]["order_id"] == "O501"
    assert result["data"]["status"] == "Shipped"
    assert result["data"]["delivery_date"] == "2026-12-01"


def test_order_not_found():
    mock_order = Mock()
    mock_order.get_order.return_value = None

    result = get_order("O999", mock_order)

    assert result["success"] is False
    assert result["message"] == "Order not found"
