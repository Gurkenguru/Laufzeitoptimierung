import streamlit as st
from classes import Portfolio
from shared import portfolios
from st_pages import Page

st.title("🆕 Create a New Portfolio")

def add_row():
    if 'rows' not in st.session_state:
        st.session_state.rows = [{'ticker': '', 'weight': 0.0}]
    else:
        st.session_state.rows.append({'ticker': '', 'weight': 0.0})

def remove_row(index):
    if 'rows' in st.session_state and len(st.session_state.rows) > 0:
        st.session_state.rows.pop(index)

def create_portfolio_list():
    portfolio_list = [(row['ticker'], row['weight']) for row in st.session_state.rows]
    portfolios.append(Portfolio(entries = portfolio_list, average = average, name = name))
    """# Join each tuple into a string and then join all strings into one to display
    portfolio_list_str = ', '.join([f"('{ticker}', {weight})" for ticker, weight in portfolio_list])
    st.text(f"[{portfolio_list_str}]")"""


name = st.text_input(label = "What should your portfolio be called?")
average = st.text_input(label = "How many trading days should the SMA include?")

if 'rows' not in st.session_state:
    add_row()

for index, row in enumerate(st.session_state.rows):
    cols = st.columns([3, 3, 1])
    with cols[0]:
        st.session_state.rows[index]['ticker'] = st.text_input("Ticker Symbol", value=row['ticker'], key=f"ticker_{index}")
    with cols[1]:
        st.session_state.rows[index]['weight'] = st.number_input("Weight in %", value=1.0, min_value=0.01, max_value=100.0, format="%f", key=f"weight_{index}")
    with cols[2]:
        st.button("Remove Row", on_click=lambda index=index: remove_row(index), key=f"remove_{index}")

st.button("Add Row", on_click=add_row)

# Automatic total weight check after each change
total_weight = sum(row['weight'] for row in st.session_state.rows)
if total_weight == 100:
    st.success("Total weight is exactly 100%")
    # Display the button for creating a portfolio list when the total weight is exactly 100%
    if st.button("Create Portfolio List"):
        create_portfolio_list()
        Page(add_prefix("portfolios"), "My Allocations", "📊")
elif total_weight < 100:
    st.warning(f"Total weight is less than 100% ({total_weight}%)")
else:
    st.error(f"Total weight exceeds 100% ({total_weight}%)")
