import streamlit as st  
import pandas as pd
from functions import *

# rodar com:  
# streamlit run "c:/Users/heyda/OneDrive/Documentos/GitHub/farmacia-bd/main.py"

if __name__ == '__main__':
    if 'username' not in st.session_state:
        st.session_state.username = None
    if st.session_state.username == None:
        st.title("Login")
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        def connect():
            try:
                conn, cursor = open_conn(user, password)
                st.success("Conexão estabelecida com sucesso!")
                close_conn(conn, cursor)
                st.session_state.username = user
                st.session_state.password = password
            except Exception as e:
                st.write("Erro ao conectar: Usuário ou senha incorretos.")
                pass
        login_button = st.button("Login", on_click=connect)
    else:
        st.title("Farmácia Novo Dia - Banco de Dados")
        operation = st.sidebar.selectbox("Selecione a operação", ("Inserir", "Deletar", "Atualizar", "Buscar"))
        # rever urgentemente isso aqui:
        if operation == "Buscar":
            table_options = ("Clientes", "Vendas", "Produtos", "Funcionários", "Vendas por data", "Valor por venda", "Balconista por turno", "Funcionário da venda") 
        else:
            table_options = ("Clientes", "Vendas", "Produtos", "Funcionários")
        table = st.sidebar.selectbox("Selecione a tabela", table_options)
            
        conn, cursor = open_conn(st.session_state['username'], st.session_state['password'])

        if operation == "Inserir":
            if table == "Clientes":
                cpf_cliente = st.text_input("CPF do cliente")
                nome_cliente = st.text_input("Nome do cliente")
                telefone_cliente_1 = st.text_input("Telefone do cliente")
                telefone_cliente_2 = st.text_input("Telefone alternativo para contato")
                
                cpf_cliente = cpf_cliente if cpf_cliente != "" else None
                nome_cliente = nome_cliente if nome_cliente != "" else None
                telefone_cliente_1 = telefone_cliente_1 if telefone_cliente_1 != "" else None
                telefone_cliente_2 = telefone_cliente_2 if telefone_cliente_2 != "" else None
                
                if st.button("Inserir"):
                    insert_data(conn, cursor, table, (cpf_cliente, nome_cliente, telefone_cliente_1, telefone_cliente_2))

            if table == "Vendas":
                cliente_venda = st.text_input("CPF do cliente")
                funcionario_venda = st.text_input("CPF do funcionário")
                data_venda = st.date_input("Data da venda")
                valor_venda = st.number_input("Valor da venda", min_value=0.0)
                cod_nota_fiscal = st.number_input("Código da nota fiscal")

                cliente_venda = cliente_venda if cliente_venda != "" else None
                funcionario_venda = funcionario_venda if funcionario_venda != "" else None
                data_venda = data_venda if data_venda != "" else None
                valor_venda = valor_venda if valor_venda != "" else None
                cod_nota_fiscal = cod_nota_fiscal if cod_nota_fiscal != "" else None

                if st.button("Inserir"):
                    insert_data(conn, cursor, table, (cliente_venda, funcionario_venda, data_venda, valor_venda, cod_nota_fiscal))

            if table == "Produtos":
                cod_produto = st.number_input("Código do produto")
                preco = st.number_input("Preço do produto", min_value=0.0)
                nome_produto = st.text_input("Nome do produto")
                tipo_produto = st.text_input("Tipo do produto")
                descricao = st.text_input("Descrição do produto")

                cod_produto = cod_produto if cod_produto != "" else None
                preco = preco if preco != "" else None
                nome_produto = nome_produto if nome_produto != "" else None
                tipo_produto = tipo_produto if tipo_produto != "" else None
                descricao = descricao if descricao != "" else None

                if st.button("Inserir"):
                    insert_data(conn, cursor, table, (cod_produto, preco, nome_produto, tipo_produto, descricao))
            
            if table == "Funcionários":
                # não lembro o que ficou definido de como a gente vai inserir essa galera, deixei assim pra depois a gente ver
                func_type = st.sidebar.selectbox("Tipo de funcionário", ("Balconista", "Farmacêutico"))
                if func_type == "Balconista":
                    cpf_balc = st.text_input("CPF")
                    cpf_gerente = st.text_input("CPF do gerente")
                    salario_balc = st.number_input("Salário", min_value=0.0)
                    nome_balc = st.text_input("Nome")
                    data_nasc_balc = st.date_input("Data de nascimento")
                    telefone_balc_1 = st.text_input("Telefone")
                    telefone_balc_2 = st.text_input("Telefone alternativo para contato")
                    turno = st.text_input("Turno do balconista")
                    st.write("Endereço:")
                    rua_balc = st.text_input("Rua")
                    numero_balc = st.number_input("Número")
                    bairro_balc = st.text_input("Bairro")

                    cpf_func = cpf_balc if cpf_balc != "" else None
                    nome_func = nome_balc if nome_balc != "" else None
                    turno = turno if turno != "" else None
                    cpf_gerente = cpf_gerente if cpf_gerente != "" else None
                    salario_func = salario_balc if salario_balc != "" else None
                    data_nasc_func = data_nasc_balc if data_nasc_balc != "" else None
                    rua_func = rua_balc if rua_balc != "" else None
                    numero_func = numero_balc if numero_balc != "" else None
                    bairro_func = bairro_balc if bairro_balc != "" else None
                    telefone_func_1 = telefone_balc_1 if telefone_balc_1 != "" else None
                    telefone_func_2 = telefone_balc_2 if telefone_balc_2 != "" else None

                    if st.button("Inserir"):
                        insert_data(conn, cursor, table, (cpf_func, cpf_gerente, salario_func, nome_func, data_nasc_func, telefone_func_1, telefone_func_2, rua_func, numero_func, bairro_func))
                        insert_data(conn, cursor, "Balconista", (cpf_func, turno))
                
                if func_type == "Farmacêutico":
                    cpf_farm = st.text_input("CPF")
                    cpf_gerente = st.text_input("CPF do gerente")
                    salario_farm = st.number_input("Salário", min_value=0.0)
                    nome_farm = st.text_input("Nome")
                    data_nasc_farm = st.date_input("Data de nascimento")
                    telefone_farm_1 = st.text_input("Telefone")
                    telefone_farm_2 = st.text_input("Telefone alternativo para contato")
                    crf = st.text_input("CRF")
                    st.write("Endereço:")
                    rua_farm = st.text_input("Rua")
                    numero_farm = st.number_input("Número")
                    bairro_farm = st.text_input("Bairro")

                    cpf_func = cpf_farm if cpf_farm != "" else None
                    nome_func = nome_farm if nome_farm != "" else None
                    crf = crf if crf != "" else None
                    cpf_gerente = cpf_gerente if cpf_gerente != "" else None
                    salario_func = salario_farm if salario_farm != "" else None
                    data_nasc_func = data_nasc_farm if data_nasc_farm != "" else None
                    rua_func = rua_farm if rua_farm != "" else None
                    numero_func = numero_farm if numero_farm != "" else None
                    bairro_func = bairro_farm if bairro_farm != "" else None
                    telefone_func_1 = telefone_farm_1 if telefone_farm_1 != "" else None
                    telefone_func_2 = telefone_farm_2 if telefone_farm_2 != "" else None

                    if st.button("Inserir"):
                        insert_data(conn, cursor, table, (cpf_func, cpf_gerente, salario_func, nome_func, data_nasc_func, telefone_func_1, telefone_func_2, rua_func, numero_func, bairro_func))
                        insert_data(conn, cursor, "Farmaceutico", (cpf_func, crf))

        elif operation == "Deletar":
            if table == "Clientes":
                cpf_cliente = st.text_input("CPF do cliente")
                if st.button("Deletar"):
                    delete_data(conn, cursor, table, "cpf_cliente", cpf_cliente)
            if table == "Vendas":
                # fiquei na dúvida se a gente tinha mudado a PK pra cod_nota_fiscal ou não
                cod_nota_fiscal = st.number_input("Código da venda")
                if st.button("Deletar"):
                    delete_data(conn, cursor, table, "cod_nota_fiscal", cod_nota_fiscal)
            if table == "Produtos":
                cod_produto = st.number_input("Código do produto")
                if st.button("Deletar"):
                    delete_data(conn, cursor, table, "cod_produto", cod_produto)
            if table == "Funcionários":
                cpf_func = st.text_input("CPF do funcionário")
                # veja a seguir um código nojento kkkkkk
                # depois a gente conversa como fazer isso, é só porque to fazendo sem ter acesso ao banco, aí to deixando aqui de qualquer jeito pra lembrar de perguntar
                if st.button("Deletar"):
                    delete_data(conn, cursor, table, "cpf_func", cpf_func)
                    try:
                        delete_data(conn, cursor, "Balconista", "cpf_balconista", cpf_func)
                    except:
                        delete_data(conn, cursor, "Farmaceutico", "cpf_farmaceutico", cpf_func)


        elif operation == "Atualizar":
            if table == "Clientes":
                cpf_cliente = st.text_input("CPF do cliente")
                novo_nome = st.text_input("Novo nome")
                novo_telefone_1 = st.text_input("Novo telefone")
                novo_telefone_2 = st.text_input("Novo telefone alternativo para contato")

                if st.button("Atualizar"):
                    if novo_nome:
                        update_data(conn, cursor, table, "nome", novo_nome, "cpf_cliente", cpf_cliente)
                    if novo_telefone_1:
                        update_data(conn, cursor, table, "telefone1", novo_telefone_1, "cpf_cliente", cpf_cliente)
                    if novo_telefone_2:
                        update_data(conn, cursor, table, "telefone2", novo_telefone_2, "cpf_cliente", cpf_cliente)
            
            if table == "Vendas":
                cod_nota_fiscal = st.number_input("Código da venda")
                novo_cliente = st.text_input("CPF do novo cliente")
                novo_funcionario = st.text_input("CPF do novo funcionário")
                nova_data = st.date_input("Nova data")
                novo_valor = st.number_input("Novo valor")
                novo_cod_nota_fiscal = st.number_input("Novo código da nota fiscal")

                if st.button("Atualizar"):
                    if novo_cliente:
                        update_data(conn, cursor, table, "cpf_cliente", novo_cliente, "cod_nota_fiscal", cod_nota_fiscal)
                    if novo_funcionario:
                        update_data(conn, cursor, table, "cpf_func", novo_funcionario, "cod_nota_fiscal", cod_nota_fiscal)
                    if nova_data:
                        update_data(conn, cursor, table, "data_venda", nova_data, "cod_nota_fiscal", cod_nota_fiscal)
                    if novo_valor:
                        update_data(conn, cursor, table, "valor", novo_valor, "cod_nota_fiscal", cod_nota_fiscal)

            if table == "Produtos":
                cod_produto = st.number_input("Código do produto")
                novo_preco = st.number_input("Novo preço")
                novo_nome = st.text_input("Novo nome")
                novo_tipo = st.text_input("Novo tipo")
                nova_descricao = st.text_input("Nova descrição")

                if st.button("Atualizar"):
                    if novo_preco:
                        update_data(conn, cursor, table, "preco", novo_preco, "cod_produto", cod_produto)
                    if novo_nome:
                        update_data(conn, cursor, table, "nome", novo_nome, "cod_produto", cod_produto)
                    if novo_tipo:
                        update_data(conn, cursor, table, "tipo", novo_tipo, "cod_produto", cod_produto)
                    if nova_descricao:
                        update_data(conn, cursor, table, "descricao", nova_descricao, "cod_produto", cod_produto)

            if table == "Funcionários":
                cpf_func = st.text_input("CPF do funcionário")
                novo_cpf_gerente = st.text_input("CPF do novo gerente")
                novo_salario = st.number_input("Novo salário")
                novo_nome = st.text_input("Novo nome")
                nova_data = st.date_input("Nova data de nascimento")
                novo_telefone_1 = st.text_input("Novo telefone")
                novo_telefone_2 = st.text_input("Novo telefone alternativo para contato")
                novo_rua = st.text_input("Nova rua")
                novo_numero = st.number_input("Novo número")
                novo_bairro = st.text_input("Novo bairro")

                tipo_funcionario = st.radio("Tipo de funcionário", ["Balconista", "Farmacêutico"])
                if tipo_funcionario == "Balconista":
                    novo_turno = st.text_input("Novo turno")
                elif tipo_funcionario == "Farmacêutico":
                    novo_crf = st.text_input("Novo CRF")

                if st.button("Atualizar"):
                    if novo_cpf_gerente:
                        update_data(conn, cursor, table, "cpf_gerente", novo_cpf_gerente, "cpf_func", cpf_func)
                    if novo_salario:
                        update_data(conn, cursor, table, "salario", novo_salario, "cpf_func", cpf_func)
                    if novo_nome:
                        update_data(conn, cursor, table, "nome", novo_nome, "cpf_func", cpf_func)
                    if nova_data:
                        update_data(conn, cursor, table, "data_nasc", nova_data, "cpf_func", cpf_func)
                    if novo_telefone_1:
                        update_data(conn, cursor, table, "telefone1", novo_telefone_1, "cpf_func", cpf_func)
                    if novo_telefone_2:
                        update_data(conn, cursor, table, "telefone2", novo_telefone_2, "cpf_func", cpf_func)
                    if novo_rua:
                        update_data(conn, cursor, table, "rua", novo_rua, "cpf_func", cpf_func)
                    if novo_numero:
                        update_data(conn, cursor, table, "numero", novo_numero, "cpf_func", cpf_func)
                    if novo_bairro:
                        update_data(conn, cursor, table, "bairro", novo_bairro, "cpf_func", cpf_func)
                    if novo_crf:
                        update_data(conn, cursor, table, "crf", novo_crf, "cpf_func", cpf_func)
                    if novo_turno:
                        update_data(conn, cursor, "Balconista", "turno", novo_turno, "cpf_balconista", cpf_func)

        #eu dei um get columns aqui pra facilitar, tu acha que Gabi reclama?
        elif operation == 'Select':
            if table == "funcionários" or "clientes" or "vendas" or "produtos":
                data = select_table(conn, cursor, table)
                st.write(f"Dados da tabela {table}:")
                columns = get_table_columns(cursor, table)
                df = pd.DataFrame(data, columns=columns)
                #st.dataframe(df.set_index('Código do Curso'), width=800)

            if table == "Balconista por turno":
                turno = st.text_input("Turno de interesse")
                if st.button("Buscar"):
                    result = select_balc_turno(conn, cursor, turno)
                    st.write(f"Balconistas que trabalham no turno da {turno}:")
                    df = pd.DataFrame(result, columns=["Cpf", "Nome"])

            if table == "Vendas por data":
                data = st.date_input("Data de interesse")
                if st.button("Buscar"):
                    result = select_venda_data(conn, cursor, data)
                    st.write(f"Vendas realizadas no dia {data}:")
                    df = pd.DataFrame(result, columns=["CPF do cliente", "CPF do funcionário", "Data da venda", "Valor da venda", "Código da nota fiscal"])

            if table == "Valor por venda":
                cod_venda = st.number_input("Código da venda")
                if st.button("Buscar"):
                    result = select_preco_venda(conn, cursor, cod_venda)
                    st.write("Valor da venda: R$")

            if table == "Funcionário da venda":
                cod_venda = st.number_input("Código da venda")
                if st.button("Buscar"):
                    result = select_func_venda(conn, cursor, cod_venda)
                    st.write("Funcionário responsável pela venda: ")
                    df = pd.DataFrame(result, columns=["Cpf", "Nome"])

        close_conn(conn, cursor)
