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
            table_options = ("Cliente", "Venda", "Produto", "Funcionário", "Vendas por data", "Valor por venda", "Balconista por turno", "Funcionário da venda", "Produtos por marca") 
        else:
            table_options = ("Cliente", "Venda", "Produto", "Funcionário")
        table = st.sidebar.selectbox("Selecione a tabela", table_options)
            
        conn, cursor = open_conn(st.session_state['username'], st.session_state['password'])

        if operation == "Inserir":
            if table == "Cliente":
                cpf_cliente = st.text_input("CPF do cliente - apenas números -")
                nome_cliente = st.text_input("Nome do cliente")
                telefone_cliente_1 = st.text_input("Telefone do cliente")
                telefone_cliente_2 = st.text_input("Telefone alternativo para contato")
                
                cpf_cliente = cpf_cliente if cpf_cliente != "" else None
                nome_cliente = nome_cliente if nome_cliente != "" else None
                telefone_cliente_1 = telefone_cliente_1 if telefone_cliente_1 != "" else None
                telefone_cliente_2 = telefone_cliente_2 if telefone_cliente_2 != "" else None
                
                if st.button("Inserir"):
                    insert_data(conn, cursor, table, (cpf_cliente, nome_cliente, telefone_cliente_1, telefone_cliente_2))

            if table == "Venda":
                cliente_venda = st.text_input("CPF do cliente - apenas números -")
                funcionario_venda = st.text_input("CPF do funcionário - apenas números -")
                data_venda = st.text_input("Data da venda (formato AAAA-MM-DD)")

                cliente_venda = cliente_venda if cliente_venda != "" else None
                funcionario_venda = funcionario_venda if funcionario_venda != "" else None
                data_venda = data_venda if data_venda != "" else None

                if "Insert" not in st.session_state:
                    st.session_state.Insert = -1
                def set_insert():
                    insert_data(conn, cursor, table, (cliente_venda, funcionario_venda, data_venda))
                    st.session_state.Insert = get_cod_nota(conn, cursor, cliente_venda, funcionario_venda, data_venda)
                st.button("Inserir", on_click=set_insert)

                if st.session_state.Insert != -1:
                    st.write("Adicionar os produtos vendidos:")
                    fk_venda = st.session_state.Insert
                    if 'cnt' not in st.session_state:
                        st.session_state.cnt = 1
                    for count in range(st.session_state.cnt):
                        cod_prod_venda = st.number_input("Código do produto", min_value=0, key=f"cod_prod{count}", disabled=count!=st.session_state.cnt-1)
                        receita_venda = st.radio("Receita", ["Sim", "Não"], key=f"receita{count}", disabled=count!=st.session_state.cnt-1)
                        quantidade_venda = st.number_input("Quantidade", min_value=0, key=f"quantidade{count}", disabled=count!=st.session_state.cnt-1)

                        if count == st.session_state.cnt - 1:
                            def add_more():
                                st.session_state.cnt += 1
                                insert_data(conn, cursor, "produto_venda", (cod_prod_venda, fk_venda, 1 if receita_venda == "Sim" else 0, quantidade_venda))
                            st.button("Adicionar mais produtos", on_click=add_more)
                    
                    if st.button("Finalizar"):
                        st.write(f"Venda finalizada com sucesso! Código da nota fiscal gerada: {fk_venda}")

            if table == "Produto":
                preco = st.number_input("Preço", min_value=0.0)
                nome_produto = st.text_input("Nome do produto")
                tipo_produto = st.radio("Tipo do produto", ["RX", "OTC", "Diversos"])
                descricao = st.text_input("Descrição")
                marca = st.text_input("Marca/Laboratório")

                preco = preco if preco != "" else None
                nome_produto = nome_produto if nome_produto != "" else None
                tipo_produto = tipo_produto if tipo_produto != "" else None
                descricao = descricao if descricao != "" else None
                marca = marca if marca != "" else None

                if st.button("Inserir"):
                    insert_data(conn, cursor, table, (preco, nome_produto, tipo_produto, descricao, marca))
            
            if table == "Funcionário":
                # não lembro o que ficou definido de como a gente vai inserir essa galera, deixei assim pra depois a gente ver
                func_type = st.sidebar.selectbox("Tipo de funcionário", ("Balconista", "Farmacêutico"))
                if func_type == "Balconista":
                    cpf_balc = st.text_input("CPF - apenas números -")
                    cpf_gerente = st.text_input("CPF do gerente - apenas números -")
                    salario_balc = st.number_input("Salário", min_value=0.0)
                    nome_balc = st.text_input("Nome")
                    data_nasc_balc = st.text_input("Data de nascimento (formato AAAA-MM-DD)")
                    telefone_balc_1 = st.text_input("Telefone")
                    telefone_balc_2 = st.text_input("Telefone alternativo para contato")
                    turno = st.radio("Turno", ["Diurno", "Noturno"])
                    st.write("Endereço:")
                    rua_balc = st.text_input("Rua")
                    numero_balc = st.number_input("Número", min_value=0)
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
                        insert_data(conn, cursor, "Funcionario", (cpf_balc, cpf_gerente, salario_balc, data_nasc_balc, telefone_balc_1, telefone_balc_2, rua_balc, numero_balc, bairro_balc, nome_balc))
                        insert_data(conn, cursor, "Balconista", (cpf_balc, turno))
                
                if func_type == "Farmacêutico":
                    cpf_farm = st.text_input("CPF - apenas números -")
                    cpf_gerente = st.text_input("CPF do gerente - apenas números -")
                    salario_farm = st.number_input("Salário", min_value=0.0)
                    nome_farm = st.text_input("Nome")
                    data_nasc_farm = st.text_input("Data de nascimento (formato AAAA-MM-DD)")
                    telefone_farm_1 = st.text_input("Telefone")
                    telefone_farm_2 = st.text_input("Telefone alternativo para contato")
                    crf = st.text_input("CRF")
                    st.write("Endereço:")
                    rua_farm = st.text_input("Rua")
                    numero_farm = st.number_input("Número", min_value=0)
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
                        insert_data(conn, cursor, "Funcionario", (cpf_farm, cpf_gerente, salario_farm, data_nasc_farm, telefone_farm_1, telefone_farm_2, rua_farm, numero_farm, bairro_farm, nome_farm))
                        insert_data(conn, cursor, "Farmaceutico", (cpf_farm, crf))

        elif operation == "Deletar":
            if table == "Cliente":
                cpf_cliente = st.text_input("CPF do cliente - apenas números -")
                if st.button("Deletar"):
                    delete_data(conn, cursor, table, "cpf_cliente", cpf_cliente)
            if table == "Venda":
                criterio = st.radio("Critério de busca", ["Código da nota fiscal", "CPF do cliente", "CPF do funcionário"])
                if criterio == "Código da nota fiscal":
                    cod_nota_fiscal = st.number_input("Código da nota fiscal", min_value = 0)
                    if st.button("Deletar"):
                        delete_data(conn, cursor, table, "cod_nota_fiscal", cod_nota_fiscal)
                elif criterio == "CPF do cliente":
                    cpf_cliente = st.text_input("CPF do cliente - apenas números -")
                    if st.button("Deletar"):
                        delete_data(conn, cursor, table, "fk_cliente", cpf_cliente)
                elif criterio == "CPF do funcionário":
                    cpf_func = st.text_input("CPF do funcionário - apenas números -")
                    if st.button("Deletar"):
                        delete_data(conn, cursor, table, "fk_func", cpf_func)
            if table == "Produto":
                cod_produto = st.number_input("Código do produto", min_value=0)
                if st.button("Deletar"):
                    delete_data(conn, cursor, table, "cod_prod", cod_produto)
            if table == "Funcionário":
                cpf_func = st.text_input("CPF do funcionário - apenas números -")
                tipo_funcionario = st.radio("Tipo de funcionário", ["Balconista", "Farmacêutico"])
                if st.button("Deletar"):
                    if tipo_funcionario == "Balconista":
                        delete_data(conn, cursor, "Balconista", "cpf_balconista", cpf_func)
                        delete_data(conn, cursor, "Funcionario", "cpf_func", cpf_func)
                    else:
                        delete_data(conn, cursor, "Farmaceutico", "cpf_farm", cpf_func)
                        delete_data(conn, cursor, "Funcionario", "cpf_func", cpf_func)

        elif operation == "Atualizar":
            if table == "Cliente":
                cpf_cliente = st.text_input("CPF do cliente - apenas números -")
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
            
            if table == "Venda":
                cod_nota_fiscal = st.number_input("Código da nota fiscal", min_value=0)
                novo_cliente = st.text_input("CPF do novo cliente")
                novo_funcionario = st.text_input("CPF do novo funcionário")
                nova_data = st.text_input("Nova data")

                if st.button("Atualizar"):
                    if novo_cliente:
                        update_data(conn, cursor, table, "fk_cliente", novo_cliente, "cod_nota_fiscal", cod_nota_fiscal)
                    if novo_funcionario:
                        update_data(conn, cursor, table, "fk_func", novo_funcionario, "cod_nota_fiscal", cod_nota_fiscal)
                    if nova_data:
                        update_data(conn, cursor, table, "data_venda", nova_data, "cod_nota_fiscal", cod_nota_fiscal)

            if table == "Produto":
                cod_produto = st.number_input("Código do produto", min_value=0)
                novo_preco = st.number_input("Novo preço")
                novo_nome = st.text_input("Novo nome")
                novo_tipo = st.radio("Novo tipo", ["RX", "OTC", "Diversos"])
                nova_descricao = st.text_input("Nova descrição")
                nova_marca = st.text_input("Nova marca")

                if st.button("Atualizar"):
                    if novo_preco:
                        update_data(conn, cursor, table, "preco", novo_preco, "cod_prod", cod_produto)
                    if novo_nome:
                        update_data(conn, cursor, table, "nome", novo_nome, "cod_prod", cod_produto)
                    if novo_tipo:
                        update_data(conn, cursor, table, "tipo", novo_tipo, "cod_prod", cod_produto)
                    if nova_descricao:
                        update_data(conn, cursor, table, "descricao", nova_descricao, "cod_prod", cod_produto)
                    if nova_marca:
                        update_data(conn, cursor, table, "marca", nova_marca, "cod_prod", cod_produto)

            if table == "Funcionário":
                cpf_func = st.text_input("CPF do funcionário - apenas números -")
                novo_cpf_gerente = st.text_input("CPF do novo gerente - apenas números -")
                novo_salario = st.number_input("Novo salário")
                novo_nome = st.text_input("Novo nome")
                nova_data = st.text_input("Nova data de nascimento")
                novo_telefone_1 = st.text_input("Novo telefone")
                novo_telefone_2 = st.text_input("Novo telefone alternativo para contato")
                novo_rua = st.text_input("Nova rua")
                novo_numero = st.number_input("Novo número", min_value=0)
                novo_bairro = st.text_input("Novo bairro")

                novo_turno = novo_crf = ""
                tipo_funcionario = st.radio("Tipo de funcionário", ["Balconista", "Farmacêutico"])
                if tipo_funcionario == "Balconista":
                    novo_turno = st.radio("Novo turno", ["Diurno", "Noturno"])
                elif tipo_funcionario == "Farmacêutico":
                    novo_crf = st.text_input("Novo CRF")

                if st.button("Atualizar"):
                    if novo_cpf_gerente:
                        update_data(conn, cursor, "Funcionario", "cpf_gerente", novo_cpf_gerente, "cpf_func", cpf_func)
                    if novo_salario:
                        update_data(conn, cursor, "Funcionario", "salario", novo_salario, "cpf_func", cpf_func)
                    if novo_nome:
                        update_data(conn, cursor, "Funcionario", "nome", novo_nome, "cpf_func", cpf_func)
                    if nova_data:
                        update_data(conn, cursor, "Funcionario", "data_nasc", nova_data, "cpf_func", cpf_func)
                    if novo_telefone_1:
                        update_data(conn, cursor, "Funcionario", "telefone1", novo_telefone_1, "cpf_func", cpf_func)
                    if novo_telefone_2:
                        update_data(conn, cursor, "Funcionario", "telefone2", novo_telefone_2, "cpf_func", cpf_func)
                    if novo_rua:
                        update_data(conn, cursor, "Funcionario", "rua", novo_rua, "cpf_func", cpf_func)
                    if novo_numero:
                        update_data(conn, cursor, "Funcionario", "numero", novo_numero, "cpf_func", cpf_func)
                    if novo_bairro:
                        update_data(conn, cursor, "Funcionario", "bairro", novo_bairro, "cpf_func", cpf_func)
                    if novo_crf:
                        update_data(conn, cursor, "Farmaceutico", "crf", novo_crf, "cpf_func", cpf_func)
                    if novo_turno:
                        update_data(conn, cursor, "Balconista", "turno", novo_turno, "cpf_balconista", cpf_func)

        elif operation == 'Buscar':
            if table == "Cliente":
                result = select_table(conn, cursor, table)
                st.write(f"{table}s:")
                df = pd.DataFrame(result, columns=["Cpf", "Nome", "Telefone 1", "Telefone 2"])
                st.dataframe(df.set_index('Cpf'), width=800)

            if table == "Venda":
                result = select_table(conn, cursor, table)
                st.write(f"{table}s:")
                df = pd.DataFrame(result, columns=["CPF do cliente", "CPF do funcionário", "Data da venda", "Valor da venda", "Código da nota fiscal"])
                st.dataframe(df.set_index('Código da nota fiscal'), width=800)
            
            if table == "Produto":
                result = select_table(conn, cursor, table)
                st.write(f"{table}s:")
                df = pd.DataFrame(result, columns=["Código do produto", "Preço", "Nome", "Tipo", "Descrição", "Marca"])
                st.dataframe(df.set_index('Código do produto'), width=800)
            
            if table == "Funcionário":
                result = select_table(conn, cursor, "Funcionario")
                st.write(f"{table}s:")
                df = pd.DataFrame(result, columns=["CPF", "CPF do gerente", "Salário", "Data de nascimento", "Telefone 1", "Telefone 2", "Rua", "Número", "Bairro", "Nome"])
                st.dataframe(df.set_index('CPF'), width=800)
        
            if table == "Balconista por turno":
                turno = st.text_input("Turno de interesse")
                if st.button("Buscar"):
                    result = select_balc_turno(conn, cursor, turno)
                    st.write(f"Balconistas que trabalham no turno da {turno}:")
                    df = pd.DataFrame(result, columns=["Cpf", "Nome"])

            if table == "Vendas por data":
                data = st.text_input("Data de interesse")
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

            if table == "Produtos por marca":
                marca = st.text_input("Marca de interesse")
                if st.button("Buscar"):
                    result = select_prod_marca(conn, cursor, marca)
                    st.write(f"Produtos da marca {marca}:")
                    df = pd.DataFrame(result, columns=["Código do produto", "Preço", "Nome", "Tipo", "Descrição", "Marca"])

