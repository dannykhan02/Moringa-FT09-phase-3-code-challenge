from models.author import Author
from models.magazine import Magazine
from models.article import Article

def register_author():
    name = input("Enter author name: ")
    author = Author(name)
    print(f"Author '{name}' added with ID {author.id}")

def register_magazine():
    name = input("Enter magazine name: ")
    category = input("Enter magazine category: ")
    magazine = Magazine(name, category)
    print(f"Magazine '{name}' added with ID {magazine.id}")

def create_article():
    author_id = int(input("Enter author ID: "))
    magazine_id = int(input("Enter magazine ID: "))
    title = input("Enter article title: ")

    author = Author.get_by_id(author_id)
    magazine = Magazine.get_by_id(magazine_id)

    if not author:
        print(f"Author with ID {author_id} not found.")
        return
    if not magazine:
        print(f"Magazine with ID {magazine_id} not found.")
        return

    try:
        article = Article(author, magazine, title, "")  # Pass empty content
        print(f"Article '{title}' added with ID {article.id}")
    except ValueError as e:
        print(e)

def find_articles_by_author():
    author_id = int(input("Enter author ID: "))
    author = Author.get_by_id(author_id)

    if not author:
        print(f"Author with ID {author_id} not found.")
        return

    articles = author.articles()

    if articles:
        print(f"Articles by author ID {author_id}:")
        for article in articles:
            print(f"- {article.title}")
    else:
        print(f"No articles found for author ID {author_id}.")

def find_articles_by_magazine():
    magazine_id = int(input("Enter magazine ID: "))
    magazine = Magazine.get_by_id(magazine_id)

    if not magazine:
        print(f"Magazine with ID {magazine_id} not found.")
        return

    articles = magazine.articles()

    if articles:
        print(f"Articles in magazine ID {magazine_id}:")
        for article in articles:
            print(f"- {article.title}")
    else:
        print(f"No articles found for magazine ID {magazine_id}.")

def find_contributors_to_magazine():
    magazine_id = int(input("Enter magazine ID: "))
    magazine = Magazine.get_by_id(magazine_id)

    if not magazine:
        print(f"Magazine with ID {magazine_id} not found.")
        return

    contributors = magazine.contributors()

    if contributors:
        print(f"Contributors to magazine ID {magazine_id}:")
        for contributor in contributors:
            print(f"- {contributor.name}")
    else:
        print(f"No contributors found for magazine ID {magazine_id}.")

def main():
    while True:
        print("Please select an option:")
        print("1. Register a new Author")
        print("2. Register a new Magazine")
        print("3. Create a new Article")
        print("4. Find Articles by Author")
        print("5. Find Articles by Magazine")
        print("6. Find Contributors to a Magazine")
        print("7. Exit the Program")
        choice = input("Your choice: ")

        if choice == '1':
            register_author()
        elif choice == '2':
            register_magazine()
        elif choice == '3':
            create_article()
        elif choice == '4':
            find_articles_by_author()
        elif choice == '5':
            find_articles_by_magazine()
        elif choice == '6':
            find_contributors_to_magazine()
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
