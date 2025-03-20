import sqlite3
import os

# Conectar a la base de datos
db_path = os.path.join(os.getcwd(), 'database', 'encspa.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Obtener lista de tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\nTablas en la base de datos:")
for table in tables:
    print(f"- {table[0]}")

# Contar registros en cada tabla
print("\nConteo de registros por tabla:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM '{table[0]}';")
    count = cursor.fetchone()[0]
    print(f"- {table[0]}: {count} registros")

# Examinar estructura de algunas tablas clave
key_tables = ['personas', 'alcohol', 'tabaco', 'marihuana', 'cocaina', 'heroína', 'extasis', 'encuestas']
print("\nEstructura de tablas clave:")
for table in key_tables:
    if (table,) in tables:
        cursor.execute(f"PRAGMA table_info('{table}');")
        columns = cursor.fetchall()
        print(f"\nTabla: {table}")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

# Cerrar conexión
conn.close()