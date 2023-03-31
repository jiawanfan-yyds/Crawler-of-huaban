import os
import argparse
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    save_path = request.form['save_path']
    max_images_to_scrape = int(request.form['max_images_to_scrape'])

    # Specify user agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    # Create local folder to save images
    os.makedirs(save_path, exist_ok=True)

    # Use Chrome browser to open the requested page
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for 20s before making requests to perform login or other actions
    time.sleep(20)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    last_length = 0
    images = []
    scroll_count = 0
    # Loop through scroll operations until all images are loaded
    while len(images) < max_images_to_scrape and scroll_count < 10:
        driver.find_element('tag name', 'body').send_keys(Keys.END)
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        new_images = soup.find_all('img')
        # Check if new images have been loaded after each scroll operation
        if len(new_images) == last_length:
            scroll_count += 1
        else:
            images.extend(new_images)
            last_length = len(new_images)
            scroll_count = 0

        # Exit loop if no new images are loaded in 3 seconds
        time_count = 0
        time_count += 3
        if time_count >= 15:
            break

    # Save images to local folder using requests
    for i, img in enumerate(images[:max_images_to_scrape]):
        img_url = img['src']
        # Remove "_fw240webp" and replace extension with ".png"
        img_filename = os.path.splitext(os.path.basename(img_url.replace("_fw240webp", "")))[0] + ".png"
        if not img_url.startswith("http"):
            img_url = "http:" + img_url
        response = requests.get(img_url.replace("_fw240webp", ""), headers=headers)
        with open(os.path.join(save_path, img_filename), 'wb') as f:
            f.write(response.content)

    driver.quit()

    return render_template('result.html', message='爬取完成')

if __name__ == '__main__':
    app.run(debug=True)
