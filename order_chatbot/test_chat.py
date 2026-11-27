
import requests

URL = "http://127.0.0.1:5000/chat"

question = "Where is order 1042?"

print("\nUser:", question)

response = requests.post(
    URL,
    json={"message": question},
    timeout=360
)

data = response.json()

if response.ok:

    print("\nTool:")

    for item in data.get("tools_used", []):

        tool_name = item["tool"]
        arguments = item["arguments"]

        if tool_name == "get_order_status":
            print(
                f"get_order_status({arguments['order_id']})"
            )

        elif tool_name == "get_customer_orders":
            print(
                f"get_customer_orders({arguments['customer_id']})"
            )

    print("\nAssistant:", data["answer"])

else:
    print("\nError:", data)
