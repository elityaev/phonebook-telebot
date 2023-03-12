import sqlite3 as sq


def create_db():
    """Создаем таблицы person и phone_number, если они еще не существуют"""
    with sq.connect('phone_book.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS person (
                person_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                second_name TEXT

            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS phone_number (
                        phone_number_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        number INTEGER,
                        person_id INTEGER,
                         FOREIGN KEY (person_id) REFERENCES person(person_id) 
                         ON DELETE CASCADE  
                    );""")
        connection.commit()


def get_all_persons(condition=None):
    "Получаем все контакты"
    with sq.connect('phone_book.db') as connection:
        cursor = connection.cursor()
        if condition:
            result = cursor.execute(f"""SELECT person_id, first_name, second_name 
            FROM person WHERE person.first_name = '{condition}' OR person.second_name = '{condition}'""")
        else:
            result = cursor.execute("""SELECT person_id, first_name, second_name FROM person ORDER BY second_name""")
        return result.fetchall()


def get_person_by_id(person_id):
    """Получаем запись из таблицы person по id"""
    with sq.connect('phone_book.db') as connection:
        cursor = connection.cursor()
        result = cursor.execute(f"""SELECT person_id, first_name, second_name 
        FROM person WHERE person_id = {person_id}""")
        return result.fetchone()


def get_numbers_by_person_id(person_id):
    """Получаем все номера контакта по person_id"""
    with sq.connect('phone_book.db') as connection:
        cursor = connection.cursor()
        result = cursor.execute(f"""SELECT phone_number_id, number 
        FROM phone_number WHERE person_id = {person_id}""")
        return result.fetchall()


def update(model, item_id, field, value):
    """
    В зависимости от передаваемых параметров обновляем
    запись в таблицах person или phone_number
    """
    with sq.connect('phone_book.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"""UPDATE {model} SET {field} = '{value}' WHERE {model}_id = {item_id}""")
        return get_person_by_id(item_id)


def add_person(person_data):
    """Добавляем новую запись в таблицу person"""
    with sq.connect('phone_book.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"""INSERT INTO person(first_name, second_name) VALUES(?, ?)""", person_data)
        connection.commit()
        person_id = cursor.execute(f"""SELECT person_id FROM person
                    WHERE first_name = '{person_data[0]}' AND second_name = '{person_data[1]}'""")
        return person_id.fetchone()[0]


def add_number(number, person_id):
    """Добавляем новую запись в таблицу phone_number"""
    with sq.connect('phone_book.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"""INSERT INTO phone_number(number, person_id) VALUES(?, ?)""", [number, person_id])
        connection.commit()


def delete_person_and_phone_number(person_id):
    """
    Удаляем запись по id из таблицы person и все
    связанные номера телефонов из таблицы phone-number
    """
    with sq.connect('phone_book.db') as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(f"""DELETE FROM person WHERE person_id={person_id}""")
