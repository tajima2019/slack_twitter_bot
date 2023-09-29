from selenium.webdriver.common.by import By
import slackweb

def login(driver, USERNAME, EMAIL, PASSWORD):
    driver.get("https://twitter.com/home")
    # 指定した要素が見つかるまでの待ち時間を設定する 今回は最大10秒待機する
    driver.implicitly_wait(10)

    mail_box = driver.find_element(by=By.XPATH,
                                   value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')

    mail_box.send_keys(EMAIL)

    next_btn = driver.find_element(by=By.XPATH,
                                   value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span')
    next_btn.click()

    driver.implicitly_wait(10)

    username_box = driver.find_element(by=By.XPATH,
                                       value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
    username_box.send_keys(USERNAME)

    next_btn = driver.find_element(by=By.XPATH,
                                   value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/span/span')
    next_btn.click()

    driver.implicitly_wait(10)

    pass_box = driver.find_element(by=By.XPATH,
                                   value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    pass_box.send_keys(PASSWORD)

    login_btn = driver.find_element(by=By.XPATH,
                                    value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span')
    login_btn.click()


def count_post(driver):
    notify_btn = driver.find_element(by=By.XPATH,
                                     value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/span/span')
    notify_btn.click()

    post_count_box = driver.find_element(by=By.XPATH,
                                         value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div')

    post_count = post_count_box.text.split(" ")
    post_count = post_count[0].replace(',', '')
    return post_count


def notify_slack(web_hook_url, TARGET):
    with open('tweet_count.txt', mode='r') as f:
        global pre, cur
        l = f.readlines()
        if len(l) == 0:
            return
        elif len(l) == 1:
            pre = int(l[0].rstrip())
            cur = int(l[0].rstrip())
        else:
            pre = int(l[-2].rstrip())
            cur = int(l[-1].rstrip())
    if cur > pre:
        slack = slackweb.Slack(web_hook_url)
        slack.notify(text="Tweetが更新されました。\n https://twitter.com/" + TARGET, unfurl_links='true')