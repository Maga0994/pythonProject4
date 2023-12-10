# Задание 1
import psycopg2

#создаем таблицу
def create_table(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            surname VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            number VARCHAR(255)
        );
    """)
    conn.commit()

# таблица для номеров клиента
def create_client_numbers_table(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client_numbers (
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(id),
            number VARCHAR(255) UNIQUE
        );
    """)
    conn.commit()

# добавление клиента
def add_client(conn, cur, name, surname, email, number=None):
    cur.execute("""
        INSERT INTO client(name, surname, email, number) VALUES(%s, %s, %s, %s) RETURNING id, name, surname, email, number;
    """, (name, surname, email, number))
    print(cur.fetchone())
    #conn.commit()

# добавление номера
def add_numbers(conn, cur, client_id, numbers):
    for number in numbers:
        cur.execute("""
            INSERT INTO client_numbers(client_id, number) VALUES(%s, %s) ON CONFLICT DO NOTHING RETURNING id, number;
        """, (client_id, number))
        print(cur.fetchone())
    conn.commit()

# изменение информации
def change_info(conn, cur, id, name=None, surname=None, email=None, number=None):
    update_params = {}
    if name:
        update_params['name'] = name
    if surname:
        update_params['surname'] = surname
    if email:
        update_params['email'] = email
    if number:
        update_params['number'] = number

    update_query = ", ".join([f"{key}=%s" for key in update_params.keys()])
    cur.execute(f"UPDATE client SET {update_query} WHERE id=%s;", list(update_params.values()) + [id])
    conn.commit()


# удаление телефона
def delete_number(conn, cur, client_id, number):
    cur.execute("""
        DELETE FROM client_numbers WHERE client_id = %s AND number = %s;
    """, (client_id, number))
    conn.commit()


# удаление клиента и связанных номеров
def delete_client(conn, cur, client_id):
    # Удаляем все номера клиента из таблицы client_numbers
    cur.execute("""
        DELETE FROM client_numbers WHERE client_id = %s;
    """, (client_id,))

    # удаляем самого клиента из таблицы client
    cur.execute("""
        DELETE FROM client WHERE id = %s;
    """, (client_id,))

    conn.commit()

#поиск клиента
def find_client(conn, cur, name=None, surname=None, email=None, number=None):
    conditions = []
    params = []

    if name:
        conditions.append("name ILIKE %s")
        params.append(f"%{name}%")
    if surname:
        conditions.append("surname ILIKE %s")
        params.append(f"%{surname}%")
    if email:
        conditions.append("email ILIKE %s")
        params.append(f"%{email}%")
    if number:
        conditions.append("number ILIKE %s")
        params.append(f"%{number}%")

    if conditions:
        conditions_str = " AND ".join(conditions)
        query = f"SELECT * FROM client WHERE {conditions_str};"
        cur.execute(query, params)
        return cur.fetchall()
    else:
        print("Не указаны критерии поиска.")
        return []

#удаление таблицы
def drop_table_client(conn, cur, client):
    cur.execute(f"DROP TABLE IF EXISTS {client};")
    conn.commit()

def drop_table_client_numbers(conn, cur, client_numbers):
    cur.execute(f"DROP TABLE IF EXISTS {client_numbers};")
    conn.commit()


with psycopg2.connect(database="personal_info", user="postgres", password="030494Maga") as conn:
    with conn.cursor() as cur:
        drop_table_client_numbers(conn, cur, 'client_numbers')  # если нужно удалить
        drop_table_client(conn, cur, 'client')  # если нужно удалить

        create_table(conn, cur)
        create_client_numbers_table(conn, cur)
        add_client(conn, cur, 'Vladimir', 'Pupkin', '6666@gmail.com', '89996666666')
        add_numbers(conn, cur, 1, ['89998887776'])
        change_info(conn, cur, 1, name='Markkk', surname='Makarskii', email='333222@mail.ru', number='89997333311')
        delete_number(conn, cur, 1, '89996666666')
        delete_client(conn, cur, 1)
        find_client(conn, cur, name='Markkk')



conn.close()
