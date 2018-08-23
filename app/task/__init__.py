# coding=utf-8
from app.extensions import celery, mail, client
import random
import requests
from time import sleep
from bson import ObjectId
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.task.custom_conditions import element_has_css_class
from app.task.solve_recaptcha import write_stat, check_exists_by_xpath, wait_between, dimention, solve_images
from app.utils import find_report_link, watch_videos

# geckodriver = 'etc//geckodriver-v0.21.0-win64/geckodriver.exe'
# binary = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
geckodriver = 'etc/geckodriver-v0.21.0-linux64/geckodriver'
binary = '/usr/bin/firefox'
api_key = '094c2420f179731334edccbf176dbd79'
PROXY_HOST = ['93.155.250.92', '94.130.126.115', '85.109.124.130', '82.148.172.162']
PROXY_PORT = '8080'
capabilities = DesiredCapabilities.FIREFOX.copy()
capabilities['marionette'] = True
capabilities['acceptSslCerts'] = True


def create_browser():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("media.volume_scale", "0.0")
    # profile.set_preference("network.proxy.type", 1)
    # profile.set_preference("network.proxy.share_proxy_settings", True)
    # profile.set_preference("network.http.use-cache", False)
    # profile.set_preference("network.proxy.http", random.choice(PROXY_HOST))
    # profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
    # profile.set_preference('network.proxy.ssl', random.choice(PROXY_HOST))
    # profile.set_preference('network.proxy.ssl_port', int(PROXY_PORT))
    # profile.set_preference('network.proxy.socks', random.choice(PROXY_HOST))
    # profile.set_preference('network.proxy.socks_port', int(PROXY_PORT))
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    browser = webdriver.Firefox(
        executable_path=geckodriver,
        firefox_options=options,
        capabilities=capabilities,
        firefox_binary=binary,
        firefox_profile=profile)
    browser.set_window_size(1920, 1080)
    browser.set_window_position(0, 0)
    return browser


def login(browser, email, password, recovery_mail):
    try:
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
        if heading_text.text == 'Welcome':
            print(heading_text.text)
        elif heading_text.text == 'Account disabled':
            return False

        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.whsOnd.zHQkBf")))
        password_inp = browser.find_element_by_css_selector('input.whsOnd.zHQkBf')
        password_inp.send_keys(password)
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "passwordNext")))
        browser.find_element_by_id('passwordNext').click()
        try:
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "headingText")))
            header = browser.find_element_by_id('headingText')
            if header and header.text == 'Verify it\'s you':
                print('Need to input recovery email')
                # WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "vdE7Oc")))
                browser.find_element_by_class_name('vdE7Oc').click()
                WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "knowledge-preregistered-email-response")))
                recovery_email = browser.find_element_by_id('knowledge-preregistered-email-response')
                # browser.execute_script("arguments[0].value = '{}'".format(recovery_mail), recovery_email)
                recovery_email.send_keys(recovery_mail)
                next_btn = browser.find_element_by_id('next')
                browser.execute_script("arguments[0].click();", next_btn)

        except Exception as ex:
            print('No need to input recovery email: {}'.format(str(ex)))

        try:
            # check protected account
            title = browser.find_element_by_class_name('N4lOwd')
            if title and title.text == 'Protect your account':
                done_btn = browser.find_element_by_class_name('CwaK9')
                done_btn.click()
        except Exception as ex:
            pass

        ui.WebDriverWait(browser, 10).until(expected_conditions.url_matches('https://www.youtube.com'))
        print('Login success')
        return True
    except Exception as ex:
        print('Login failed: {}'.format(str(ex)))
        return False


def submit_report(browser, report_channel, report_reason_1, report_reason_2, report_note):
    browser.get(report_channel + '/videos')
    sleep(5)
    # check if channel die
    try:
        text = browser.find_element_by_css_selector('#container > yt-formatted-string')
        if text.text == 'This account has been terminated for violating Google\'s Terms of Service.':
            return '2'
    except NoSuchElementException as ex:
        pass

    # watch some videos
    try:
        videos = browser.find_elements_by_id('video-title')
        video = random.choice(videos)
        href = video.get_attribute('href')
        watch_videos(browser, href)

        sleep(random.randint(0, 10))

        for i in range(2):
            browser.execute_script("window.scrollTo(0, {})".format(random.randint(0, 1080)))
            sleep(1)
    except Exception as ex:
        print('we can not watch video: {}'.format(str(ex)))
        return '0'

    # Report this channel
    try:
        report_link = find_report_link(report_channel)
        browser.get(report_link)
        change_language(browser)
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.ID, "tab-start")))
        tab_start = browser.find_element_by_id('tab-start')
        report_types = tab_start.find_elements_by_css_selector('ul > li > div > label')
        for report_type in report_types:
            if report_type.text == report_reason_1:
                report_type.click()

        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.ID, "tab-hate-speech")))
        tab_hate_speech = browser.find_element_by_id('tab-hate-speech')
        report_types = tab_hate_speech.find_elements_by_css_selector('ul > li > div > label')
        for report_type in report_types:
            if report_type.text == report_reason_2:
                report_type.click()

        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.ID, "show-reported-user-info")))

        continue_btn = browser.find_element_by_id('show-reported-user-info')
        browser.execute_script("arguments[0].click();", continue_btn)

        ui.WebDriverWait(browser, 10).until(
            element_has_css_class((By.TAG_NAME, 'textarea'), "yt-uix-form-input-textarea"))
        notes = browser.find_element_by_class_name('yt-uix-form-input-textarea')
        notes.send_keys(report_note)

        html = browser.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        return '1'
    except Exception as ex:
        print('Report channel failed: {}'.format(str(ex)))
        return '0'


def get_key_recaptcha(browser):
    try:
        browser.switch_to.default_content()
        iframe_switch = browser.find_element(By.XPATH,
                                             "/html/body/div[1]/div[3]/div/div/form/div[2]/div/div[19]/div[4]/div/div/div/iframe")
        key = iframe_switch.get_attribute('src')
        keys = key.split('&')
        for item in keys:
            if 'k=' in item:
                key = item[2:]
                return key
    except Exception as ex:
        print('Can not switch to recaptcha checkbox: {}'.format(str(ex)))
        return None


def key_resolver_captcha(api_key, api_url):
    try:
        r = requests.get(api_url)
        res = r.text
        if 'OK' in res:
            request_id = res[3:]
            resolver_api = 'http://2captcha.com/res.php?key={}&action=get&id={}'.format(api_key, request_id)
            print(resolver_api)
            while True:
                response = requests.get(resolver_api)
                response = response.text
                if 'OK' in response:
                    response_key = response[3:]
                    sleep(5)
                    break
                if 'ERROR_CAPTCHA_UNSOLVABLE' in response:
                    response_key = None
                    break

            return response_key
        else:
            print('Can not get key api 2captcha.com')
    except Exception as ex:
        print('Can not resolver captcha: {}'.format(str(ex)))
        return None


def change_language(browser):
    try:
        lang_btn = browser.find_element_by_id('yt-picker-language-button')
        lang_btn.click()

        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "yt-picker-item")))

        current_lang = browser.find_element_by_class_name('yt-picker-item')

        sleep(2)
        # vi_btn = browser.find_elements_by_css_selector('div.yt-picker-grid:nth-child(5) > button:nth-child(2)')
        # vi_btn.click()
        en_us_btn = browser.find_element_by_xpath(
            '/html/body/div[2]/div/div[1]/div[2]/div[2]/form/div/div[2]/button[2]')
        en_us_btn.click()
    except Exception as ex:
        print('Can not change language: {}'.format(str(ex)))


@celery.task()
def print_hello():
    print('start')


@celery.task()
def stat_report():
    channels = client.db.channel.find({'status': 'active'})
    channels = list(channels)
    if len(channels) == 0:
        return
    channel = random.choice(channels)
    try:
        if channel is not None:
            client.db.channel.update({'_id': channel['_id']}, {'$set': {'reporting': True}})
            print(channel['name'])
            strategy = client.db.strategy.find_one({'_id': ObjectId(channel['strategy'])})
            if strategy is not None:
                report_reason_1 = strategy['issue']
                report_reason_2 = strategy['sub_issue']
                report_note = strategy['note']
                tmp_emails = client.db.email.find({'status': True})
                tmp_emails = list(tmp_emails)
                if len(tmp_emails) == 0:
                    client.db.channel.update({'_id': channel['_id']}, {'$set': {'reporting': False}})
                    return

                tmp_email = random.choice(tmp_emails)
                email = tmp_email['email']
                password = tmp_email['password']
                recovery_email = tmp_email['recovery_email']
                tmp_emails = None
                report_channel = channel['channel']
                try:
                    browser = create_browser()
                except Exception as ex:
                    print('Can not start browser: {}'.format(str(ex)))
                    client.db.channel.update({'_id': channel['_id']}, {'$set': {'reporting': False}})
                    return

                login_status = login(browser, email, password, recovery_email)
                if login_status:
                    # report three times
                    for i in range(3):
                        submit_report_status = submit_report(
                            browser, report_channel,
                            report_reason_1, report_reason_2,
                            report_note)

                        if submit_report_status == '1':
                            google_key = get_key_recaptcha(browser)
                            if google_key is None:
                                client.db.channel.update({'_id': channel['_id']}, {'$inc': {'count_fail': 1}})

                            current_url = browser.current_url
                            captcha_resolver_api = 'http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}&here=now'.format(
                                api_key, google_key, current_url)
                            key_resolver = key_resolver_captcha(api_key, captcha_resolver_api)
                            if key_resolver is not None:

                                browser.switch_to.default_content()
                                WebDriverWait(browser, 30).until(
                                    EC.presence_of_element_located((By.ID, "g-recaptcha-response")))
                                browser.execute_script(
                                    "document.getElementById('g-recaptcha-response').style.display = 'block';")
                                textarea_box = browser.find_element_by_id('g-recaptcha-response')
                                textarea_box.send_keys(key_resolver)
                                submit_report_btn = browser.find_element_by_id('submit-report')
                                submit_report_btn.click()
                                try:
                                    WebDriverWait(browser, 30).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, ".section > p:nth-child(1)")))
                                    section = browser.find_element_by_css_selector('.section > p:nth-child(1)')
                                    if section and section.text == 'Thank You.':
                                        print('Submit report successfully')
                                        client.db.channel.update({'_id': channel['_id']},
                                                                 {'$inc': {'count_success': 1}})
                                except Exception as ex:
                                    print('Submit report failed: {}'.format(str(ex)))
                                    client.db.channel.update({'_id': channel['_id']}, {'$inc': {'count_fail': 1}})

                            else:
                                client.db.channel.update({'_id': channel['_id']}, {'$inc': {'count_fail': 1}})

                        elif submit_report_status == '2':
                            print('Channel suspended save to database')
                            client.db.channel.update({'_id': channel['_id']}, {'$set': {'status': 'Suspended'}})
                            return

                    client.db.channel.update({'_id': channel['_id']}, {'$set': {'reporting': False}})
                    browser.quit()
                else:
                    print('{} can not login to youtube'.format(email))
                    client.db.email.update({'_id': tmp_email['_id']}, {'$set': {'status': False}})
                    # mark as done reporting
                    client.db.channel.update({'_id': channel['_id']}, {'$set': {'reporting': False}})
                    browser.quit()
    except Exception as ex:
        client.db.channel.update({'_id': channel['_id']}, {'$set': {'reporting': False}})
        print('Exception: {}'.format(str(ex)))
