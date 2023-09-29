from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils import login, count_post, notify_slack
import yaml

with open("config.yaml") as file:
    global USERNAME, EMAIL, PASSWORD, TARGET, WEBHOOK
    yaml_file = yaml.safe_load(file)
    USERNAME = yaml_file['username']
    EMAIL = yaml_file['email']
    PASSWORD = yaml_file['password']
    TARGET = yaml_file['target']
    WEBHOOK = yaml_file['webhook']

driver_path = r'C:\Users\kento\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("-start-maximized")

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

login(driver, USERNAME, EMAIL, PASSWORD)

driver.get("https://twitter.com/" + TARGET)

count = count_post(driver)

with open('tweet_count.txt', mode='a') as f:
    f.write(count + '\n')

notify_slack(WEBHOOK, TARGET)





