# Задание 1
import psycopg2

conn = psycopg2.connect(database="personal_info",
                        user="postgres",
                        password="030494Maga")
with conn.cursor() as cur:
    cur.execute("""
    DROP TABLE client;
    """)
    def create_table(conn):
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
    create_table(conn)

    #добавление клиента
    def add_client(conn, name, surname, email, number=None):
        cur.execute("""
            INSERT INTO client(name, surname, email, number) VALUES('Volodya', 'Semenov', '123@mail.ru', '88005553535') RETURNING id, name, surname, email, number;
            """)
        print(cur.fetchone())
        #conn.commit()
    add_client(conn, name='', surname='', email='', number=None)

    #добавление номера
    def add_numbers(conn, id, number):
        cur.execute("""
            INSERT INTO client(number) VALUES(89266666666) RETURNING id, number;
            """)
        print(cur.fetchone())
        #conn.commit()
    add_numbers(conn, id, number='')

    #изменение информации
    def change_info(conn, id, name=None, surname=None, email=None, number=None):
        #cur.execute("""
           # UPDATE client SET name=%s, surname=%s, email=%s, number=%s WHERE id=%s;  Вариант, где все сразу
          #  """, ('Markkk', 'Makarov', '2222@mail.ru', '9999221121', 1))
        cur.execute("""
                    UPDATE client SET name=%s WHERE id=%s;
                    """, ('Markkk', 1))
        cur.execute("""
                    UPDATE client SET surname=%s WHERE id=%s;
                    """, ('Makarskii', 1))
        cur.execute("""
                    UPDATE client SET email=%s WHERE id=%s;
                    """, ('333222@mail.ru', 2))
        cur.execute("""
                    UPDATE client SET number=%s WHERE id=%s;
                    """, ('89997333311', 1))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())
        #conn.commit()
    change_info(conn, id, name='', surname='', email='', number='')


    # удаление телефона
    def delete_number(conn, id, number):
        cur.execute("""
            UPDATE client SET number=NULL WHERE id=%s;
                    """, (2,))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())
        #conn.commit()
    delete_number(conn, id, number='')


    # удаление клиента
    def delete_client(conn, id, number=None):
        cur.execute("""
            DELETE FROM client WHERE id=%s;
            """, (2, ))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())
        #conn.commit()
    delete_client(conn, id)

    #поиск клиента
    def find_client(conn, name=None, surname=None, email=None, number=None):
        cur.execute("""
            SELECT * FROM client WHERE name LIKE %s;
            """, (f"%{''}%", ))
        cur.execute("""
            SELECT * FROM client WHERE surname LIKE %s;
            """, (f"%{''}%", ))
        cur.execute("""
            SELECT * FROM client WHERE email LIKE %s;
            """, (f"%{'123@mail.ru'}%", ))
        cur.execute("""
            SELECT * FROM client WHERE number LIKE %s;
            """, (f"%{''}%",))

        print(cur.fetchall())
        #conn.commit()
    find_client(conn, name='', surname='', email='', number='')

