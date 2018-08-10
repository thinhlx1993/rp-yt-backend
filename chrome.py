# -*- coding: utf-8 -*-

import random
import json
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from custom_conditions import element_has_css_class
from untils import find_report_link, watch_videos
from solve_recaptcha import write_stat, check_exists_by_xpath, wait_between, dimention, solve_images

chrome_driver = 'D:\\Code\\repport-yt-backend\etc\\chromedriver_win32\\chromedriver.exe'
binary = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
PROXY_HOST = ''
PROXY_PORT = ''
email = 'markogunz@gmail.com'
password = 'Minh1234'
recovery_mail = 'washpets17336@yahoo.com'
report_channel = 'https://www.youtube.com/channel/UCMacC2sTrMeLIS82oQCT0DA'
report_link = find_report_link(report_channel)
print(report_link)
report_reson_1 = 'Hate Speech Against a Protected Group'
report_reson_2 = 'Race or ethnic origin (examples: African American, Pacific Islander)'
report_note = 'none'



browser = webdriver.Chrome(executable_path=chrome_driver)
browser.set_window_size(1920, 1080)
browser.set_window_position(0, 0)
wait = ui.WebDriverWait(browser,10)

browser.get('https://www.youtube.com/')

sign_in_btn = browser.find_element_by_css_selector('a.yt-simple-endpoint.style-scope.ytd-button-renderer')
sign_in_btn.click()

email_inp = browser.find_element_by_id('identifierId')
email_inp.send_keys(email)
browser.find_element_by_id('identifierNext').click() # đi đến trang nhập password
wait.until(expected_conditions.text_to_be_present_in_element((
                By.CSS_SELECTOR, '#headingText > content'), 'Welcome'))
password_inp = browser.find_element_by_css_selector('input.whsOnd.zHQkBf')
password_inp.send_keys(password)
browser.find_element_by_id('passwordNext').click()

try:
    header = browser.find_element_by_id('headingText')
    if header and header.text == 'Verify it\'s you':
        print('Need to input recovery email')
        browser.find_element_by_class_name('vdE7Oc').click()
        recovery_email = browser.find_element_by_id('knowledge-preregistered-email-response')
        recovery_email.send_keys(recovery_mail)
        next_btn = browser.find_element_by_id('next')
        next_btn.click()
except Exception as ex:
    print('No need to input recovery email')


wait.until(expected_conditions.url_matches('https://www.youtube.com/'))
# watch some videos
browser.get(report_channel + '/videos')
videos = browser.find_elements_by_id('video-title')
video = random.choice(videos)
href = video.get_attribute('href')
watch_videos(browser, href)
        
sleep(random.randint(0, 10))
# Report this channel
browser.get(report_link)
tab_start = browser.find_element_by_id('tab-start')
report_types = tab_start.find_elements_by_css_selector('ul > li > div > label')
for report_type in report_types:
    if report_type.text == report_reson_1:
        report_type.click()

tab_hate_speech = browser.find_element_by_id('tab-hate-speech')
report_types = tab_hate_speech.find_elements_by_css_selector('ul > li > div > label')
for report_type in report_types:
    if report_type.text == report_reson_2:
        report_type.click()
        
continue_btn = browser.find_element_by_id('show-reported-user-info')
continue_btn.click()

wait.until(element_has_css_class((By.TAG_NAME, 'textarea'), "yt-uix-form-input-textarea"))
notes = browser.find_element_by_class_name('yt-uix-form-input-textarea')
notes.send_keys(report_note)

html = browser.find_element_by_tag_name('html')
html.send_keys(Keys.END)



#start = time()
#mainWin = browser.current_window_handle  
#
## move the driver to the first iFrame 
#recaptcha = browser.find_element_by_class_name('g-recaptcha')
#browser.switch_to_frame(recaptcha.find_element_by_css_selector("div > div > iframe"))
#
#checkbox = browser.find_element_by_id('recaptcha-anchor-label')
#
#audio_button = browser.find_element_by_id('recaptcha-audio-button')
#print(audio_button.get_attribute('title'))
#audio_button.click()
#
#download_audio = browser.find_element_by_class_name('rc-audiochallenge-tdownload-link')
#print(download_audio.get_attribute('title'))
#download_audio.click()
#captcha_visible = browser.find_element_by_class_name('recaptcha-checkbox-checkmark')
#captcha_visible.click()
#audio_button = browser.find_element_by_id('recaptcha-audio-button')
#audio_button.click()
#play_button = browser.find_element_by_class_name('rc-audiochallenge-play-button')
#play_button.click()
