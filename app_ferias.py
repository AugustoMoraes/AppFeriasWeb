from time import sleep
import streamlit as st

from crud import ler_todos_usuarios
from pagina_calendario import  pagina_calendario
from pagina_gestao import pagina_gestao, tab_gestao_usuarios


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
def pagina_principal():
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
        pagina_gestao()
        with st.sidebar:
            tab_gestao_usuarios()

    else:
        pagina_calendario()
def main():
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False

    if not 'pag_gestao_usuarios' in st.session_state:
        st.session_state['pag_gestao_usuarios'] = False

    if not st.session_state['logado']:
        login()
    else:
        pagina_principal()


if __name__ == '__main__':
    main()