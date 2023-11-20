import streamlit as st
import mysql.connector

# pip install mysql-connector-python

def open_conn(input_user, input_password):
    conn2 = mysql.connector.connect(
        host="localhost", user="root", password="pacienc1@", database="farmacia"
    )
    cursor2 = conn2.cursor()
    cursor2.execute(f"SELECT COUNT(*) FROM mysql.user WHERE user = '{input_user}'")
    user_exists = cursor2.fetchone()[0]
    if not user_exists:
        cursor2.execute(
            f"CREATE USER '{input_user}'@'localhost' IDENTIFIED BY '{input_password}';"
        )
        cursor2.execute(f"GRANT ALL PRIVILEGES ON * . * TO '{input_user}'@'localhost';")
        cursor2.execute(f"FLUSH PRIVILEGES;")

    conn = mysql.connector.connect(
        host="localhost",
        user=input_user,
        password=input_password,
        database="farmacia",
    )

    cursor = conn.cursor()
    return conn, cursor

def insert_data(conn, cursor, table, data):
    if table == "Venda":
        query = f"INSERT INTO {table} (fk_cliente, fk_func, data_venda) VALUES ({', '.join(['%s']*len(data))}) "
    elif table == "Produto":
        query = f"INSERT INTO {table} (preco, nome, tipo, descricao, marca) VALUES ({', '.join(['%s']*len(data))}) "
    else:
        query = f"INSERT INTO {table} VALUES ({', '.join(['%s']*len(data))})"
    cursor.execute(query, data)
    conn.commit()
    st.success(f"Dados inseridos em {table}.")

def delete_data(conn, cursor, table, condition_column, condition_value):
    query = f"DELETE FROM {table} WHERE {condition_column} = %s"
    cursor.execute(query, (condition_value,))
    conn.commit()
    st.success(f"Dados deletados de {table}.")

def update_data(conn, cursor, table, set_column, set_value, condition_column, condition_value):
    query = f"UPDATE {table} SET {set_column} = %s WHERE {condition_column} = %s"
    cursor.execute(query, (set_value, condition_value))
    conn.commit()
    st.success(f"Dados atualizados em {table}.")

#def select_table(conn, cursor, table):
#    query = f"SELECT * FROM {table}"
#    cursor.execute(query)
#    data = cursor.fetchall()
#    return data

def select_table(conn, cursor, table, filter_column=None, input=None):
    if filter_column and input:
        if table == "Venda" and filter_column in ["valor", "cod_nota_fiscal"]:
            query = f"SELECT * FROM {table} WHERE {filter_column} = {input};"
        elif table == "Venda" and filter_column == "fk_prod":
            query = f"SELECT v.* FROM venda v JOIN produto_venda pv ON v.cod_nota_fiscal = pv.fk_venda WHERE pv.fk_prod = {input};"
        elif table == "Funcionario" and filter_column == "turno":
            query = f"SELECT f.*, b.turno FROM funcionario f JOIN balconista b ON f.cpf_func = b.cpf_balconista WHERE b.turno = '{input}';"
        elif table == "FUncionario" and filter_column == "crf":
            query = f"SELECT f.*, p.crf FROM funcionario f JOIN farmaceutico p ON f.cpf_func = p.cpf_farm WHERE p.crf = '{input}';"
        else: 
            query = f"SELECT * FROM {table} WHERE {filter_column} LIKE '%{input}%';"
    else:
        query = f"SELECT * FROM {table};"

    cursor.execute(query)
    result = cursor.fetchall()
    return result
    
def get_cod_nota(conn, cursor, cliente_venda, funcionario_venda, data_venda):
    query = f"SELECT cod_nota_fiscal FROM venda WHERE fk_cliente = '{cliente_venda}' AND fk_func = '{funcionario_venda}' AND data_venda = '{data_venda}';"
    cursor.execute(query)
    data = cursor.fetchall()
    return data[-1][0]

def close_conn(conn, cursor):
    cursor.close()
    conn.close()
