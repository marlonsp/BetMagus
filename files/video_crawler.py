from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

video_url = "https://lolesports.com/vod/110471059652887260/1/ckoxgB42rhE"

driver = webdriver.Chrome()
try:
    driver.get(video_url)
    
    actions = ActionChains(driver)

    video_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="title"]/h1/yt-formatted-string'))
    )

    print(video_title.text)

    start_button = driver.find_element(By.XPATH, "//*[@class='ytp-play-button ytp-button']")
    start_button.click()
    print("Video started")
    #wait 5 seconds
    time.sleep(5)
    #pause video
    start_button.click()

    #press the END key to go to the end of the video
    actions.send_keys(Keys.END).perform()
    
    time.sleep(2)

except Exception as e:
    print(e)

finally:
    print("Closing driver")
    driver.quit()

