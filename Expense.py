import streamlit as st
import json
import os
import uuid

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="icon.png",
    layout="wide",
)

# Directory to store user data
USER_DATA_DIR = 'user_data'

# Create directory if it doesn't exist
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

# Function to load user data
def load_user_data(username):
    user_data_file = os.path.join(USER_DATA_DIR, f"{username}.json")
    if os.path.exists(user_data_file):
        try:
            with open(user_data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

# Function to save user data
def save_user_data(username, data):
    user_data_file = os.path.join(USER_DATA_DIR, f"{username}.json")
    with open(user_data_file, 'w') as f:
        json.dump(data, f)

# Function to authenticate user
def authenticate_user(username, password):
    user_data = load_user_data(username)
    return user_data.get('password') == password

# Function to register new user
def register_user(username, password):
    user_data = {'password': password, 'expenses': []}
    save_user_data(username, user_data)

# Function to add an expense
def add_expense(username, item_name, item_amount):
    user_data = load_user_data(username)
    if item_name and item_amount:
        user_data['expenses'].append({'name': item_name, 'amount': float(item_amount)})
        save_user_data(username, user_data)

# Function to remove selected expenses
def remove_expense(username, item_name):
    user_data = load_user_data(username)
    user_data['expenses'] = [expense for expense in user_data['expenses'] if expense['name'] != item_name]
    save_user_data(username, user_data)

# Function to clear all expenses
def clear_expenses(username):
    user_data = load_user_data(username)
    user_data['expenses'] = []
    save_user_data(username, user_data)

st.sidebar.title('Expense Tracker')

# Main content area
if 'page' not in st.session_state:
    st.session_state.page = 'Login'

if st.session_state.page == 'Register':
    st.subheader('Register')
    new_username = st.text_input('New Username')
    new_password = st.text_input('New Password', type='password')
    if st.button('Register'):
        if new_username and new_password:
            if os.path.exists(os.path.join(USER_DATA_DIR, f"{new_username}.json")):
                st.error('Username already exists. Please choose a different username.')
            else:
                register_user(new_username, new_password)
                st.success('Registration successful! You can now login.')
                st.session_state.page = 'Login'
        else:
            st.error('Please enter both username and password.')

elif st.session_state.page == 'Login':
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.success('Login successful!')
            st.session_state.page = 'Add Expense'
        else:
            st.session_state.authenticated = False
            st.error('Invalid username or password. Please try again.')

if st.session_state.page == 'Add Expense':
    if st.session_state.authenticated:
        if 'expenses' not in st.session_state:
            st.session_state.expenses = []

        st.subheader('Add Expense')
        item_name = st.text_input('Item Name')
        item_amount = st.text_input('Item Amount (₹)')

        if st.button('Add Expense'):
            add_expense(username, item_name, item_amount)

        if st.button('Clear All'):
            clear_expenses(username)

        user_data = load_user_data(username)
        total_amount = sum(expense['amount'] for expense in user_data.get('expenses', []))

        st.write('## Expenses')
        selected_expense = st.selectbox('Select expense to remove', [''] + [expense['name'] for expense in user_data.get('expenses', [])])
        if st.button('Remove Expense') and selected_expense:
            remove_expense(username, selected_expense)

        for expense in user_data.get('expenses', []):
            st.write(f"{expense['name']}: ₹{expense['amount']}")

        st.write(f'## Total: ₹{total_amount}')
    else:
        st.warning('Please login to access the expense tracker.')
