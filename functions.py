import streamlit as st
import pandas as pd
import mysql.connector

#conexão com o banco
def open_conn(input_user, input_password):
    global conn
    conn = mysql.connector.connect(
    host="localhost",
    user= input_user,
    password= input_password, 
    database="UNIVERSIDADE"
)
    global cursor 
    cursor = conn.cursor()
    

#insert
def insert_data(table, data):
    query = f"INSERT INTO {table} VALUES ({', '.join(['%s']*len(data))})"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Dados inseridos em {table}.')

#delete
def delete_data(table, condition_column, condition_value):
    query = f"DELETE FROM {table} WHERE {condition_column} = %s"
    cursor.execute(query, (condition_value,))
    conn.commit()
    st.success(f'Dados deletados de {table}.')

#update
def update_data(table, set_column, set_value, condition_column, condition_value):
    query = f"UPDATE {table} SET {set_column} = %s WHERE {condition_column} = %s"
    cursor.execute(query, (set_value, condition_value))
    conn.commit()
    st.success(f'Dados atualizados em {table}.')

#select
#def select_data(table, data):
    #query = f"SELECT * FROM {table}"           
    #cursor.execute(query)
    #data = cursor.fetchall()
    #return data

def select_data(data):
    query = f"SELECT total_creditos({data});"
    cursor.execute(query)
    query_result = cursor.fetchone()
    valor = query_result[0]
    return valor

#fechar conexão
def close_conn():
    cursor.close()
    conn.close()
