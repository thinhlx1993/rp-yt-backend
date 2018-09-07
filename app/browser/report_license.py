# coding=utf-8
import os
import sys
import random
import subprocess
import requests
from time import sleep
from bson import ObjectId
from itertools import islice
from pymongo import MongoClient
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# logging
import logging

# create logger with 'report_application'
logger = logging.getLogger('report_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
log_path = 'D:/Code/report-yt-backend/logs' if sys.platform == 'win32' \
    else '/opt/rp-yt-backend/logs/report_license.log'
fh = logging.FileHandler(log_path)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

api_key = '094c2420f179731334edccbf176dbd79'


def create_browser(user_agent):
    capabilities = DesiredCapabilities.FIREFOX.copy()
    capabilities['marionette'] = True
    capabilities['acceptSslCerts'] = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("general.useragent.override", user_agent['name'])
    profile.set_preference("media.volume_scale", "0.0")
    options = webdriver.FirefoxOptions()

    print(sys.platform)
    logger.info(sys.platform)
    if sys.platform == 'win32':
        geckodriver = '../../etc/geckodriver-v0.21.0-win64/geckodriver.exe'
        binary = 'C:/Program Files/Mozilla Firefox/firefox.exe'
    else:
        geckodriver = '/opt/rp-yt-backend/etc/geckodriver-v0.21.0-linux64/geckodriver'
        binary = '/usr/bin/firefox'
        options.add_argument('--headless')
    driver = webdriver.Firefox(
        executable_path=geckodriver,
        firefox_options=options,
        capabilities=capabilities,
        firefox_binary=binary,
        firefox_profile=profile)
    driver.set_window_size(1920, 1080)
    driver.set_window_position(0, 0)
    return driver


def login(browser, email, password, recovery_email):
    browser.get('https://www.youtube.com/')
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-button-renderer.style-scope:nth-child(5) > a:nth-child(1)")))
    # sign_in_btn = browser.find_element_by_css_selector('a.yt-simple-endpoint.style-scope.ytd-button-renderer')
    sign_in_btn = browser.find_element_by_css_selector('ytd-button-renderer.style-scope:nth-child(5) > a:nth-child(1)')
    sign_in_btn.click()

    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_inp = browser.find_element_by_id('identifierId')
    email_inp.send_keys(email)
    browser.find_element_by_id('identifierNext').click()  # đi đến trang nhập password
    sleep(3)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#headingText > content")))
    heading_text = browser.find_element_by_css_selector('#headingText > content')
    if heading_text.text != 'Welcome':
        return 'fail'

    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.whsOnd.zHQkBf")))
    password_inp = browser.find_element_by_css_selector('input.whsOnd.zHQkBf')
    password_inp.send_keys(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "passwordNext")))
    browser.find_element_by_id('passwordNext').click()
    
    sleep(2)
    # Input recovery email
    try:
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "headingText")))
        header = browser.find_element_by_id('headingText')
        if header and header.text == 'Verify it\'s you':
            print('Input recovery email')
            logger.info('Input recovery email')
            browser.find_element_by_class_name('vdE7Oc').click()
            sleep(2)
            while True:
                try:
                    recovery_inp = browser.find_element_by_id('knowledge-preregistered-email-response')
                    recovery_inp.click()
                    recovery_inp.send_keys(recovery_email)
                    break
                except:
                    logger.info('Input recovery email error')
                    print('Input recovery email error')

            next_btn = browser.find_element_by_id('next')
            browser.execute_script("arguments[0].click();", next_btn)
    except Exception as ex:
        logger.info('No need to enter recovery email: {}'.format(str(ex)))
        print('No need to enter recovery email: {}'.format(str(ex)))
        return 'success'
    
    sleep(2)
    try:
        # check protected account
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "N4lOwd")))
        title = browser.find_element_by_class_name('N4lOwd')
        print(title.text)
        if title and title.text == 'Protect your account':
            done_btn = browser.find_element_by_class_name('CwaK9')
            done_btn.click()
    except Exception as ex:
        pass
    
    sleep(2)
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "headingText")))
        header = browser.find_element_by_id('headingText')
        print(header.text)
        if header and (header.text == 'Account disabled' or header.text == 'Change password'):
            return 'disabled'
    except Exception as ex:
        logger.error('Enter recovery email successfully')
        print('Enter recovery email successfully')
        
    try:
        ui.WebDriverWait(browser, 10).until(EC.url_matches('https://www.youtube.com'))
        return 'success'
    except Exception as ex:
        return 'fail'


def get_key_recaptcha(browser, xpath):
    try:
        browser.switch_to.default_content()
        iframe = browser.find_element_by_xpath(xpath)
        key = iframe.get_attribute('src')
        keys = key.split('&')
        for item in keys:
            if 'k=' in item:
                key = item[2:]
                return key
    except Exception as ex:
        print('Can not switch to recaptcha checkbox: {}'.format(str(ex)))
        logger.error('Can not switch to recaptcha checkbox: {}'.format(str(ex)))
        return None


def key_resolver_captcha(api_url):
    try:
        r = requests.get(api_url)
        sleep(5)
        res = r.text
        if 'OK' in res:
            request_id = res[3:]
            resolver_api = 'http://2captcha.com/res.php?key={}&action=get&id={}'.format(api_key, request_id)
            logger.info(resolver_api)
            print(resolver_api)
            while True:
                try:
                    response = requests.get(resolver_api)
                    response = response.text
                    if 'OK' in response:
                        response_key = response[3:]
                        break
                    if 'ERROR_CAPTCHA_UNSOLVABLE' in response:
                        response_key = None
                        break
                except Exception as ex:
                    logger.error('Get response error: {}'. format(str(ex)))
                    print('Get response error: {}'. format(str(ex)))

            return response_key
        else:
            logger.info('Can not get key api 2captcha.com')
            print('Can not get key api 2captcha.com')
    except Exception as ex:
        logger.error('Can not resolver captcha: {}'.format(str(ex)))
        print('Can not resolver captcha: {}'.format(str(ex)))
        return None


def change_language(browser):
    try:
        lang_btn = browser.find_element_by_id('yt-picker-language-button')
        lang_btn.click()
        sleep(2)
        langs = browser.find_elements_by_css_selector('.yt-picker-item > span')
        for lang in langs:
            if 'English' in lang.text:
                lang.click()
                return
    except Exception as ex:
        logger.error('Change lang failed: {}'.format(str(ex)))
        print('Change lang failed: {}'.format(str(ex)))


def fakeip():
    subprocess.call(['macchanger', '-A', 'ens33'])
    process = subprocess.Popen(['macchanger', '-s', 'ens33'], stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    logger.info(stdout)
    subprocess.call(['service', 'vpngate@worker', 'restart'])
    sleep(10)


def videos_of_channel(browser):
    channels = db.channel.find({'status': 'active'})
    channels = list(channels)
    if len(channels) == 0:
        logger.info('Channel list is empty')
        print('Channel list is empty')
        return
    channel = random.choice(channels)
    browser.get('{}/videos'.format(channel['channel']))
    channel_id = channel['_id']
    for i in range(5):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    videos = browser.find_elements_by_id('video-title')
    data = list()
    for video in videos:
        href = video.get_attribute('href')
        if not href.startswith('https'):
            href = 'https://www.youtube.com/{}'.format(href)
        data.append({'url': href, 'title': video.text})
    return data, channel_id


def main_func(browser, db, videos, channel_id):
    login_status = False
    while not login_status:
        tmp_emails = db.email.find({'status': True})
        tmp_emails = list(tmp_emails)
        if len(tmp_emails) == 0:
            logger.info('Can not find any email')
            print('Can not find any email')
            return
        tmp_email = random.choice(tmp_emails)
        email = tmp_email['email']
        password = tmp_email['password']
        recovery_email = tmp_email['recovery_email']
        login_status = login(browser, email, password, recovery_email)
        if login_status == 'success':
            logger.info('Logged in to youtube')
            print('Logged in to youtube')
        elif login_status == 'fail':
            logger.info('{} can not login to youtube'.format(email))
            print('{} can not login to youtube'.format(email))
            return
        elif login_status == 'disabled':
            logger.info('{} is disabled'.format(email))
            print('{} is disabled'.format(email))
            db.email.update({'_id': tmp_email['_id']}, {'$set': {'status': False}})
            return

    for video in videos:
        browser.get('https://www.youtube.com/copyright_complaint_form')
        # need to resolver captcha
        # break if captcha can not resolved
        captcha_status = True
        try:
            title = browser.find_element_by_xpath('/html/body/div[1]/div/b')
            if title.text == 'About this page':
                x_path = '/html/body/div[1]/form/div/div/div/iframe'
                google_key = get_key_recaptcha(browser, x_path)
                current_url = browser.current_url
                captcha_resolver_api = 'http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}&here=now'.format(api_key, google_key, current_url)
                key_resolver = key_resolver_captcha(captcha_resolver_api)
                if key_resolver is not None:
                    browser.switch_to.default_content()
                    WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.ID, "g-recaptcha-response")))
                    browser.execute_script(
                        "document.getElementById('g-recaptcha-response').style.display = 'block';")
                    textarea_box = browser.find_element_by_id('g-recaptcha-response')
                    textarea_box.send_keys(key_resolver)
                    submit_report_btn = browser.find_element_by_xpath('/html/body/div[1]/form/input[3]')
                    submit_report_btn.click()
                else:
                    captcha_status = False
        except Exception as ex:
            logger.error('No Need to resolver captcha')
            print('No Need to resolver captcha')
        
        if captcha_status:
            change_language(browser)
            reason1 = 'copyright infringement (someone copied my creation)'
            reason2 = 'i am!'

            complaint_filter_div = browser.find_element_by_id('complaint_filter_div')
            complaints = complaint_filter_div.find_elements_by_css_selector('ul > li > label')
            for complaint in complaints:
                complaint_text = complaint.text
                complaint_text = complaint_text.lower().strip()
                if complaint_text == reason1:
                    complaint.click()

            affected_entities_div = browser.find_element_by_id('affected-entities-div')
            complaints = affected_entities_div.find_elements_by_css_selector('ul > li > label')
            for complaint in complaints:
                complaint_text = complaint.text
                complaint_text = complaint_text.lower().strip()
                if complaint_text == reason2:
                    complaint.click()

            video_url_0 = browser.find_element_by_id('video_url_0')
            video_url_0.send_keys(video['url'])
            from selenium.webdriver.support.ui import Select
            issue_type_0 = Select(browser.find_element_by_id('issue_type_0'))
            issue_type_0.select_by_value('S')

            issue_details_wrapper = browser.find_element_by_class_name('issue_details_wrapper')
            conditional_value_validations = issue_details_wrapper.find_elements_by_css_selector('.conditional-value-validation')
            for conditional_value_validation in conditional_value_validations:
                if conditional_value_validation.get_attribute('name') == 'issue_detail_S_0':
                    conditional_value_validation.send_keys(video['title'])

            reason3 = 'entire video'
            position_marker = browser.find_element_by_class_name('position-marker-class-S-0')
            issue_details = position_marker.find_elements_by_css_selector('ul > li > label')
            for issue_detail in issue_details:
                issue_detail_text = issue_detail.text
                issue_detail_text = issue_detail_text.lower().strip()
                if issue_detail_text == reason3:
                    issue_detail.click()

            totals = db.fake_user.count_documents({})
            fake_user = db.fake_user.find({}).limit(-1).skip(random.randint(0, totals)).next()

            owner_display_name = browser.find_element_by_id('owner_display_name')
            owner_display_name.send_keys(fake_user['name'])

            requester_title = browser.find_element_by_id('requester_title')
            requester_title.send_keys(fake_user['name'])

            requester_name = browser.find_element_by_id('requester_name')
            requester_name.send_keys(fake_user['name'])

            address1 = browser.find_element_by_id('address1')
            address1.send_keys(fake_user['address_1'])

            address2 = browser.find_element_by_id('address2')
            address2.send_keys(fake_user['address_2'])

            city = browser.find_element_by_id('city')
            city.send_keys(fake_user['city'])

            state = browser.find_element_by_id('state')
            state.send_keys(fake_user['state'])

            zip_code = browser.find_element_by_id('zip')
            zip_code.send_keys(fake_user['zip_code'])

            phone = browser.find_element_by_id('phone')
            phone.send_keys(fake_user['phone'])

            country = Select(browser.find_element_by_id('country'))
            country.select_by_value('US')

            browser.find_element_by_id('checkbox_confirmation_1').click()
            browser.find_element_by_id('checkbox_confirmation_2').click()
            browser.find_element_by_id('checkbox_confirmation_3').click()
            browser.find_element_by_id('checkbox_confirmation_liability').click()
            browser.find_element_by_id('checkbox_confirmation_abuse_termination').click()
            owner_signature = browser.find_element_by_id('owner_signature')
            owner_signature.send_keys(fake_user['name'])

            iframe_path = '/html/body/div[1]/div[3]/div/div/div[2]/form/div[5]/div[4]/div/div/iframe'
            google_key = get_key_recaptcha(browser, iframe_path)
            current_url = browser.current_url
            captcha_resolver_api = 'http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}&here=now'.format(
                api_key, google_key, current_url)
            key_resolver = key_resolver_captcha(captcha_resolver_api)
            if key_resolver is not None:
                browser.switch_to.default_content()
                WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.ID, "g-recaptcha-response")))
                browser.execute_script(
                    "document.getElementById('g-recaptcha-response').style.display = 'block';")
                textarea_box = browser.find_element_by_id('g-recaptcha-response')
                textarea_box.send_keys(key_resolver)
                submit_report_btn = browser.find_element_by_id('submit_complaint_button')
                submit_report_btn.click()
                try:
                    change_language(browser)
                    content = browser.find_element_by_css_selector('.page-default > div > h1')
                    if content and 'Thank you' in content.text:
                        logger.info('Submit report successfully')
                        print('Submit report successfully')
                        db.channel.update({'_id': channel_id}, {'$inc': {'count_success': 1}})
                except Exception as ex:
                    logger.error('Submit report failed: {}'.format(str(ex)))
                    print('Submit report failed: {}'.format(str(ex)))
                    db.channel.update({'_id': channel_id}, {'$inc': {'count_fail': 1}})


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


if __name__ == "__main__":
    while True:
        try:
            fakeip()
            client = MongoClient('167.99.145.231', username='admin', password='1234567a@', authSource='admin')
            db = client['test-yt']
            totals = db.agents.count_documents({'status': True})
            agent = db.agents.find({'status': True}).limit(-1).skip(random.randint(0, totals)).next()
            logger.info('new agent: {}'.format(agent['name']))
            get_videos_browser = create_browser(agent)
            all_videos, channel_id = videos_of_channel(get_videos_browser)
            get_videos_browser.quit()
            
            chunk_videos = list(chunk(all_videos, 3))
            for videos in chunk_videos:
                main_browser = create_browser(agent)
                main_func(main_browser, db, videos, channel_id)
                if main_browser:
                    main_browser.quit()
                
        except Exception as ex:
            if get_videos_browser:
                get_videos_browser.quit()
            if main_browser:
                main_browser.quit()
            logger.error('Exception: {}'.format(str(ex)))
            print('Exception: {}'.format(str(ex)))
