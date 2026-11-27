def get_customer(customer_id, crm_client):
    if not customer_id or not customer_id.strip():
        return {
            "success": False,
            "message": "Customer ID is required"
        }

    customer = crm_client.get_customer(customer_id)

    if customer is None:
        return {
            "success": False,
            "message": "Customer not found"
        }

    return {
        "success": True,
        "data": customer
    }
