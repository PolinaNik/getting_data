from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument("start-maximized")

s = Service('/usr/lib/chromium-browser/chromedriver')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get('https://www.mvideo.ru/')
driver.implicitly_wait(20)

# прокрутка до трендов
driver.execute_script("window.scrollTo(0, 1800)")

# нажатие кнопки "В тренде"
button = driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']")
driver.execute_script("arguments[0].click();", button)

# сбор трендовых товаров
products = []
container = driver.find_element(By.XPATH, "//mvid-shelf-group[@class='page-carousel-padding ng-star-inserted']")
links = container.find_elements(By.XPATH, ".//a[@class='img-with-badge ng-star-inserted']")
prices = container.find_elements(By.XPATH, ".//span[contains(@class, 'price__main-value')]")
names = container.find_elements(By.XPATH, ".//div[contains(@class, 'title')]/a/div")

for num, elem in enumerate(links):
    product = {}
    link = elem.get_attribute('href')
    name = names[num].text
    price = prices[num].text.replace(" ", "")
    product["link"] = link
    product["price"] = price
    product["name"] = name
    products.append(product)

# добавление в базу
client = MongoClient('localhost', 27017)
db = client['mvideo_products']  # database
mvideo_db = db.vacancies  # collection

for product in products:
    link_product = product['link']
    if mvideo_db.count_documents({"link": link_product}) == 0:
        mvideo_db.insert_one(product)
