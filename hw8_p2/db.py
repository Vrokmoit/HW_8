from mongoengine import connect

# Підключення до бази даних
def connect_to_database():
    connect(
        db='contacts_database',
        username='vrokmoitcattus',
        password='owtXMbGQIFr2444j',
        host='hw8.3qphtkz.mongodb.net',
        port=27017,
        authentication_source='admin'
    )
