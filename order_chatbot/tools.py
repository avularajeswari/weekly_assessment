
from database import get_connection


def get_order_status(order_id):

    if isinstance(order_id, bool) or not isinstance(order_id, int) or order_id <= 0:
        return {"error": "Invalid order ID"}

    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cur:
            cur.execute("""
                SELECT order_id, customer_id, status,
                       shipped_date, delivery_status
                FROM orders
                WHERE order_id = %s
            """, (order_id,))

            row = cur.fetchone()

            if row is None:
                return {"message": f"Order {order_id} was not found."}

            return {
                "order_id": row[0],
                "customer_id": row[1],
                "status": row[2],
                "shipped_date": str(row[3]) if row[3] else None,
                "delivery_status": row[4]
            }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()


def get_customer_orders(customer_id):

    if isinstance(customer_id, bool) or not isinstance(customer_id, int) or customer_id <= 0:
        return {"error": "Invalid customer ID"}

    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cur:
            cur.execute("""
                SELECT order_id, customer_id, order_date,
                       status, shipped_date, delivery_status
                FROM orders
                WHERE customer_id = %s
                ORDER BY order_date DESC
            """, (customer_id,))

            rows = cur.fetchall()

            return {
                "customer_id": customer_id,
                "orders": [
                    {
                        "order_id": row[0],
                        "customer_id": row[1],
                        "order_date": str(row[2]),
                        "status": row[3],
                        "shipped_date": str(row[4]) if row[4] else None,
                        "delivery_status": row[5]
                    }
                    for row in rows
                ]
            }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()
