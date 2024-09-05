import streamlit as st
from utils import book_spaces
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from datetime import datetime, timedelta

ss = st.session_state
st.set_page_config(layout='wide')


def stop_booking():
    time.sleep(2)
    st.write("Stopped Booking!")


# link up streamlit and css
folder_path = os.path.dirname(__file__)
cssfile_path = os.path.join(folder_path, "styles.css")
with open(cssfile_path) as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# sidebar
with st.sidebar:
    st.divider()
    st.write("## About xxx Booking Bot")
    st.write("version 1.0") 
    st.write("""This web application books xxx spaces via [xxx website](https://google.com/xxx). """)
    st.write("Made by xxx.") 
    st.divider()
    st.write("## Table Arrangement")
    st.image('xxx.png', width=300)
    st.divider()

# Main Page
st.markdown('<p class="main-header-text">Book xxx Spaces</p>', unsafe_allow_html=True)

st.write("Enter the information below: ")

start_date = st.date_input("Enter booking start date:", datetime.now())

end_date = st.date_input("Enter booking end date (LIMIT to 3 months from now):", datetime.now())

st.write("Choose the day of week:")
book_mon = st.checkbox("Monday")
book_tue = st.checkbox("Tuesday")
book_wed = st.checkbox("Wednesday")
book_thu = st.checkbox("Thursday")
book_fri = st.checkbox("Friday")
book_sat = False
book_sun = False
day_of_week_pref = [book_mon,
                    book_tue,
                    book_wed,
                    book_thu,
                    book_fri,
                    book_sat,
                    book_sun]

start_time = st.selectbox(
    "Choose the booking start time:",
    ("08:30", "09:00", "09:30","10:00"),
)

table_pref = st.multiselect(
    "Choose the table number you want to book in order of preference:",
    [x for x in reversed(range(1,24)) if (x != 17) and (x!=18)],
    [23,1],
)

show_table_layout = st.toggle("Show Table Layout?", False)
if show_table_layout:
    st.image('xxx.png', width=400)

is_god_mode = st.toggle("Activate GOD mode?", False)
if is_god_mode:
    st.write("GOD mode activated!")
    
st.divider()
st.write("Enter your login details below: ")
st.text_input('email', key='email', 
    placeholder='Enter your xxx email address: ', 
    help='', label_visibility="collapsed", disabled = False)

st.text_input('vcode', key='vcode', 
    placeholder='Enter your verification code: ', 
    help='', label_visibility="collapsed", disabled = False)

c1,c2= st.columns([1,4])

if c1.button('Book!', disabled=False):
   with st.spinner('Booking now...'):
      email = ss.get('email')
      vcode = ss.get('vcode')

      book_spaces(table_pref, start_date, end_date, day_of_week_pref, start_time, is_god_mode, email, vcode)

if c2.button("Stop"):
    with st.spinner('Stopping now...'):
        stop_booking()

