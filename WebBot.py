#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, sys, itertools, pickle, getpass
import pandas as pd

# login to myasu using name and passowrd
def login(usr_name, pw, browser):
    browser.find_element('id', 'rememberid').click()
    login = browser.find_element('id',"username")
    login.send_keys(usr_name)
    login = browser.find_element('id','password')
    login.send_keys(pw)
    login.submit()

# Check if input is float or int and then return it
# returns None if neither is true
def input_type(value):
    try:
        num = int(value)
        return num
    except ValueError:
        try:
            num = float(value)
            return num
        except:
            pass
    return None

def confirm_enrollment(wait):
    enroll = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="DERIVED_SSR_FL_SSR_ENROLL_FL"]')))
    enroll.click()
    confirm_enrollment = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="#ICYes"]')))
    confirm_enrollment.click()

def cart_term_confirm(wait):
     # accessing the cart and confirming the term
    shop_cart = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="win2divSCC_LO_FL_WRK_SCC_GROUP_BOX_1$0"]')))
    shop_cart.click()
    term_choice = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="GRID_TERM_SRC5$0_row_0"]/td')))
    term_choice.click()

def get_to_cart(browser, wait):
    browser.get('https://webapp4.asu.edu/myasu/')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="classes-link-4"]')))
    browser.get('https://webapp4.asu.edu/myasu/?action=addclass&strm')
    

        

        
# Enter and check the correct command line args
if len(sys.argv) <= 1:
    print('\nUsage: ./WebBot.py [Search for classes: y/N]')
    print('\nExiting program...')
    sys.exit(1)
else:
    print('\n\tWelcome To The RegBOT\n\tInitializing Web Browser...')
    period_in_min = input('Enter time period to wait between trials (in minutes): ')
    period_in_min = input_type(period_in_min) 
    period_in_sec = period_in_min * 60
    
    repeat_times = input("Enter the number of Trials: ") 
    repeat_times = input_type(repeat_times)
    repeat_times = round(repeat_times)
    
# check if need to search for classes or not
arg1 = sys.argv[1].upper()
if arg1 == 'Y':
    class_search = True
    df = pd.read_csv('classes.csv')
    df_subjects = df.iloc[0:,0].values.tolist()
    df_class_num = df.iloc[0:,1].values.tolist()
    df_section_num = df.iloc[0:,2].values.tolist()
    df_instructor_last = df.iloc[0:,3].values.tolist()
    
elif arg1 == 'N':
    class_search = False
    print('choose from the below options: ')
    print('\t1. Enroll in classes in "classes.csv" file.')
    print('\t2. Input clasees that you want to enroll in.')
    print('\t3. Enroll in all classes.')

    classes_search_source = input()
    classes_search_source = input_type(classes_search_source)
    while classes_search_source > 3 or classes_search_source < 1:
        print('[-]Invalid input, please Enter a number between 1-3')
        classes_search_source = input()
        
    # Using the CSV file to confirm enrollment in classes
    if classes_search_source == 1:
        df = pd.read_csv('classes.csv')
        df_class_num = df.iloc[0:,1].values.tolist()
        df_section_num = df.iloc[0:,2].values.tolist()
        
    # Using user input to confirm enrollment in classes
    elif classes_search_source == 2:
        raise NotImplementedError('This functionality is not implemented yet!')
    
    # Enroll in all classes that are present in student cart
    else:
        print('Enrolling in all classes...')
        print('Sit down, watch, and have fun :)')

else:
    print('Input should be "Y/y" or "N/n" with no quotation marks!\n\tProgram is Exiting')
    sys.exit(1)

# prompting for user information
user_name = input("Enter your ASURITE User ID: ")
pw = getpass.getpass("Enter your Password: ")


browser  = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get('https://webapp4.asu.edu/myasu/')

login(user_name,pw, browser)

wait = WebDriverWait(browser,60)


# Choice if adding classes
if class_search:
    # Choose the correct term
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="classes-link-4"]')))
    element.click()
    element = browser.find_element(By.XPATH, '//a[contains(@href,"?action=clearschedcache&nextUrl=https%3A%2F%2Fcatalog.apps.asu.edu%2Fcatalog%2Fclasses%2Fclasslist%3Fterm%3D2237")]')
    element.click()
    time.sleep(3)
    signed_up = len(df_class_num)
    
# loop that will repeats at given interval
    for i in range(signed_up):
            
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div/input')))
        subject_box = browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div/input')
        subject_box.click()
        print(len(df_subjects))
        subject_box.send_keys(df_subjects[0])
        df_subjects.pop(0)

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="catalogNbr"]')))
        number = browser.find_element(By.XPATH, '//*[@id="catalogNbr"]')
        number.click()
        number.send_keys(df_class_num[0])
        df_class_num.pop(0)
        browser.find_element(By.XPATH, '//*[@id="search-button"]').click()
        class_to_search = df_section_num[0]
        df_section_num.pop(0)

        classes_list = browser.find_element(By.CSS_SELECTOR, "div:nth-child(5)")
        time.sleep(2)
        odd_items = classes_list.find_elements(By.XPATH, '//div[@class="class-accordion odd"]')
        even_items = classes_list.find_elements(By.XPATH, '//div[@class="class-accordion even"]')
        for (odd_item, even_item) in itertools.zip_longest(odd_items, even_items):
            title1 = None
            title2 = None
            try:
                # class_name1 = odd_item.find_element(By.XPATH, 'div[2]/span').text
                title1 = odd_item.find_element(By.XPATH, 'div[4]').text
            except:
                pass
            
            try:
                # class_name2 = even_item.find_element(By.XPATH, 'div[2]/span').text
                title2 = even_item.find_element(By.XPATH, 'div[4]').text
            except:
                pass 
            

            if class_to_search == int(title1) and odd_item:
                print("found Class ", title1)
                try:
                    adding = odd_item.find_element(By.XPATH, 'div[17]')
                    # print(title1 ,adding1.text)
                except:
                    try:
                        adding = odd_item.find_element(By.XPATH, 'div[16]')
                    except:
                        adding= odd_item.find_element(By.XPATH, 'div[15]')
                adding.click()
                break
            
            elif even_item and class_to_search == int(title2):
                print("found Class ", title2)
                try:
                    adding = odd_item.find_element(By.XPATH, 'div[17]')
                    # print(title1 ,adding1.text)
                except:
                    try:
                        adding = odd_item.find_element(By.XPATH, 'div[16]')
                    except:
                        adding = odd_item.find_element(By.XPATH, 'div[15]')
                adding.click()
                break
            
            else:
                print('Class is Not found!')
            
        add_to_cart = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ASU_ADDCLAS_WRK_ADD_BTN"]')))
        add_to_cart.click()
        
        browser.get('https://catalog.apps.asu.edu/catalog/classes/classlist')
        time.sleep(3)
    

    get_to_cart(browser, wait)
    cart_term_confirm(wait)
    confirm_enrollment(wait)
        
        
        # time.sleep(period_in_sec)
        
        
# Choice if not adding classes 
while not class_search:
    if classes_search_source == 1:
        # Accessing the class registration page
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="classes-link-4"]')))
        browser.get('https://webapp4.asu.edu/myasu/?action=addclass&strm')
        
        cart_term_confirm(wait)
    
        # get_to_cart(browser, wait) TODO::###
        
        counter = 0
        while True:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="win1divSSR_REGFORM_VW$grid$0"]/table/tbody')))
            classes_list = browser.find_element(By.XPATH, '//*[@id="win1divSSR_REGFORM_VW$grid$0"]/table/tbody')
        
            # Uncheck the classes that are not wanted using class and section numbers
            items = classes_list.find_elements(By.TAG_NAME, 'tr')
            for item in items:
                _, class_num, _ = item.find_element(By.XPATH, 'td[4]').text.split(maxsplit=2)
                section, _ = item.find_element(By.XPATH, 'td[3]').text.split(maxsplit=1)
                if (int(class_num) not in df_class_num) or (int(section) not in df_section_num):
                    checkbox = item.find_element(By.XPATH, 'td[1]/div/div/div/input')
                    checkbox.click()
                    
                    
            confirm_enrollment(wait)
            class_stat = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="win1divDERIVED_REGFRM1_SS_MESSAGE_LONG$0"]/div')))
            time.sleep(period_in_sec)
            if 'is full' in class_stat.text and counter < repeat_times:
                shop_cart = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="win2divSCC_LO_FL_WRK_SCC_GROUP_BOX_1$0"]')))
                shop_cart.click()
                counter += 1
            else:
                break
                    
                    
    elif classes_search_source == 2:
        pass
    
    elif classes_search_source == 3:
        # Accessing the class registration page
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="classes-link-4"]')))
        browser.get('https://webapp4.asu.edu/myasu/?action=addclass&strm')
        cart_term_confirm(wait) 

        counter = 0
        while True:             
            confirm_enrollment(wait)
            class_stat = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="win1divDERIVED_REGFRM1_SS_MESSAGE_LONG$0"]/div')))
            time.sleep(period_in_sec)
            if 'is full' in class_stat.text and counter < repeat_times:
                shop_cart = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="win2divSCC_LO_FL_WRK_SCC_GROUP_BOX_1$0"]')))
                shop_cart.click()
                counter += 1
            else:
                break
    
    
print('GoodBey')
