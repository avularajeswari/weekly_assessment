# crm_server.py

from fastapi import FastAPI, HTTPException

app = FastAPI()

customers = {
    1: {"id": 1, "name": "Priya", "plan": "Premium",
        "email": "priya@gmail.com", "city": "Hyderabad"},

    2: {"id": 2, "name": "Amit", "plan": "Basic",
        "email": "amit@gmail.com", "city": "Mumbai"},

    3: {"id": 3, "name": "Rahul", "plan": "Standard",
        "email": "rahul@gmail.com", "city": "Delhi"},

    4: {"id": 4, "name": "Sneha", "plan": "Premium",
        "email": "sneha@gmail.com", "city": "Bangalore"},

    5: {"id": 5, "name": "Kiran", "plan": "Basic",
        "email": "kiran@gmail.com", "city": "Chennai"}
}


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):

    customer = customers.get(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer