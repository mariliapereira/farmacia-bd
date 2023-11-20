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
        operation = st.sidebar.selectbox("Selecione a operação", ("Inserir", "Deletar", "Atualizar", "Visualizar", "Gerar relatório"))
        if operation == "Gerar relatório":
            table_options = ("Funcionário do mês", "Arrecadamento mensal", "Produto mais vendido por mês", "Produto favorito por cliente")
        else:
            table_options = ("Cliente", "Venda", "Produto", "Funcionário")
        table = st.sidebar.selectbox("Escolha uma tabela:", table_options)

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
                        insert_data(conn, cursor, "produto_venda", (cod_prod_venda, fk_venda, 1 if receita_venda == "Sim" else 0, quantidade_venda))
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

                    cpf_balc = cpf_balc if cpf_balc != "" else None
                    nome_balc = nome_balc if nome_balc != "" else None
                    turno = turno if turno != "" else None
                    cpf_gerente = cpf_gerente if cpf_gerente != "" else None
                    salario_balc = salario_balc if salario_balc != "" else None
                    data_nasc_balc = data_nasc_balc if data_nasc_balc != "" else None
                    rua_balc = rua_balc if rua_balc != "" else None
                    numero_bacl = numero_balc if numero_balc != "" else None
                    bairro_balc = bairro_balc if bairro_balc != "" else None
                    telefone_balc_1 = telefone_balc_1 if telefone_balc_1 != "" else None
                    telefone_balc_2 = telefone_balc_2 if telefone_balc_2 != "" else None
                    print(f'cpf gerente: {cpf_gerente}\ntelefone 1: {telefone_balc_1}\ntelefone2: {telefone_balc_2}')

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

                    cpf_farm = cpf_farm if cpf_farm != "" else None
                    nome_farm = nome_farm if nome_farm != "" else None
                    crf = crf if crf != "" else None
                    cpf_gerente = cpf_gerente if cpf_gerente != "" else None
                    salario_farm = salario_farm if salario_farm != "" else None
                    data_nasc_farm = data_nasc_farm if data_nasc_farm != "" else None
                    rua_farm = rua_farm if rua_farm != "" else None
                    numero_farm = numero_farm if numero_farm != "" else None
                    bairro_farm = bairro_farm if bairro_farm != "" else None
                    telefone_farm_1 = telefone_farm_1 if telefone_farm_1 != "" else None
                    telefone_farm_2 = telefone_farm_2 if telefone_farm_2 != "" else None

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
                novo_preco = st.number_input("Novo preço", min_value=0.0)
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
                novo_salario = st.number_input("Novo salário", min_value=0.0)
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

        elif operation == 'Visualizar':
            if table == "Cliente":
                filter_option = st.radio("Filtrar clientes por:", ["Cpf", "Nome", "Telefone 1", "Telefone 2"], index = None)

                if filter_option == None:
                    result = select_table(conn, cursor, table)
                else:
                    user_input = st.text_input(f"Informe o {filter_option} para filtrar:")
                    if filter_option == "Nome":
                        result = select_table(conn, cursor, table, filter_column="Nome", input=user_input)
                    elif filter_option == "Telefone 1":
                        result = select_table(conn, cursor, table, filter_column="Telefone1", input=user_input)
                    elif filter_option == "Telefone 2":
                        result = select_table(conn, cursor, table, filter_column="Telefone2", input=user_input)
                    elif filter_option == "Cpf":
                        result = select_table(conn, cursor, table, filter_column="cpf_cliente", input=user_input)

                st.write(f"{table}s:")
                df = pd.DataFrame(result, columns=["Cpf", "Nome", "Telefone 1", "Telefone 2"])
                st.dataframe(df.set_index('Cpf'), width=800)
                

            if table == "Venda":
                filter_option = st.radio("Filtrar vendas por:", ["Código da nota fiscal", "CPF do cliente", "CPF do funcionário", "Valor da venda", "Data", "Código do produto vendido"], index = None)

                if filter_option == None:
                    result = select_table(conn, cursor, table)
                else:
                    user_input = st.text_input(f"Informe o {filter_option} para filtrar:")
                    if filter_option == "Código da nota fiscal":
                        result = select_table(conn, cursor, table, filter_column="cod_nota_fiscal", input=user_input)
                    elif filter_option == "CPF do cliente":
                        result = select_table(conn, cursor, table, filter_column="fk_cliente", input=user_input)
                    elif filter_option == "CPF do funcionário":
                        result = select_table(conn, cursor, table, filter_column="fk_func", input=user_input)
                    elif filter_option == "Valor da venda":
                        result = select_table(conn, cursor, table, filter_column="valor", input=user_input)
                    elif filter_option == "Data":
                        result = select_table(conn, cursor, table, filter_column="data_venda", input=user_input)
                    elif filter_option == "Código do produto vendido":
                        result = select_table(conn, cursor, table, filter_column="cod_prod", input=user_input)
                        
                st.write(f"{table}s:")
                df = pd.DataFrame(result, columns=["CPF do cliente", "CPF do funcionário", "Data da venda", "Valor da venda", "Código da nota fiscal"])
                st.dataframe(df.set_index('Código da nota fiscal'), width=800)

            
            if table == "Produto":
                filter_option = st.radio("Filtrar produtos por:", ["Nome", "Tipo", "Marca", "Descrição", "Preço", "Código do produto"], index = None)

                if filter_option == None:
                    result = select_table(conn, cursor, table)
                else:
                    user_input = st.text_input(f"Informe o {filter_option} para filtrar:")
                    if filter_option == "Nome":
                        result = select_table(conn, cursor, table, filter_column="Nome", input=user_input)
                    elif filter_option == "Tipo":
                        result = select_table(conn, cursor, table, filter_column="Tipo", input=user_input)
                    elif filter_option == "Marca":
                        result = select_table(conn, cursor, table, filter_column="Marca", input=user_input)
                    elif filter_option == "Descrição":
                        result = select_table(conn, cursor, table, filter_column="Descricao", input=user_input)
                    elif filter_option == "Preço":
                        result = select_table(conn, cursor, table, filter_column="Preco", input=user_input)
                    elif filter_option == "Código do produto":
                        result = select_table(conn, cursor, table, filter_column="cod_prod", input=user_input)

                st.write(f"{table}s:")
                df = pd.DataFrame(result, columns=["Código do produto", "Preço", "Nome", "Tipo", "Descrição", "Marca"])
                st.dataframe(df.set_index('Código do produto'), width=800)

            
            if table == "Funcionário":
                filter_option = st.radio("Filtrar funcionários por:", ["Cpf", "Cpf do gerente", "Nome", "Telefone 1", "Telefone 2", "Salário", "Data de nascimento", "Rua", "Número", "Bairro", "Turno", "Crf"], index = None)

                if filter_option == None:
                    result = select_table(conn, cursor, "Funcionario")
                else:
                    user_input = st.text_input(f"Informe o {filter_option} para filtrar:")
                    if filter_option == "Nome":
                        result = select_table(conn, cursor, "Funcionario", filter_column="Nome", input=user_input)
                    elif filter_option == "Cpf do gerente":
                        result = select_table(conn, cursor, "Funcionario", filter_column="cpf_gerente", input=user_input)
                    elif filter_option == "Cpf":
                        result = select_table(conn, cursor, "Funcionario", filter_column="cpf_func", input=user_input)
                    elif filter_option == "Telefone 1":
                        result = select_table(conn, cursor, "Funcionario", filter_column="Telefone1", input=user_input)
                    elif filter_option == "Telefone 2":
                        result = select_table(conn, cursor, "Funcionario", filter_column="Telefone2", input=user_input)
                    elif filter_option == "Cpf":
                        result = select_table(conn, cursor, "Funcionario", filter_column="cpf_func", input=user_input)
                    elif filter_option == "Salário":
                        result = select_table(conn, cursor, "Funcionario", filter_column="salario", input=user_input)
                    elif filter_option == "Data de nascimento":
                        result = select_table(conn, cursor, "Funcionario", filter_column="data_nasc", input=user_input)
                    elif filter_option == "Rua":
                        result = select_table(conn, cursor, "Funcionario", filter_column="rua", input=user_input)
                    elif filter_option == "Número":
                        result = select_table(conn, cursor, "Funcionario", filter_column="numero", input=user_input)
                    elif filter_option == "Bairro":
                        result = select_table(conn, cursor, "Funcionario", filter_column="bairro", input=user_input)
                    elif filter_option == "Tipo":
                        result = select_table(conn, cursor, "Funcionario", filter_column="tipo", input=user_input)
                    elif filter_option == "Turno":
                        result = select_table(conn, cursor, "Funcionario", filter_column="turno", input=user_input)
                    elif filter_option == "Crf":
                        result = select_table(conn, cursor, "Funcionario", filter_column="crf", input=user_input)

                st.write(f"{table}s:")
                df = pd.DataFrame(result, columns=["Cpf", "Cpf do gerente", "Salário", "Data de nascimento", "Telefone 1", "Telefone 2", "Rua", "Número", "Bairro", "Nome"])
                st.dataframe(df.set_index('Cpf'), width=800)
        
        elif operation == "Gerar relatório":
            meses = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 
                                7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
            if table == "Funcionário do mês":
                mes = st.number_input("Mês", min_value=1, max_value=12)
                result = funcionario_do_mes(conn, cursor, mes)
                nome_mes = meses.get(mes)
                st.write(f"Funcionário de {nome_mes}:")
                df = pd.DataFrame(result, columns=["Nome", "Total de vendas"])
                st.dataframe(df.set_index('Nome'), width=400)
            
            if table == "Produto mais vendido por mês":
                mes = st.number_input("Mês", min_value=1, max_value=12)
                nome_mes = meses.get(mes)
                result = produto_mais_vendido_mes(conn, cursor, mes)
                st.write(f"Produto mais vendido em {nome_mes}:")
                df = pd.DataFrame(result, columns=["Mês", "Arrecadamento (R$)"])
                st.dataframe(df.set_index('Mês'), width=800)

            if table == "Arrecadamento mensal":
                mes = st.number_input("Mês", min_value=1, max_value=12)
                nome_mes = meses.get(mes)
                result = arrecadamento_mensal(conn, cursor, mes)
                st.write(f"Arrecadamento de {nome_mes}: R${result[0][0]}")

            if table == "Produto favorito por cliente":
                nome_cliente = st.text_input("Nome do cliente")
                result = produto_mais_comprado_pelo_cliente(conn, cursor, nome_cliente)
                st.write("Produto mais comprado pelo cliente:")
                df = pd.DataFrame(result, columns=["Código do produto", "Nome do produto", "Total de compras"])
                st.dataframe(df.set_index('Código do produto'), width=800)