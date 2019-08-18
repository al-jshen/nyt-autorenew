from selenium import webdriver
from time import sleep

# TPL card number and pin, Gmail and password
CARDNUM = ''
CARDPIN = ''
EMAIL = ''
PASSWORD = ''

driver = webdriver.Chrome()

# Access TPL site for NYT access
driver.get('https://www.torontopubliclibrary.ca/detail.jsp?Entt=RDMEDB0202&R=EDB0202')
driver.find_element_by_css_selector('.button.access-online.clear-left').click()

# Log in to TPL
driver.find_element_by_id('userId').send_keys(CARDNUM)
pin = driver.find_element_by_id('password')
pin.send_keys(CARDPIN)
pin.submit()

driver.find_element_by_css_selector('.button.submit.access-online').click()
driver.find_element_by_partial_link_text('Log in here').click()

# Save current window because there will be a popup
main_page = driver.current_window_handle

# Authenticate with Google instead of NYT account to avoid captcha
driver.find_element_by_id('js-google-oauth-login').click()

sleep(1.5)

# Switch to popup
for handle in driver.window_handles:
    if handle != main_page:
        login_page = handle
        break
driver.switch_to.window(login_page)

# Log in to Google
driver.find_element_by_id('identifierId').send_keys(EMAIL)
driver.find_element_by_css_selector('.RveJvd.snByac').click()
sleep(1)
driver.find_element_by_name('password').send_keys(PASSWORD)
driver.find_element_by_css_selector('.RveJvd.snByac').click()

# Switch back to main page
driver.switch_to.window(main_page)

# Wait for authentication to go through, then quit
while True:
    links = driver.find_elements_by_link_text('Go to NYTimes.com')
    if len(links) == 0:
        sleep(0.25)
    else:
        sleep(0.1)
        driver.quit()
        break

