import json
import streamlit as st
from streamlit_calendar import calendar

with open('calendar_options.json') as f:
    calendar_options = json.load(f)

if not 'ultimo_clique' in st.session_state:
    st.session_state['ultimo_clique'] = 'ultimo_clique'

calendar_events = [
    {
        "title": "Férias do Fulano",
        "start": "2024-01-01T08:30:00",
        "end": "2024-02-01T10:30:00",
        "resourceId": "a",
    },

]
custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

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
                if st.button('Limpar', use_container_width=True):
                    del st.session_state['data_inicio']
                    del st.session_state['data_final']
                    st.rerun()
            cols = st.columns([0.7, 0.3])
            with cols[0]:
                st.warning(f'Data final de férias solicitada {date}')
            with cols[1]:
                st.button('Adicionar Férias', use_container_width=True)


st.write(calendar_widget)