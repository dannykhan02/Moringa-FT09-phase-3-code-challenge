from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.id = None
        self._create_in_db()

    def _create_in_db(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', 
                           (self.name, self.category))
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(magazine_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine_id,))
            row = cursor.fetchone()
            if row:
                magazine = Magazine(row[1], row[2])
                magazine.id = row[0]
                return magazine
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def articles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, title FROM articles WHERE magazine_id = ?', (self.id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def contributors(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT authors.* FROM authors '
                           'JOIN articles ON authors.id = articles.author_id '
                           'WHERE articles.magazine_id = ?', (self.id,))
            authors_data = cursor.fetchall()
            return [Author(*data) for data in authors_data]
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()
