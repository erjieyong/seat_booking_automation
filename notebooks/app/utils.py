import streamlit as st
	
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def book_spaces(table_pref, start_date, end_date, day_of_week_pref, start_time, is_god_mode, email, vcode):
    
    # updated for Chrome - headless implementation
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("window-size=1888,836")

    ########## added & updated for Docker implementation
    # https://stackoverflow.com/questions/72254697/how-can-i-get-selenium-chrome-driver-using-python-running-in-docker/78678053#78678053
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    print(f"window size: {driver.get_window_size()}")
    driver.get("https://google.com/xxx")
    

    # updated table coordinates
    # updated to include CONSTANT DELAYTIME to support delayed clicking of timeslots
    
    # translate month to number
    month_text2no = {"January": 1,
                     "February": 2,
                     "March": 3,
                     "April": 4,
                     "May": 5,
                     "June": 6,
                     "July": 7,
                     "August": 8,
                     "September": 9,
                     "October": 10,
                     "November": 11,
                     "December": 12
    }
    shortmonth_text2no = {"Jan": 1,
                          "Feb": 2,
                          "Mar": 3,
                          "Apr": 4,
                          "May": 5,
                          "Jun": 6,
                          "Jul": 7,
                          "Aug": 8,
                          "Sep": 9,
                          "Oct": 10,
                          "Nov": 11,
                          "Dec": 12
    }

    time_slots = {
        'am':[
            '08:30 - 09:00',
            '09:00 - 09:30',
            '09:30 - 10:00',
            '10:00 - 10:30',
            '10:30 - 11:00',
            '11:00 - 11:30',
            '11:30 - 12:00',
            '12:00 - 12:30',
        ],
        'pm':[
            '14:00 - 14:30',
            '14:30 - 15:00',
            '15:00 - 15:30',
            '15:30 - 16:00',
            '16:00 - 16:30',
            '16:30 - 17:00',
            '17:00 - 17:30',
        ]
    }
    
    start_times = ["08:30", "09:00", "09:30","10:00"]
    if is_god_mode == False:
        for idx in range(len(start_times)):
            if start_times[idx] == start_time:
                time_slots['am'] = time_slots['am'][idx:]

    tables_cood = {
        1: [68,162],
        2: [68,186],
        3: [68,218],
        4: [68,247],
        5: [145,161],
        6: [145,189],
        7: [145,216],
        8: [145,243],
        9: [162,163],
        10: [162,187],
        11: [162,214],
        12: [162,244],
        13: [102, 312],
        14: [130, 312],
        15: [158, 312],
        16: [102, 329],
    #     17:
    #     18:
        19: [260, 257], 
        20: [288, 257],
        21: [316, 257],
        22: [280, 326],
        23: [297, 326],
    }


    DELAY=2
    MID_DELAY=5
    LONG_DELAY=40

    try:
        # updated to automate closing of pop-ups/overlay (x2) when webpage initially loads
        # longer allowable delay to let website load fully
        
        time.sleep(5)
        
        # try to close overlay #1 and #2
        try:
            close_button1 = WebDriverWait(driver, MID_DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, "path[d='M30.7458 21.4295C31.0702 21.105 31.0702 20.579 30.7458 20.2545C30.4213 19.93 29.8952 19.93 29.5708 20.2545L25.4999 24.3253L21.4291 20.2545C21.1046 19.93 20.5786 19.93 20.2541 20.2545C19.9296 20.579 19.9296 21.105 20.2541 21.4295L24.3249 25.5003L20.2541 29.5712C19.9296 29.8956 19.9296 30.4217 20.2541 30.7462C20.5786 31.0706 21.1046 31.0706 21.4291 30.7462L25.4999 26.6753L29.5708 30.7462C29.8952 31.0706 30.4213 31.0706 30.7458 30.7462C31.0702 30.4217 31.0702 29.8956 30.7458 29.5712L26.6749 25.5003L30.7458 21.4295Z']")))
            close_button1.click()
        except:
            st.write("WARNING: Overlay #1 not found.")
            pass
        
        try: 
            close_button2 = WebDriverWait(driver, MID_DELAY).until(EC.presence_of_element_located((By.XPATH, f"//button[contains(text(), 'Got it!')]")))
            close_button2.click()
        except:
            st.write("WARNING: Overlay #2 not found.")
            pass

        # updated to automate login (email + verification code)
        # longer allowable delay to let website load fully
        login_button = WebDriverWait(driver, LONG_DELAY).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Log In')]")))
        action = ActionChains(driver).move_to_element(login_button).click()
        action.perform()

        # login page (email only)
        email_field = WebDriverWait(driver, LONG_DELAY).until(EC.presence_of_element_located((By.NAME, "loginfmt")))
        email_field.send_keys(email)
        
        next_button = WebDriverWait(driver, LONG_DELAY).until(EC.presence_of_element_located((By.ID, "idSIButton9")))
        next_button.click()

        # main login page (email + verification code)
        vcode_field = WebDriverWait(driver, LONG_DELAY).until(EC.presence_of_element_located((By.NAME, "VerificationCode")))
        vcode_field.send_keys(vcode)
        sign_in_button = WebDriverWait(driver, LONG_DELAY).until(EC.presence_of_element_located((By.NAME, "SignIn")))
        sign_in_button.click()
        
    except:
        st.write(f"Login Failed.")
        return

    
    # updated table input to table_preference input
    # updated to include for-loop to scan through all tables (in order of table preference)
    # updated to include GOD mode to book seat for ALL individual time slot (instead of AM/PM bulk booking)
    # updated to include support for delayed clicking of timeslots ("time_slots")

    booking_dates = get_booking_dates(start_date, end_date, day_of_week_pref)

    if is_god_mode == True:
        time_slots['am'] = time_slots['am'] \
                            + ['12:30 - 13:00',
                              '13:00 - 13:30',
                              '13:30 - 14:00',
                              ]
        time_slots['pm'] = time_slots['pm'] \
                            + ['17:30 - 18:00',
                              '18:00 - 18:30',
                              ]
        
    failed_dates = []
    for date in booking_dates[:]:
        for ampm in ['am', 'pm']:
            if is_god_mode == True:
                for time_slot in time_slots[ampm]:
                    target_date = date
                    target_mth = shortmonth_text2no[target_date[:3]]

                    driver.get("https://google.com/xxx/Book-a-Space")
                    time.sleep(1)
                    # click on Do some quiet work
                    driver.find_element(By.CSS_SELECTOR,'button[id="Do some quiet work"]').send_keys(Keys.RETURN)
                    time.sleep(1)
                    # click on Next
                    driver.find_element(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]').send_keys(Keys.RETURN)
                    time.sleep(1)
                    # check current default month
                    current_month = driver.find_element(By.CSS_SELECTOR,'div[class*="css-1v994a0"]').text
                    month_text2no[current_month]
                    time.sleep(0.5)

                    # press the next month button depending on how many times it is away from our target_mth
                    for i in range(target_mth-month_text2no[current_month]):
                        driver.find_element(By.CSS_SELECTOR,'button[title="Next month"]').send_keys(Keys.RETURN)
                    time.sleep(0.75)

                    try:
                        # press the date
                        driver.find_element(By.CSS_SELECTOR,f'button[aria-label="{target_date}"]').send_keys(Keys.RETURN)
                        time.sleep(0.5)

                        # click on Next
                        driver.find_element(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]').send_keys(Keys.RETURN)
                        time.sleep(0.5)

                        # Select individual time slot
                        selected_time_slot = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{time_slot}')]")))
                        driver.execute_script("arguments[0].scrollIntoView();", selected_time_slot)
                        selected_time_slot.send_keys(Keys.RETURN)

                        # click on Next
                        driver.find_element(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]').send_keys(Keys.RETURN)
                        time.sleep(1.5)

                        # try selecting seat
                        for table in table_pref:
                            try:
                                js_script = f"""
                                var stage = Konva.stages[0];  // Get the first Konva Stage

                                // Get the shape at the current position
                                var shape = stage.getIntersection({{x: {tables_cood[table][0]}, y: {tables_cood[table][1]}}});

                                if (shape) {{
                                    // Simulate a click on the shape
                                    shape.fire('click');
                                    // return "Clicked at (" + 160 + ", " + 380 + ")";
                                }}
                                """
                                output = driver.execute_script(js_script)
                                time.sleep(1)
                                
                                has_selected_seat = check_seat_selection(driver)
                                if (has_selected_seat):
                                    # click on Book
                                    driver.find_element(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]').send_keys(Keys.RETURN)
                                    time.sleep(1)

                                    # Confirm booking by clicking on the 2nd button
                                    # driver.get_screenshot_as_file("screenshot0.png")
                                    confirm_booking_button = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Confirm and Book')]")))
                                    confirm_booking_button.click()
                                    time.sleep(1)

                                    # confirm
                                    driver.find_elements(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]')[1].send_keys(Keys.RETURN)
                                    time.sleep(1)
                                    st.write(f"Booked table {table} on {target_date}, {time_slot}{ampm} successfully")
                                    break # remove break if wish to book ALL tables in table_pref
                                else:
                                    st.write(f"Unable to book for {target_date}, {time_slot}{ampm}. Table {table} not available for booking")
                                    failed_dates.append(target_date + ' ' + time_slot + ' ' + ampm)
                                    
                            except:
                                st.write(f"Unable to book for {target_date}, {time_slot}{ampm}. Table {table} not available for booking")
                                failed_dates.append(target_date + ' ' + time_slot + ' ' + ampm)

                    except:
                        st.write(f"Unable to book for {target_date}, {time_slot}{ampm}. Date not available for booking.")
                        failed_dates.append(target_date + ' ' + time_slot + ' ' + ampm)
                        pass
                    
            elif is_god_mode == False:
                target_date = date
                target_mth = shortmonth_text2no[target_date[:3]]

                driver.get("https://google.com/xxx/Book-a-Space")
                time.sleep(1)
                # click on Do some quiet work
                driver.find_element(By.CSS_SELECTOR,'button[id="Do some quiet work"]').send_keys(Keys.RETURN)
                time.sleep(1)
                # click on Next
                driver.find_element(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]').send_keys(Keys.RETURN)
                time.sleep(1)
                # check current default month
                current_month = driver.find_element(By.CSS_SELECTOR,'div[class*="css-1v994a0"]').text
                month_text2no[current_month]
                time.sleep(0.5)

                # press the next month button depending on how many times it is away from our target_mth
                for i in range(target_mth-month_text2no[current_month]):
                    driver.find_element(By.CSS_SELECTOR,'button[title="Next month"]').send_keys(Keys.RETURN)
                time.sleep(0.75)

                try:
                    # press the date
                    driver.find_element(By.CSS_SELECTOR,f'button[aria-label="{target_date}"]').send_keys(Keys.RETURN)
                    time.sleep(0.5)

                    # click on Next
                    driver.find_element(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]').send_keys(Keys.RETURN)
                    time.sleep(0.5)

                    # Select AM or PM time slot. 
                    for time_slot in time_slots[ampm]:
                        selected_time_slot = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{time_slot}')]")))
                        driver.execute_script("arguments[0].scrollIntoView();", selected_time_slot)
                        selected_time_slot.send_keys(Keys.RETURN)

                    # click on Next
                    driver.find_element(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]').send_keys(Keys.RETURN)
                    time.sleep(1.5)

                    # try selecting seat
                    for table in table_pref:
                        try:
                            js_script = f"""
                            var stage = Konva.stages[0];  // Get the first Konva Stage

                            // Get the shape at the current position
                            var shape = stage.getIntersection({{x: {tables_cood[table][0]}, y: {tables_cood[table][1]}}});

                            if (shape) {{
                                // Simulate a click on the shape
                                shape.fire('click');
                                // return "Clicked at (" + 160 + ", " + 380 + ")";
                            }}
                            """
                            output = driver.execute_script(js_script)
                            time.sleep(1)
                            
                            has_selected_seat = check_seat_selection(driver)
                            if (has_selected_seat):
                                # click on Book
                                driver.find_element(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]').send_keys(Keys.RETURN)
                                time.sleep(1)

                                # Confirm booking by clicking on the 2nd button
                                # driver.get_screenshot_as_file("screenshot0.png")
                                confirm_booking_button = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Confirm and Book')]")))
                                confirm_booking_button.click()
                                time.sleep(1)

                                # confirm
                                driver.find_elements(By.CSS_SELECTOR,'button[class*="w-full h-full py-4 px-5 txt-MontserratExtraBold"]')[1].send_keys(Keys.RETURN)
                                time.sleep(1)
                                st.write(f"Booked table {table} on {target_date}, {ampm} successfully")
                                break # remove break if wish to book ALL tables in table_pref
                            else:
                                st.write(f"Unable to book for {target_date}, {ampm}. Table {table} not available for booking")
                                failed_dates.append(target_date + ' ' + ampm)
                        except:
                            st.write(f"Unable to book for {target_date}, {ampm}. Table {table} not available for booking")
                            failed_dates.append(target_date + ' ' + ampm)

                except:
                    st.write(f"Unable to book for {target_date}, {ampm}. Date not available for booking.")
                    failed_dates.append(target_date + ' ' + ampm)
                    pass


    st.write("BOOKING DONE!")
    driver.quit()



def get_booking_dates(start_date, end_date, day_of_week_pref):

   from datetime import datetime, timedelta

   # Initialize the current date to start date
   current_date = start_date

   # Initialize a list to store the dates
   booking_dates = []

   # Iterate over the dates from start to end
   while current_date <= end_date:
       # Get the weekday (0 is Monday, 1 is Tuesday, 2 is Wednesday)
       if day_of_week_pref[current_date.weekday()] == True:
    #    if current_date.weekday() <= 2:  # Monday, Tuesday, or Wednesday
           # Append the date in the specified format
           booking_dates.append(current_date.strftime("%b %-d, %Y"))
       # Move to the next day
       current_date += timedelta(days=1)

   return booking_dates


def check_seat_selection(driver):
# updated to include function to detect if seat is selected 
   try:
       driver.find_element(By.XPATH,'//div[contains(text(), "Selected Seat")]')
       has_selected_seat = True
       
   except: 
       has_selected_seat = False
       
   return has_selected_seat


