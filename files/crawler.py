from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

video_url = ["https://lolesports.com/vod/110471059652887260/1/ckoxgB42rhE",
             "https://lolesports.com/vod/110471059652887260/2/Hu26a6o4thc",
             "https://lolesports.com/vod/110471059652887260/3/SBJ-tuj1jSU",
             "https://lolesports.com/vod/110471059652887260/4/oYHwbmzb_vM"]

driver = webdriver.Chrome()
count = 1
for url in video_url:
    try:
        driver.get(url)
        
        actions = ActionChains(driver)

        print("Waiting for video to load")
        time.sleep(5)
        print("Video loaded")

        start_button = driver.find_element(By.XPATH, "//*[@class='attached']")
        start_button.click()

        time.sleep(2)
        #press the 9 key to go back 10 seconds
        actions.send_keys(Keys.NUMPAD9).perform()
        time.sleep(2)

        #get the htlm of the page
        html = driver.page_source

        file_name = f"lolesports_{count}.txt"

        # Obter o diretório do script atual
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Construir o caminho completo para o arquivo 'lolesports.txt' dentro da pasta 'data/raw'
        file_path = os.path.join(script_directory, '..', 'data', 'raw', file_name)

        # Garantir que o diretório 'data/raw' exista
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Salvar a saída no arquivo
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html)
        
        count += 1
    except Exception as e:
        print(e)
        
print("Closing driver")
driver.quit()

