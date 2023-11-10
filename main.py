import streamlit as st  
import pandas as pd
from functions import *
# pip install mysql-connector-python

# rodar com:  
# streamlit run "c:/Users/heyda/OneDrive/Documentos/GitHub/farmacia-bd/main.py"

def main_page():
    st.title("Aplicação de Gerenciamento de Dados")
    operation = st.sidebar.selectbox("Selecione a operação", ("Inserir", "Deletar", "Atualizar", "Select"))
    table = st.sidebar.selectbox("Selecione a tabela", ("curso", "projeto", "pessoa", "professor", "disciplina", "turma", "ministra", "aluno", "aluno_turma", "prova", "monitoria", "busca - créditos totais"))

    if operation == "Inserir":
        if table == "curso":
            codigo_curso = st.number_input("Código do Curso", min_value=0)
            nome_curso = st.text_input("Nome do Curso")
            if st.button("Inserir"):
                insert_data(table, (codigo_curso, nome_curso))
    elif operation == "Deletar":
        if table == "curso":
            codigo_curso = st.number_input("Código do Curso a ser deletado", min_value=0)
            if st.button("Deletar"):
                delete_data(table, "codigo_curso", codigo_curso)
    elif operation == "Atualizar":
        if table == "curso":
            codigo_curso = st.number_input("Código do Curso a ser atualizado", min_value=0)
            novo_nome = st.text_input("Novo Nome do Curso")
            if st.button("Atualizar"):
                update_data(table, "nome", novo_nome, "codigo_curso", codigo_curso)
    elif operation == 'Select':
        if table == "curso":
            data = select_data(table)
            st.write("Dados da tabela Curso:")
            df = pd.DataFrame(data, columns=["Código do Curso", "Nome do Curso"])
            st.dataframe(df.set_index('Código do Curso'), width=800)
        if table == 'aluno':
            data = select_data(table)
            st.write("Dados da tabela Aluno:")
            df = pd.DataFrame(data, columns=["Matrícula do aluno", "Nota do vestibular", "Codigo do curso"])
            st.dataframe(df.set_index('Matrícula do aluno'), width=800)
        if table == 'busca - créditos totais':
            matricula_aluno = st.number_input("Matrícula do aluno", min_value=0)
            if st.button("Buscar"):
                result = select_data(matricula_aluno)
                st.write(f"Total de créditos do aluno: {result}")

if __name__ == '__main__':
    st.title("Login")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Login"):
        open_conn(user, password)
        main_page()
        close_conn()
