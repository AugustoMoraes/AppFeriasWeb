import json
from datetime import datetime
import streamlit as st

from streamlit_calendar import calendar

from crud import ler_todos_usuarios

def verifica_e_adiciona_ferias(data_inicio, data_fim):
    usuario = st.session_state['usuario']

    total_dias = (
        datetime.strptime(data_fim, '%Y-%m-%d')
        - datetime.strptime(data_inicio, '%Y-%m-%d')
    ).days + 1
    dias_solicitar = usuario.dias_para_solicitar()
    if total_dias < 5:
        st.error('Quantidade de dias inferior a 5')
    elif dias_solicitar < total_dias:
        st.error(f'Usuário solicitou {total_dias}, mas tem apenas {dias_solicitar} para solicitar')
    else:
        usuario.adiciona_ferias(data_inicio, data_fim)
        limpa_datas()

def limpa_datas():
    del st.session_state['data_inicio']
    del st.session_state['data_final']

def pagina_calendario():


    with open('calendar_options.json') as f:
        calendar_options = json.load(f)

    usuarios = ler_todos_usuarios()
    calendar_events = []
    for usuario in usuarios:
        calendar_events.extend(usuario.lista_ferias())

    usuario = st.session_state['usuario']

    with st.expander('Dias para solicitar'):
        dias_para_solicitar = usuario.dias_para_solicitar()
        st.markdown(f'O usuário {usuario.nome} possui **{dias_para_solicitar}** dias para solicitar')
    if not 'ultimo_clique' in st.session_state:
        st.session_state['ultimo_clique'] = 'ultimo_clique'


    calendar_widget = calendar(events=calendar_events, options=calendar_options)

    if 'callback' in calendar_widget and calendar_widget['callback'] == 'dateClick':

        row_date = calendar_widget['dateClick']['date']
        if row_date != st.session_state['ultimo_clique']:
            st.session_state['ultimo_clique'] = row_date

            date = calendar_widget['dateClick']['date'].split('T')[0]
            st.write(date)
            if not 'data_inicio' in st.session_state:
                st.session_state['data_inicio'] = date
                st.warning(f'Data de início de férias solicitada {date}')
            else:
                st.session_state['data_final'] = date
                data_inicio = st.session_state['data_inicio']
                cols = st.columns([0.7, 0.3])
                with cols[0]:
                    st.warning(f'Data de início de férias solicitada {data_inicio}')
                with cols[1]:
                    st.button('Limpar', use_container_width=True, on_click=limpa_datas())
                cols = st.columns([0.7, 0.3])
                with cols[0]:
                    st.warning(f'Data final de férias solicitada {date}')
                with cols[1]:
                    st.button('Adicionar Férias',
                              use_container_width=True,
                              on_click=verifica_e_adiciona_ferias,
                              args=(data_inicio, date)
                              )


