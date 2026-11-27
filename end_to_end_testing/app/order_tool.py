
def get_order(order_id, order_client):
    order = order_client.get_order(order_id)

    if order is None:
        return {
            "success": False,
            "message": "Order not found"
        }

    return {
        "success": True,
        "data": order
    }
