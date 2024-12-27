import os
import yt_dlp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ydl_opts = {
    'format': 'bestaudio/best',
}

itteration = 0
max_itteration = 5

driver = webdriver.Chrome()

driver.get('https://uz.lyricsus.com/')

links = [a.get_attribute('href') for a in driver.find_elements(By.XPATH, '//*[@id="post-19787"]/a')]
for link in links:
    if itteration >= max_itteration:
        break

    driver.get(link)
    song_name = driver.find_element(By.XPATH, '//*[@id="main-area-header"]/h1').text
    song_lyrics = driver.find_element(By.XPATH, '//div[@id="main-article"]').text

    song_folder = f'parsed_songs/{song_name}'
    if not os.path.exists(song_folder):
        os.makedirs(song_folder)

    text_file_path = os.path.join(song_folder, f'{song_name}.txt')
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(song_lyrics)
        
    video_link_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="youtube"]//iframe')))

    video_link = video_link_element.get_attribute('src')

    ydl_opts['outtmpl'] = os.path.join(song_folder, f'{song_name}.mp3')
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

    itteration += 1

driver.quit()