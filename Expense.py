import streamlit as st
import json
import os

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="icon.png",
    layout="centered",
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

# Function to remove an expense
def remove_expense(username, item_name):
    user_data = load_user_data(username)
    user_data['expenses'] = [expense for expense in user_data['expenses'] if expense['name'] != item_name]
    save_user_data(username, user_data)

# Function to clear all expenses
def clear_expenses(username):
    user_data = load_user_data(username)
    user_data['expenses'] = []
    save_user_data(username, user_data)

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

st.sidebar.title('Expense Tracker')

# Registration form
if st.sidebar.button('Register'):
    st.session_state.page = 'Register'

# Login form
if st.sidebar.button('Login'):
    st.session_state.page = 'Login'

if st.session_state.get('page') == 'Register':
    st.subheader('Register')
    new_username = st.text_input('New Username', key='register_username')
    new_password = st.text_input('New Password', type='password', key='register_password')
    if st.button('Register', key='register_button'):
        if new_username and new_password:
            if os.path.exists(os.path.join(USER_DATA_DIR, f"{new_username}.json")):
                st.error('Username already exists. Please choose a different username.')
            else:
                register_user(new_username, new_password)
                st.success('Registration successful! You can now login.')
                st.session_state.page = 'Login'

if st.session_state.get('page') == 'Login':
    st.subheader('Login')
    username = st.text_input('Username', key='login_username')
    password = st.text_input('Password', type='password', key='login_password')
    if st.button('Login', key='login_button'):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.current_user = username
            st.success('Login successful!')
            st.session_state.page = 'Add Expense'
        else:
            st.session_state.authenticated = False
            st.error('Invalid username or password. Please try again.')

if st.session_state.get('page') == 'Add Expense' and st.session_state.get('authenticated'):
    st.subheader('Add Expense')
    item_name = st.text_input('Item Name', key='item_name')
    item_amount = st.text_input('Item Amount (₹)', key='item_amount')
    
    if st.button('Add Expense', key='add_expense'):
        add_expense(st.session_state.current_user, item_name, item_amount)

    if st.button('Clear All', key='clear_all'):
        clear_expenses(st.session_state.current_user)

    user_data = load_user_data(st.session_state.current_user)
    total_amount = sum(expense['amount'] for expense in user_data.get('expenses', []))

    st.write('## Expenses')
    for expense in user_data.get('expenses', []):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"{expense['name']}: ₹{expense['amount']}")
        with col3:
            if st.button("🗑️", key=f"remove_{expense['name']}"):
                remove_expense(st.session_state.current_user, expense['name'])
                st.experimental_rerun()

    st.write(f'## Total: ₹{total_amount}')
elif st.session_state.get('authenticated') is False:
    st.warning('Please login to access the expense tracker.')
