import sqlite3

# Conectarse a la base de datos
conexion = sqlite3.connect("database/biotrack_v2.db")

cursor = conexion.cursor()

# Mostrar todas las tablas
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

tablas = cursor.fetchall()

print("Tablas encontradas:\n")

for tabla in tablas:
    print("-", tabla[0])

conexion.close()