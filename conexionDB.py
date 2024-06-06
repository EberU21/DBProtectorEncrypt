import mysql.connector
from mysql.connector import Error
from tkinter import filedialog, messagebox, ttk


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="integradora.mysql.database.azure.com",
            user="User",
            password="Abcd1234",
            database="steamgamesintegradora"
        )
        return connection
    except Error as e:
        raise Exception(f"No se pudo conectar a la base de datos: {e}")

def fetch_table_data(connection, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        raise Exception(f"No se pudo recuperar los datos de la tabla {table_name}: {e}")

def fetch_table_names(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        return tables
    except Error as e:
        raise Exception(f"No se pudieron obtener los nombres de las tablas: {e}")


def fetch_table_columns(connection, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [column[0] for column in cursor.fetchall()]
        return columns
    except Error as e:
        raise Exception(f"No se pudieron obtener los nombres de las columnas de la tabla: {e}")

def display_table_data(connection, table_name, tree):
    table_data = fetch_table_data(connection, table_name)
    table_columns = fetch_table_columns(connection, table_name)

    for row in tree.get_children():
        tree.delete(row)

    for col in table_columns:
        tree.heading(col, text=col)
        
    for row in table_data:
        tree.insert("", "end", values=row)
        

def actualizar_datosBD(tabla, nombre, encriptado, col):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        sql = f"UPDATE {tabla} SET {col} = %s WHERE {col} = %s"
        cursor.execute(sql, (encriptado, nombre))
        connection.commit()
        messagebox.showinfo("Base de Datos Actualizada", "El dato encriptado ha sido actualizado en la base de datos.")
    except Error as e:
        messagebox.showerror("Error", f"No se pudo actualizar la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

