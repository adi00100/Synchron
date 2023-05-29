from django.db import connection

cursor = connection.cursor()
roles = cursor.execute("SELECT * FROM Roles")
roles = cursor.fetchall()
roles = {}

for id, name in roles:
    roles[id] = name
