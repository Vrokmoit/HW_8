from mongoengine import connect
import configparser

def connect_to_mongodb():
    try:
        # Читаємо конфігураційний файл
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Отримуємо дані для підключення до бази даних з конфігураційного файлу
        mongo_user = config.get('DB', 'user')
        mongodb_pass = config.get('DB', 'pass')
        db_name = config.get('DB', 'db_name')
        domain = config.get('DB', 'domain')

        # Підключаємося до бази даних MongoDB Atlas за допомогою з'єднання з рядком підключення
        connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority", ssl=True)

        print("Connected to MongoDB Atlas")
    except Exception as e:
        print("Failed to connect to MongoDB Atlas:", e)

# Викликаємо функцію для підключення до бази даних
connect_to_mongodb()
