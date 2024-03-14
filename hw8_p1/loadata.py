import json
from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних MongoDB
connect('celebrities', host='mongodb+srv://vrokmoitcattus:owtXMbGQIFr2444j@hw8.3qphtkz.mongodb.net/celebrities?retryWrites=true&w=majority')

# Функція для завантаження даних з JSON файлів
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

# Функція для завантаження авторів
def load_authors():
    authors_data = load_data_from_json('authors.json')
    for author_data in authors_data:
        author = Author(**author_data)
        author.save()

# Функція для завантаження цитат
def load_quotes():
    quotes_data = load_data_from_json('quotes.json')
    for quote_data in quotes_data:
        author_name = quote_data.pop('author')  # Видаляємо поле з ім'ям автора
        author = Author.objects(fullname=author_name).first()  # Знаходимо автора за ім'ям
        if author:
            quote_data['author'] = author  # Замінюємо рядкове значення ім'ям автора на посилання на об'єкт автора
            quote = Quote(**quote_data)
            quote.save()

# Завантаження даних
load_authors()
load_quotes()

print("Дані завантажено успішно!")
