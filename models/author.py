
from database.connection import get_db_connection

class Author:
    def __init__(self, name):
        self.name = name
        self.id = None
        self._create_in_db()

    def _create_in_db(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (self.name,))
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_by_id(author_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
            row = cursor.fetchone()
            if row:
                return Author(row[1])
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
