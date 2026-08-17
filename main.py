books = []
next_number = 1

def is_dublicate(title, author, year):
    for book in books:
        if book["title"].lower() == title.lower() and book["author"].lower() == author.lower() and book["year"] == year:
            return True
    return False

def check_books():
    if len(books) == 0:
        print("Библиотека пуста.")
        return True
    return False


def show_menu():
    print("=" * 25)
    print("      BOOK MANAGER")
    print("=" * 25)
    print("\n1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Найти книгу")
    print("4. Удалить книгу")
    print("5. Статистика")
    print("0. Выход")

def add_book():
    global next_number
    title = input("Введите название книги: ").strip()
    author = input("Введите автора книги: ").strip()
    year_input = input("Введите год выпуска: ")
    current_year = 2026

    if not year_input.isdigit():
        print("Ошибка: год должен быть числом.")
        return
    year = int(year_input)

    if title != "" and author != "" and year >= 1500 and year <= current_year:
        if is_dublicate(title, author, year):
            print("Такая книга уже есть в библиотеке.")
        else:
            books.append({"id": next_number, "title": title, "author": author, "year": year})
            next_number += 1
            print("Книга успешно добавлена.")
    else:
        print("Ошибка: проверьте название, автора и год выпуска книги.")


def show_books():
    if check_books():
        return

    for id in range(len(books)):
        book = books[id]
        print(str(book["id"]) + ". " + book["title"] + " - " + book["author"] + " (" + str(book["year"]) + ")")

def find_book():
    if check_books():
        return

    part = input("Введите часть названия книги: ").strip().lower()
    found = False

    for id in range (len(books)):
        book = books[id]
        if part in book["title"].lower():
            print(str(book["id"]) + ". " + book["title"] + " - " + book["author"] + " (" + str(book["year"]) + ")")
            found = True

    if not found:
        print("Книга не найдена.")

def delete_book():
    if check_books():
        return
    show_books()
    number_input = input("Введите номер книги для удаления: ").strip()

    if not number_input.isdigit():
        print("Неверный номер книги.")
        return

    number = int(number_input)

    for id in range(len(books)):
        if books[id]["id"] == number:
            removed = books.pop(id)
            print("Книга \"" + removed["title"] + "\" удалена.")
            return
    print("Неверный номер книги.")

def show_statistics():
    if check_books():
        return
    total = len(books)
    oldest_year = books[0]["year"]
    newest_year = books[0]["year"]

    for id in range(len(books)):
        year = books[id]["year"]
        if year < oldest_year:
            oldest_year = year
        if year > newest_year:
            newest_year = year

    print("Всего книг:", total)
    print("Самая старая книга:", oldest_year)
    print("Самая новая книга:", newest_year)

def main():
    choice = -1

    while choice !=0:
        show_menu()
        choice_input = input("Выберите пункт меню: ").strip()

        if not choice_input.isdigit():
            print("Неверный ввод. Попробуйте снова.")
            continue

        choice = int(choice_input)

        if choice == 1:
            add_book()
        elif choice == 2:
            show_books()
        elif choice == 3:
            find_book()
        elif choice == 4:
            delete_book()
        elif choice == 5:
            show_statistics()
        elif choice == 0:
            print("До свидания")
        else:
            print("Неверный пункт меню. Попробуйте снова.")

if __name__=="__main__":
    main()