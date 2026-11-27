
from database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM order_items")
    item_count = cursor.fetchone()[0]

    print("Database connection successful!")
    print("Total orders:", order_count)
    print("Total order items:", item_count)

    cursor.close()
    conn.close()

except Exception as e:
    print("Database verification failed:", e)
