from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

def slow_type(element, text, delay=0.2):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

# Set up Selenium WebDriver (make sure chromedriver is in your PATH)
driver = webdriver.Chrome(executable_path='chromedriver.exe')

# Go to Facebook login page
driver.get('https://www.facebook.com/login')
time.sleep(3)

# Enter your credentials here
username = ""
password = ""

# Find and fill the email field
email_elem = driver.find_element(By.ID, 'email')
slow_type(email_elem, username, delay=0.2)
time.sleep(1)

# Find and fill the password field
pass_elem = driver.find_element(By.ID, 'pass')
slow_type(pass_elem, password, delay=0.2)
time.sleep(1)

# Submit the login form
pass_elem.submit()
time.sleep(5)

# Go to the public Facebook page (replace with the desired page)
page_url = 'https://www.facebook.com/groups/311334916683880/'
driver.get(page_url)
time.sleep(5)

# Scroll to load more posts
scraped_posts = []
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find post containers (selectors may change over time)
    # Find all elements with the specified class
    posts = soup.find_all('span', class_='html-span xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x1hl2dhg x16tdsg8 x1vvkbs')
    scraped_posts.append(posts)



for post in posts:
    print(post.get_text(strip=True))

driver.quit()