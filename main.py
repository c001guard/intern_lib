import datetime

import db
import menu

def check_empty(items, message):
    if len(items) == 0:
        print(message)
        return True
    return False

def resolve_author():
    name = input("Введите имя автора: ").strip()

    if name == "":
        print("Ошибка: имя автора не может быть пустым.")
        return None

    author = db.find_author_by_name(name)

    if author is not None:
        return author[0]

    answer = input("Автор не найденю Добавить нового автора? (да/нет): ").strip()

    if answer != "да":
        print("Добавление книги отменено.")
        return None

    country = input("Введите страну автора: ").strip()
    author_id = db.add_author(name, country if country != "" else None)
    print("автор успешно добавлен.")
    return author_id

def add_author_action():
    name = input("Введите имя автора: ").strip()
    country = input("Введите страну автора: ").strip()

    if name == "":
        print("Ошибка: имя автора не может быть пустым.")
        return

    db.add_author(name, country if country != "" else None)
    print("Автор успешно добавлен.")

def show_authors_action():
    authors = db.get_authors()

    if check_empty(authors, "Список авторов пуст."):
        return

    for author in authors:
        author_id, name, country = author
        print(str(author_id) + ". " + name + " (" + (country or "-") + ")")

def add_book_action():
    title = input("Введите название книги: ").strip()
    year_input = input ("Введите год выпуска книги:").strip()
    current_year = datetime.date.today().year

    if title == "":
        print("Ошибка: название книги не может быть пустым.")
        return

    year = int(year_input)

    if year < 1500 or year > current_year:
        print("Ошибка: год должен быть от 1500 до " + str(current_year) + ".")
        return

    author_id = resolve_author()

    if author_id is None:
        return

    if db.is_book_duplicate(title, year, author_id):
        print("Такая книга уже есть в библиотеке.")
        return

    db.add_book(title, year, author_id)
    print("книга успешн добавлена.")

def show_books_action():
    books = db.get_books()

    if check_empty(books, "Библиотека пуста."):
        return

    for book in books:
        book_id, title, author_name, year = book
        print(str(book_id) + ". " + title + " - " + author_name + " (" + str(year) + ")")

def find_book_action():
    books = db.get_books()

    if check_empty(books, "Библиотека пуста."):
        return

    part = input("Введите часть названия книги: ").strip()
    results = db.find_books(part)

    if len(results) == 0:
        print("Книга не найдена.")
        return

    for book in results:
        book_id, title, author_name, year = book
        print(str(book_id)+ ". " + title + " - " + author_name + " (" + str(year)+ ")")

def delete_book_action():
    number_input = input("Введите номер книги для удаления: ").strip()

    if not number_input.isdigit():
        print("Неверный номер книги.")
        return

    result = db.delete_book(int(number_input))

    if result == "deleted":
        print("Книга удалена.")
    elif result == "has_loans":
        print("Нельзя удалить книгу: по ней есть история выдач.")
    else:
        print("Неверный номер книги.")

def show_library_statistics_action():
    total, oldest, newest, total_authors = db.book_statistics()

    if total == 0:
        print("Библиотека пуста.")
        return

    print("Всего книг:", total)
    print("Всего авторов", total_authors)
    print("Самая старая книга:", oldest)
    print("Сама новая книга:", newest)

def add_reader_action():
    name = input("Введите имя читателя: ").strip()
    city = input("Введите город читателя: ").strip()

    if name == "":
        print("Ошибка: имя читателя не может быть пустым.")
        return

    db.add_reader(name, city if city != "" else None)
    print("Читатель успешно добавлен.")

def show_readers_action():
    readers = db.get_readers()

    if check_empty(readers, "Список читателей пуст."):
        return

    for reader in readers:
        reader_id, name, city = reader
        print(str(reader_id) + ". " + name + " (" + (city or "-") + ")")

def delete_reader_action():
    readers = db.get_readers()

    if check_empty(readers, "Список читателей пуст."):
        return

    show_readers_action()
    number_input = input("Введите номер читателя для удаления: ").strip()

    if not number_input.isdigit():
        print("неверный номер читателя.")
        return

    result = db.delete_reader(int(number_input))

    if result == "deleted":
        print("Читатель удален.")
    elif result == "has_loans":
        print("Нельзя удалить читателя: у него есть история выдач.")
    else:
        print("неверный номер читателя.")

def issue_book_action():
    books = db.get_books()

    if check_empty(books, "Библиотека пуста."):
        return

    readers = db.get_readers()

    if check_empty(readers, "Список читателей пуст"):
        return

    show_books_action()
    book_input = input("Введите номер книги для выдачи: ").strip()

    if not book_input.isdigit() or not db.book_exists(int(book_input)):
        print("Неверный номер книги.")
        return

    book_id = int(book_input)

    if db.is_book_issued(book_id):
        print("Эта книга уже выдана и еще не возвращена.")
        return

    show_readers_action()
    reader_input = input("Введите номер читателя: ").strip()

    if not reader_input.isdigit() or not db.reader_exists(int(reader_input)):
        print("Неверный номер читателя.")
        return

    db.issue_book(book_id, int(reader_input))
    print("Книга успешно выдана")

def return_book_action():
    book_input = input("Введите номер книги для возврата: ")

    if not book_input.isdigit():
        print("Неверный номер книги.")
        return

    if db.return_book(int(book_input)):
        print("Книга успешно возвращена.")
    else:
        print("У этой книги нет активной выдачи.")

def show_reader_statistics_action():
    total_readers, active_loans, total_loans = db.reader_statistics()

    if total_readers == 0:
        print("Список читателей пуст.")
        return

    print("Всего читателей:", total_readers)
    print("Книг на руках:", active_loans)
    print("Всего выдач за все время:", total_loans)

def library_menu_loop():
    choice = -1

    while choice != 0:
        menu.authors_menu()
        choice_input = input("Выберите пункт меню: ").strip()

        if not choice_input.isdigit():
            print("неверный ввод. Попробуйте снова.")
            continue

        choice = int(choice_input)

        if choice == 1:
            add_author_action()
        elif choice == 2:
            show_authors_action()
        elif choice == 3:
            add_book_action()
        elif choice == 4:
            show_books_action()
        elif choice == 5:
            find_book_action()
        elif choice == 6:
            delete_book_action()
        elif choice == 7:
            show_library_statistics_action()
        elif choice == 0:
            pass
        else:
            print("Неверный пункт меню. Попробуйте снова.")

def readers_menu_loop():
    choice = -1

    while choice != 0:
        menu.readers_menu()
        choice_input = input("Выберите пункт меню: ").strip()

        if not choice_input.isdigit():
            print("Неверный ввод. Попробуйте снова.")
            continue

        choice = int(choice_input)

        if choice == 1:
            add_reader_action()
        elif choice == 2:
            show_readers_action()
        elif choice == 3:
            delete_reader_action()
        elif choice == 4:
            issue_book_action()
        elif choice == 5:
            return_book_action()
        elif choice == 6:
            show_reader_statistics_action()
        elif choice == 0:
            pass
        else:
            print("Неверный пункт меню. Попробуйте снова.")

def main():
    db.connect()

    try:
        choice = -1

        while choice != 0:
            menu.main_menu()
            choice_input = input("Выберите пункт меню: ").strip()

            if not choice_input.isdigit():
                print("Неверный ввод. Попробуйте снова.")
                continue

            choice = int(choice_input)

            if choice == 1:
                library_menu_loop()
            elif choice == 2:
                readers_menu_loop()
            elif choice == 0:
                print("До свидания.")
            else:
                print("Неверный пункт меню. Попробуйте снова.")

    finally:
        db.close()

if __name__ == "__main__":
    main()
