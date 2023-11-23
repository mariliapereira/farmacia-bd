import streamlit as st
import mysql.connector
# pip install mysql-connector-python

def open_conn(input_user, input_password):
    conn = mysql.connector.connect(
        host="localhost", user=input_user, password=input_password, database="farmacia"
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
    query = f"DELETE FROM {table} WHERE {condition_column} = {condition_value}"
    cursor.execute(query)
    conn.commit()
    st.success(f"Dados deletados de {table}.")

def update_data(conn, cursor, table, set_column, set_value, condition_column, condition_value):
    query = f"UPDATE {table} SET {set_column} = '{set_value}' WHERE {condition_column} = '{condition_value}'"
    cursor.execute(query)
    conn.commit()
    st.success(f"Dados atualizados em {table}.")

def select_table(conn, cursor, table, filter_column=None, input=None):
    if filter_column and input:
        if table == "Venda" and filter_column in ["valor", "cod_nota_fiscal"]:
            query = f"SELECT * FROM {table} WHERE {filter_column} = {input};"
        elif table == "Venda" and filter_column == "cod_prod":
            query = f"SELECT v.* FROM venda v JOIN produto_venda pv ON v.cod_nota_fiscal = pv.fk_venda WHERE pv.fk_prod = {input};"
        elif table == "Funcionario" and filter_column == "turno":
            query = f"SELECT f.* FROM funcionario f JOIN balconista b ON f.cpf_func = b.cpf_balconista WHERE b.turno = '{input}';"
        elif table == "Funcionario" and filter_column == "crf":
            query = f"SELECT f.* FROM funcionario f JOIN farmaceutico fm ON f.cpf_func = fm.cpf_farm WHERE fm.crf = '{input}';"
        else: 
            query = f"SELECT * FROM {table} WHERE {filter_column} LIKE '%{input}%';"
    else:
        query = f"SELECT * FROM {table};"

    cursor.execute(query)
    result = cursor.fetchall()
    return result
    
def funcionario_do_mes(conn, cursor, input):
    query = f"SELECT f.nome, COUNT(*) as vendas FROM funcionario f JOIN venda v ON f.cpf_func = v.fk_func WHERE MONTH(v.data_venda) = {input} \
                GROUP BY f.cpf_func HAVING COUNT(*) = ( \
                    SELECT MAX(total_vendas) \
                    FROM (SELECT COUNT(*) as total_vendas FROM funcionario f_sub JOIN venda v_sub ON f_sub.cpf_func = v_sub.fk_func \
                    WHERE MONTH(v_sub.data_venda) = {input} GROUP BY f_sub.cpf_func) AS subquery);"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def produto_mais_vendido_mes(conn, cursor, input):
    query = f"SELECT p.nome as nome_produto, SUM(pv.quantidade) as total_quantidade_vendida FROM produto p \
                JOIN produto_venda pv ON p.cod_prod = pv.fk_prod JOIN venda v ON pv.fk_venda = v.cod_nota_fiscal \
                WHERE MONTH(v.data_venda) = {input} GROUP BY p.cod_prod, p.nome HAVING SUM(pv.quantidade) = ( \
                    SELECT MAX(total_quantidade) \
                    FROM (SELECT SUM(pv_sub.quantidade) as total_quantidade \
                    FROM produto_venda pv_sub \
                    JOIN venda v_sub ON pv_sub.fk_venda = v_sub.cod_nota_fiscal \
                    WHERE MONTH(v_sub.data_venda) = {input} \
                    GROUP BY pv_sub.fk_prod \
                    ) AS subquery \
                )"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def produto_mais_comprado_pelo_cliente(conn, cursor, input):
    query = f"SELECT pv.fk_prod AS codigo_produto, p.nome AS nome_produto, SUM(pv.quantidade) AS total_quantidade_comprada \
                FROM produto_venda pv JOIN venda v ON pv.fk_venda = v.cod_nota_fiscal JOIN produto p ON pv.fk_prod = p.cod_prod \
                JOIN cliente c ON v.fk_cliente = c.cpf_cliente WHERE c.nome  = '{input}' GROUP BY pv.fk_prod, p.nome \
                HAVING SUM(pv.quantidade) = (SELECT MAX(total_quantidade) FROM (SELECT SUM(pv_sub.quantidade) AS total_quantidade \
                FROM produto_venda pv_sub JOIN venda v_sub ON pv_sub.fk_venda = v_sub.cod_nota_fiscal \
                JOIN cliente c_sub ON v_sub.fk_cliente = c_sub.cpf_cliente WHERE c_sub.nome  = '{input}' \
                GROUP BY pv_sub.fk_prod) AS subquery)"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def arrecadamento_mensal(conn, cursor, input):
    query = f"SELECT SUM(valor) AS total_vendas FROM venda WHERE MONTH(data_venda) = {input};"
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
