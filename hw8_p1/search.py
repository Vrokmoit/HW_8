from mongoengine import connect
from models import Quote, Author

# Підключення до бази даних
connection_string = "mongodb+srv://vrokmoitcattus:owtXMbGQIFr2444j@hw8.3qphtkz.mongodb.net/celebrities?retryWrites=true&w=majority"
connect(host=connection_string, ssl=True)

def search_quotes(params):
    if 'name' in params:
        author_name = params['name']
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print(f"No quotes found for author {author_name}")
    elif 'tag' in params:
        tag_name = params['tag']
        quotes = Quote.objects(tags=tag_name)
        if quotes:
            for quote in quotes:
                print(quote.quote)
        else:
            print(f"No quotes found for tag {tag_name}")
    elif 'tags' in params:
        tags = params['tags'].split(',')
        quotes = Quote.objects(tags__in=tags)
        if quotes:
            for quote in quotes:
                print(quote.quote)
        else:
            print(f"No quotes found for tags {', '.join(tags)}")
    else:
        print("Невідома команда. Спробуйте ще раз.")

while True:
    command = input("Введіть команду (наприклад, 'tag:life', 'name:Steve Martin', 'tags:life,live', або 'exit'): ")
    if command == 'exit':
        print("Завершення роботи програми.")
        break
    else:
        command_type, value = command.split(':')
        if command_type == 'name':
            search_quotes({'name': value.strip()})
        elif command_type == 'tag':
            search_quotes({'tag': value.strip()})
        elif command_type == 'tags':
            search_quotes({'tags': value.strip()})
        else:
            print("Невідома команда. Спробуйте ще раз.")
