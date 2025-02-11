import streamlit as st
from time import sleep
import pandas as pd
from crud import ler_todos_usuarios, cria_usuarios, modifica_usuario, deleta_usuario


def tab_gestao_usuarios():
    tab_vis, tab_cria, tab_mod, tab_del = st.tabs(
        ['Visualizar', 'Criar', 'Modificar', 'Deletar']
    )
    usuarios = ler_todos_usuarios()
    with tab_vis:
        data_usuarios = [{
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'acesso_gestor': usuario.acesso_gestor,
            'inicio_na_empresa': usuario.inicio_na_empresa
        }for usuario in usuarios]
        st.dataframe(pd.DataFrame(data_usuarios).set_index('id'))
    with tab_cria:
        nome = st.text_input('Nome do Usuário')
        senha = st.text_input('Senha do Usuário')
        email = st.text_input('Email do Usuário')
        acesso_gestor = st.checkbox('Tem Acesso Gestor?',False)
        inicio_na_empresa = st.text_input('Data de início na empresa (formato AAAA-MM-DD')

        if st.button('Criar'):
            cria_usuarios(
                nome = nome,
                senha= senha,
                email = email,
                acesso_gestor = acesso_gestor,
                inicio_na_empresa = inicio_na_empresa
            )
            st.success('Cadastro Realizado com sucesso!')
            sleep(1)
            st.rerun()
    with tab_mod:
        usuarios_dict = {usuario.nome: usuario for usuario in usuarios}
        nome_usuario = st.selectbox('Selecione o usuário para modificar', usuarios_dict.keys())
        usuario = usuarios_dict[nome_usuario]
        nome = st.text_input(
            'Nome do Usuário',
            value=usuario.nome
            )
        senha = st.text_input(
            'Senha do Usuário',
            value='xxxxx'
            )
        email = st.text_input(
            'Email do Usuário',
             value=usuario.email
            )
        acesso_gestor = st.checkbox(
            'Modificar Acesso Gestor?',
            value= usuario.acesso_gestor
        )
        inicio_na_empresa = st.text_input(
            'Data de início na empresa (formato AAAA-MM-DD)',
            value= usuario.inicio_na_empresa
            )

        if st.button('Modificar'):
            if senha == 'xxxxx':
                modifica_usuario(
                    id=usuario.id,
                    nome=nome,
                    email=email,
                    acesso_gestor=acesso_gestor,
                    inicio_na_empresa=inicio_na_empresa
                )
            else:
                modifica_usuario(
                    id= usuario.id,
                    nome=nome,
                    senha=senha,
                    email=email,
                    acesso_gestor=acesso_gestor,
                    inicio_na_empresa=inicio_na_empresa
                )
            st.success('Usuário Modificado com sucesso!')
            sleep(1)
            st.rerun()

    with tab_del:
        usuarios_dict = {usuario.nome: usuario for usuario in usuarios}
        nome_usuario = st.selectbox('Selecione o usuário para deletar', usuarios_dict.keys())
        usuario = usuarios_dict[nome_usuario]

        if st.button('Deletar'):
            deleta_usuario(usuario.id)
        st.success('Usuário Deletado com sucesso!')
        sleep(1)
        st.rerun()

def pagina_gestao():

    usuarios = ler_todos_usuarios()

    for usuario in usuarios:
        with st.container(border=True):
            cols = st.columns(2)
            dias_para_solicitar = usuario.dias_para_solicitar()
            with cols[0]:
                if dias_para_solicitar > 40:
                    st.error(f'### {usuario.nome}')
                else:
                    st.markdown(f'### {usuario.nome}')
            with cols[1]:
                if dias_para_solicitar > 40:
                    st.error(f'#### Dias para tirar {dias_para_solicitar}')
                else:
                    st.markdown(f'#### Dias para tirar {dias_para_solicitar}')
