import streamlit as st
import mysql.connector

# pip install mysql-connector-python


# conexão com o banco
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

# insert
def insert_data(conn, cursor, table, data):
    print(f'data --> {data}')
    if table == "Venda":
        query = f"INSERT INTO {table} (fk_cliente, fk_func, data_venda) VALUES ({', '.join(['%s']*len(data))}) "
    elif table == "Produto":
        query = f"INSERT INTO {table} (preco, nome, tipo, descricao, marca) VALUES ({', '.join(['%s']*len(data))}) "
    else:
        query = f"INSERT INTO {table} VALUES ({', '.join(['%s']*len(data))})"
    cursor.execute(query, data)
    conn.commit()
    st.success(f"Dados inseridos em {table}.")

# delete
def delete_data(conn, cursor, table, condition_column, condition_value):
    query = f"DELETE FROM {table} WHERE {condition_column} = %s"
    cursor.execute(query, (condition_value,))
    conn.commit()
    st.success(f"Dados deletados de {table}.")


# update
def update_data(conn, cursor, table, set_column, set_value, condition_column, condition_value):
    query = f"UPDATE {table} SET {set_column} = %s WHERE {condition_column} = %s"
    cursor.execute(query, (set_value, condition_value))
    conn.commit()
    st.success(f"Dados atualizados em {table}.")


# select
def select_table(conn, cursor, table):
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    data = cursor.fetchall()
    return data


#def select_data(conn, cursor, data):
#    query = f"SELECT total_creditos({data});"
#    cursor.execute(query)
#    query_result = cursor.fetchone()
#    valor = query_result[0]
#    return valor

def select_venda_data(conn, cursor, data):
    query = f"SELECT * FROM venda WHERE data_venda = '{data}';"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def select_preco_venda(conn, cursor, data):
    query = f"SELECT valor FROM venda WHERE cod_venda = '{data}';"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def select_balc_turno(conn, cursor, data):
    query = f"SELECT b.cpf_balconista, f.nome FROM balconista b JOIN funcionario f ON b.cpf_balconista = f.cpf_func WHERE b.turno = '{data}';"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def select_func_venda(conn, cursor, data):
    query = f"SELECT v.cpf_func, f.nome FROM venda v JOIN funcionario f ON v.cpf_func = f.cpf_func WHERE cod_venda = '{data}';"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def select_prod_marca(conn, cursor, data):
    query = f"SELECT * FROM produto WHERE p.marca = '{data}';"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# fazer uns select mais complicados! usar join!!! algum procedure ou função?
# função tipo qual o valor total que um cliente x já gastou? pegar todas as ocorrências do mesmo cliente em venda por exemplo e sair somando o valor?
# usar coisa tipo max min avg not null like etc

def get_cod_nota(conn, cursor, cliente_venda, funcionario_venda, data_venda):
    query = f"SELECT cod_nota_fiscal FROM venda WHERE fk_cliente = '{cliente_venda}' AND fk_func = '{funcionario_venda}' AND data_venda = '{data_venda}';"
    cursor.execute(query)
    data = cursor.fetchall()
    return data[-1][0]

# fechar conexão
def close_conn(conn, cursor):
    cursor.close()
    conn.close()
