
from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, author, magazine, title):
        self.author_id = author.id
        self.magazine_id = magazine.id
        self.title = title
        self.id = None
        self._create_in_db()

    def _create_in_db(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)', 
                           (self.author_id, self.magazine_id, self.title))
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value) < 5 or len(value) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters")
        self._title = value

    @property
    def author(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
            author = cursor.fetchone()
            return author
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    @property
    def magazine(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
            magazine = cursor.fetchone()
            return magazine
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_all():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM articles')
            articles = cursor.fetchall()
            return [Article(Author.get_by_id(row[1]), Magazine.get_by_id(row[2]), row[3]) for row in articles]
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
