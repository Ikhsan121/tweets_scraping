# import dependencies
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains


service = Service(executable_path="C:\Development\chromedriver.exe")
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://twitter.com/jokowi?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor")

result = []
sleep(5)

y = 500
while True:

    element = driver.find_element(By.XPATH, "//div[@aria-label='Back']")
    # scroll down
    sleep(2)
    driver.execute_script("window.scrollTo(0, " + str(y) + ")")
    # click on the tweet
    sleep(2)
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(element, 0, 200).click().perform()
    # scraping process
    sleep(2)
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    for article in articles:
        UserTag = driver.find_element(By.XPATH, ".//div[@data-testid='User-Names']").text.split("\n")[0]
        TimeStamp = driver.find_element(By.XPATH, ".//time").get_attribute('datetime')
        Tweet = driver.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
        Reply = driver.find_element(By.XPATH, "(.//span[@data-testid='app-text-transition-container'])[1]").text
        reTweet = driver.find_element(By.XPATH, "(.//span[@data-testid='app-text-transition-container'])[2]").text
        Like = driver.find_element(By.XPATH, "(.//span[@data-testid='app-text-transition-container'])[3]").text

        final_data = {
            'UserTag': UserTag,
            'TimeStamp': TimeStamp,
            'Tweet': Tweet,
            'Reply': Reply,
            'reTweet': reTweet,
            'Like': Like,
        }
        result.append(final_data)


    y += 500
    try:
        pop_up = driver.find_element(By.XPATH, "//div[@data-testid='mask']")
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(pop_up, 0, 0).click().perform()
    except:
        None
    # back to original profile page
    driver.execute_script("window.history.go(-1)")

    if len(result) > 50:
        break

# remove duplicate tweets
result = list(
    {
        dictionary['Tweet']: dictionary
        for dictionary in result
    }.values()
)

print(result)
print(len(result))
try:
    os.mkdir('json_result')
except FileExistsError:
    pass
with open('json_result/final_data.json', "w+") as json_data:
    json.dump(result, json_data)
print('json created')

# create csv
df = pd.DataFrame(result)
df.to_csv('twitter_data.csv', index=False)
df.to_excel('twitter_data.xlsx', index=False)
print("Data created success")
print("Total rows", len(result))