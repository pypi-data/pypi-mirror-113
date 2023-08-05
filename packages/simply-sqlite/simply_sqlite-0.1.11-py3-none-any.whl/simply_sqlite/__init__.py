'''
Author: Oscar Gutierrez
Email: o.guty66@gmail.com
Date: 2021-04-22
Python Version: 3.6.9
Version: 0.1.1
'''

# -*- coding: utf-8 -*-

# __LIBRARIES__ #
import sqlite3
from sqlite3 import Error

# __MAIN CODE__ #


class SQL:
    def __init__(self, name):
        self.db_name = name + '.db'
        self.create_connexion()
        self.cursorObj = self.conn.cursor()

    def create_connexion(self):  # crea la conexion a la BDD o la propia BDD
        self.conn = None  # creamos el objeto conect
        try:  # caso de omitir la ruta se crea en el directorio actual
            self.conn = sqlite3.connect(self.db_name)  # crea la BD en la ruta
        except Error as e:
            print(e)

    def find_tables(self):  # busca y almacena el nombre d ls tablas de la BDD
        self.table_names = list()
        self.cursorObj.execute(
            'SELECT name FROM sqlite_master WHERE type="table";')
        for name in self.cursorObj.fetchall():
            self.table_names.append(str(name)[2:-3])

    def create_table(self, name, p_key, typ):  # crea tablas nuevas en la BDD
        self.cursorObj.execute(
            'CREATE TABLE %s(%s %s PRIMARY KEY)' % (name, p_key, typ)
        )
        self.table_names.append(name)

    def insert_column(self, table, column, type):  # inserta columnas a la BDD
        self.cursorObj.execute(
            'ALTER TABLE %s ADD COLUMN %s %s' % (table, column, type)
        )
        self.commit()

    def insert_info(self, table, column, info):
        value = (info,)
        self.cursorObj.execute(
            'INSERT INTO %s(%s) VALUES(?)' % (table, column), value
        )
        self.commit()

    def update(self, table, column, key, info):
        self.cursorObj.execute(
            'UPDATE %s SET %s = ? WHERE %s = ?' % (table, column, key), info
        )  # UPDATE Replicas SET Modelo = val1 WHERE SN = val2
        self.commit()

    def show_all_rows(self, table):
        self.cursorObj.execute(
            'SELECT * FROM %s' % (table)
        )
        return self.cursorObj.fetchall()

    def show_one_row(self, table, column, info):
        ind = self.show_column_names(table).index(column)
        row = [elem for elem in self.show_all_rows(table) if info == elem[ind]]
        return row

    def show_column_names(self, table):
        point = self.cursorObj.execute('SELECT * FROM %s' % (table))
        names = [description[0] for description in point.description]
        return names

    def delete_row(self, table, column, info):
        value = (info,)
        self.cursorObj.execute(
            'DELETE FROM %s WHERE %s = ?' % (table, column), value
        )
        self.commit()

    def commit(self):
        self.conn.commit()


'''

    def list(self):

    def delete(self):
'''


def run():
    db = SQL('Mia')
    print(db.show_all_rows('Replicas'))


if __name__ == '__main__':
    run()

# __NOTES__ #
'''
    __init__(name):
        {name}  hace referencia a la variable que almacena el nombre de la base
                de datos.

    create_connexion():
        Crea la conexion con la base de datos.

    create_tables(name, p_key, typ):
        crea una tabla con una unica columna.
        {name}  hace referencia al nombre de la tabla a crear.
        {p_key} hace referencia al valor clave de la fila.
        {typ}   almacena el tipo de dato del valor clave.

    insert_column():
        Inserta columnas nuevas en la tabla establecida
        {table}  Nombre de la tabla
        {column} Nombre de la columna
        {type}   Establece el tipo de caracter almacenado en la columna.

    insert_info(self, table, column, info):
        Se emplea para insertar informacion en la tabla seleccionada
        en la columna establecida.
        {table}  Nombre de la tabla empleada
        {column} Columna en la que introducir la informacion
        {info}   infromacion a introdicir en la columna

    update(self, table, column, key, info):
        actualiza la infromacion en la columna especificada de una cierta tabla
        {table}  Nombre de la tabla empleada
        {column} nombre de la columna a actualizar
        {key}    Nombre de la columna que almacena el key
        {info}   Tupla con la siguiente estructura:
            (val, key)
                {val} Valor nuevo a introducir en la columna establecida
                {key} Key de la fila a modificar.

    show_column_names(self, table):
        Devuelve los nombres de las columnas de la tabla establecida.
        {table} Nombre de la tabla de la que se desea saber las columnas.

    show_all_rows(self, table):
        Devuelve toda la infromacion de una tabla dada.
        {table} Nombre de la tabla de la que se desea saber la informacion.

    show_one_row(self, table, column, info):
        Devuelve la informacion de la fila seleccionada
        {table}  Nombre de la tabla en la que buscar la infromacion
        {column} Nombre de la columna de referencia
        {info}   Infromacion a buscar en la columna.

    list_complete():
        nos permite ver toda la informacion en una base de datos
    delete():
        eliminara la informacion especificada.

'''
# __BIBLIOGRAPHY__ #
