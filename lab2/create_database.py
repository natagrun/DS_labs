import psycopg2
from psycopg2 import Error
try:
    connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="127.0.0.1",
                                      port="5432")
    cursor = connection.cursor()
    connection.autocommit=True
    cursor.execute('''DO $$
                BEGIN
                    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'server') THEN
                        CREATE USER server WITH PASSWORD 'server' superuser;
                    END IF;
                    
                END
                $$; ''')
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname ='users';")
    if not cursor.fetchone():
        cursor.execute("create database users;")
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
try:
    connection = psycopg2.connect(dbname = "users",user="postgres",
                                  password="postgres",
                                  host="127.0.0.1",
                                  port="5432")
    cursor = connection.cursor()
    connection.autocommit = True
    cursor.execute('''
    CREATE TABLE if not exists person (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age numeric(3,0) check (age>0 and age<100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );''')
    cursor.execute("select * from person;")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")