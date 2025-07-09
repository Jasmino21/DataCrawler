import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from urllib.parse import quote

def slow_type(element, text, delay=0.1):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

# Set up Selenium WebDriver (make sure chromedriver is in your PATH)
driver = webdriver.Chrome(executable_path='chromedriver.exe')

# Go to Facebook login page
driver.get('https://www.facebook.com/login')
time.sleep(3)

# Enter your credentials here
username = os.getenv("FB_USERNAME")
password = os.getenv("FB_PASSWORD")

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

# Go to the public Facebook page
page_urls = ['https://www.facebook.com/groups/311334916683880/', 'https://www.facebook.com/groups/185364866044514', 'https://www.facebook.com/groups/997778863653171']
results = {}
feed_post_list = []
for page_url in page_urls:
    driver.get(page_url)
    time.sleep(5)

    # Scroll to load more posts
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        feed_posts = soup.find_all('div', class_='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z')
        # feed_post_list.append(feed_posts)

        for post in feed_posts:
            # Get poster names
            poster_names = []
            poster_name_tags = post.find_all('a', class_='x1i10hfl xjbqb8w x1ejq31n x18oe1m7 x1sy0etr xstzfhl x972fbf x10w94by x1qhh985 x14e42zd x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xkrqix3 x1sur9pj xzsf02u x1s688f')
            for name_tag in poster_name_tags:
                for span in name_tag.find_all('span'):
                    name_text = span.get_text(strip=True)
                    if name_text:
                        poster_names.append(name_text)

            # Get descriptions
            description1 = post.find_all(
                'span',
                class_='html-span xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x1hl2dhg x16tdsg8 x1vvkbs',
                attrs={'data-ad-rendering-role': 'description'}
            )
            description2 = post.find_all('div', attrs={'data-ad-preview': 'message'})
            description3 = post.find_all(
                'span',
                class_='html-span xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x1hl2dhg x16tdsg8 x1vvkbs',
                attrs={'data-ad-rendering-role': 'title'}
            )
            description4 = post.find_all(
                'span',
                class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x6prxxf xvq8zen xo1l8bm xzsf02u'
            )

            # Join all found texts for each description type
            desc1 = ' '.join([desc.get_text(strip=True) for desc in description1])
            desc2 = ' '.join([desc.get_text(strip=True) for desc in description2])
            desc3 = ' '.join([desc.get_text(strip=True) for desc in description3])
            desc4 = ' '.join([desc.get_text(strip=True) for desc in description4])

            # For each name found, add to results
            for name in poster_names:
                quoted_name = quote(name)
                post_link = f"{page_url}search/?q={quoted_name}"
                results[name] = {
                    'desc1': desc1,
                    'desc2': desc2,
                    'desc3': desc3,
                    'desc4': desc4, 
                    'post_link': post_link,
                    'page_url': page_url
                }
                print(f"Post link: {post_link}")
                print(f"Name: {name}")
                print(f"Description 1: {desc1}")    
                print(f"Description 2: {desc2}")    
                print(f"Description 3: {desc3}")    
                print(f"Description 4: {desc4}")    

# After scraping, save or print the results as JSON
with open('output/fb_posts.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

# with open('output/feed_posts.txt', 'w', encoding='utf-8') as f:
#     f.write(str(feed_post_list))

driver.quit()