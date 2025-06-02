from shared.database import get_db_connection

def create_order(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO game_order (gamer_id) VALUES (%s)", (gamer_id,))
        order_id = cursor.lastrowid
        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def add_order_detail(order_id, game_id, description="Pembelian game"):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO order_detail (order_id, game_id, description) VALUES (%s, %s, %s)",
            (order_id, game_id, description)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def check_game_already_owned(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 1 FROM order_detail od
        JOIN game_order go ON od.order_id = go.order_id
        WHERE go.gamer_id = %s AND od.game_id = %s
    ''', (gamer_id, game_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None
