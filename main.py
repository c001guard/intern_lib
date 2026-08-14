books = []


def show_menu():
    print("=" * 25)
    print("            BOOK MANAGER")
    print("=" * 25)
    print("\n1.  Добавить книгу")
    print("2. Показать все книги")
    print("3. Найти книгу")
    print("4. Удалить книгу")
    print("5. Статистика")
    print("0. Выход")

def add_book()
    title = input("Введите название книги: ").strip()
    author = input("Введите автора книги: ").strip()
    year_input = input("Введите год выпуска: ")
    current_year = 2026

    if not year_input.isdigit():
        print("Ошибка: год должен быть числом.")
        return
    year = int(year_input)

    if title != "" and author!+ "" and year >= 1500 and year <= current_year:
        books.append({"title": title, "author": author, "year": year})
        print("Книга успешно добалена.")
    else:
        print("Ошибка: проверьте название, автора и год выпуска книги.")


def show_books():
    if len(books) == 0:
        print("Бибилиотека пуста.")
        return

    for i in range(len(books)):
        book = books[i]
        print(str(i + 1) + ". " + book["title"] + " - " + book["author"] + " (" + str(book["year"]) + ")")

def find_book():
    if len(books) == 0:
        print("Библиотека пуста.")
        return

    part = input("Введите часть названия книги: ").strip().lower()
    found = False

    for i in range (len(books)):
        book = books[i]
        if part in book["title"].lower():
            print(str(i + 1) + ". " + book["title"] + " - " + book["author"] + " (" + str(book["year"]) + ")")
            found = True

    if not found:
        print("Книга не найдена. ")