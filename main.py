from time import sleep
import streamlit as st
import pandas as pd

from crud import ler_todos_usuarios, cria_usuarios, modifica_usuario, deleta_usuario

def login():
    usuarios = ler_todos_usuarios()
    usuarios = {usuario.nome: usuario for usuario in usuarios}
    with st.container(border=True):
        st.markdown('Bem-Vindos ao AppFerias')
        nome_usuario = st.selectbox(
            'Selecione o seu usuário',
            usuarios.keys()
        )
        senha = st.text_input(
            'Digite sua senha',
            type= 'password'
        )
        if st.button('Acessar'):
            usuario = usuarios[nome_usuario]

            if usuario.verifica_senha(senha):
                st.success('Login efetuado com sucesso!')
                st.session_state['usuario'] = usuario
                st.session_state['logado'] = True
                sleep(1)
                st.rerun() #sair da tela de login e ir pra outra tela
            else:
                st.error('Senha incorreta')
def pagina_calendario():
    st.title('Bem-Vindo ao AppFerias')
    st.divider()

    usuario = st.session_state['usuario']

    if usuario.acesso_gestor:
        cols = st.columns(2)
        with cols[0]:
            if st.button('Acessar Gestão de Usuários', use_container_width=True):
                st.session_state['pag_gestao_usuarios'] = True
                st.rerun()
        with cols[1]:
            if st.button('Acessar Acessar Calendário', use_container_width=True):
                st.session_state['pag_gestao_usuarios'] = False
                st.rerun()
    if st.session_state['pag_gestao_usuarios']:
        st.markdown('Página Gestão de Usuários')
        with st.sidebar:
            tab_gestao_usuarios()
    else:
        st.markdown('Calendário')

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

def main():
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False

    if not 'pag_gestao_usuarios' in st.session_state:
        st.session_state['pag_gestao_usuarios'] = False

    if not st.session_state['logado']:
        login()
    else:
        pagina_calendario()

if __name__ == '__main__':
    main()