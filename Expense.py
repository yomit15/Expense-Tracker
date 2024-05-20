import streamlit as st
import json
import os
import uuid

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="icon.png",
    layout="centered",
)

# File to save the expenses
EXPENSE_FILE = 'expenses.json'

# Load expenses from file
@st.cache(allow_output_mutation=True)
def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

# Save expenses to file
def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(expenses, f)

# Function to clear all expenses for a new session
def clear_expenses():
    return []

# Initialize session state for expenses if it doesn't exist
if 'expenses' not in st.session_state:
    st.session_state.expenses = clear_expenses()

# Generate a unique session ID if it doesn't exist
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Function to add an expense
def add_expense(item_name, item_amount):
    if item_name and item_amount:
        st.session_state.expenses.append({'name': item_name, 'amount': float(item_amount)})
        save_expenses(st.session_state.expenses)

st.title('EXPENSE TRACKER')

item_name = st.text_input('Item Name')
item_amount = st.text_input('Item Amount (₹)')

if st.button('Add Expense'):
    add_expense(item_name, item_amount)

if st.button('Clear All'):
    st.session_state.expenses = clear_expenses()

total_amount = sum(expense['amount'] for expense in st.session_state.expenses)

st.write('## Expenses')
for expense in st.session_state.expenses:
    st.write(f"{expense['name']}: ₹{expense['amount']}")

st.write(f'## Total: ₹{total_amount}')
