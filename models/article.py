from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, author, magazine, title, content):
        self.author_id = author.id
        self.magazine_id = magazine.id
        self.title = title
        self.content = content
        self._id = None
        self._create_in_db()

    def _create_in_db(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO articles (author_id, magazine_id, title, content) VALUES (?, ?, ?, ?)', 
                           (self.author_id, self.magazine_id, self.title, self.content))
            conn.commit()
            self._id = cursor.lastrowid
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
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
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError("Content must be a string")
        self._content = value

    @property
    def author(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
            author_data = cursor.fetchone()
            return Author(*author_data) if author_data else None
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    @property
    def magazine(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
            magazine_data = cursor.fetchone()
            return Magazine(*magazine_data) if magazine_data else None
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        articles = []
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM articles')
            article_rows = cursor.fetchall()
            for row in article_rows:
                author = Author.get_by_id(row[1])
                magazine = Magazine.get_by_id(row[2])
                article = Article(author, magazine, row[3], row[4])
                article.id = row[0]
                articles.append(article)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
        return articles
