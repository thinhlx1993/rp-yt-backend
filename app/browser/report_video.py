# coding=utf-8
import sys
import random
from time import sleep
import subprocess
import platform

import requests
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Text
from sqlalchemy import create_engine

api_key = 'ddc61b61b359963abe27e6cf3213bc34'
engine = create_engine('sqlite:///etc/db/prd.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    status = Column(Text)
    count_success = Column(Integer)
    count_fail = Column(Integer)
    first_time = Column(Text)
    second_time = Column(Text)

    @classmethod
    def find_random(cls):
        while True:
            rand = random.randrange(0, session.query(Video).count())
            row = session.query(Video)[rand]
            if row.status == 'active':
                break
        return row

    @classmethod
    def find_all(cls):
        return session.query(Video).filter_by(status='active').all()

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()


class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    created_date = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    @classmethod
    def find_random(cls):
        while True:
            rand = random.randrange(0, session.query(Agent).count())
            row = session.query(Agent)[rand]
            if row.status:
                break
        return row

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()


class Email(Base):
    __tablename__ = 'email'

    id = Column(Integer, primary_key=True)
    password = Column(Text, nullable=False)
    recovery_email = Column(Text)
    status = Column(Integer, nullable=False)
    date = Column(Text)
    email = Column(Text, nullable=False)
    phone = Column(Integer)

    def __init__(self, password, recovery_email, status, date, email, phone):
        self.password = password
        self.recovery_email = recovery_email
        self.status = status
        self.date = date
        self.email = email
        self.phone = phone

    def json(self):
        return {"id": self.id, 'password': self.password, 'recovery_email': self.recovery_email, 'status': self.status,
                'date': self.date, 'email': self.email, 'phone': self.phone}

    @classmethod
    def find_random(cls):
        rand = random.randrange(0, session.query(Email).count())
        row = session.query(Email)[rand]
        print(row.json())
        return row

    @classmethod
    def find_by_status(cls, status):
        return cls.query.filter_by(status=status).first()

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()


class FakeUser(Base):
    __tablename__ = 'fake_user'

    id = Column(Integer, primary_key=True)
    country = Column(Text)
    gender = Column(Text)
    state = Column(Text)
    name = Column(Integer)
    address_1 = Column(Text)
    address_2 = Column(Text)
    city = Column(Text)
    zip_code = Column(Text)
    phone = Column(Text)

    @classmethod
    def find_random(cls):
        rand = random.randrange(0, session.query(FakeUser).count())
        row = session.query(FakeUser)[rand]
        return row

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()


def find_report_link(s):
    """
    Ge report link from url
    :param s:
    :return:
    """
    first = 'https://www.youtube.com/channel/'
    try:
        start = s.index(first) + len(first) + 2
        report_link = 'https://www.youtube.com/reportabuse?u={}'.format(s[start:])
        return report_link
    except ValueError:
        return None


def watch_videos(browser, href):
    ActionChains(browser) \
        .key_up(Keys.CONTROL) \
        .send_keys('t') \
        .key_up(Keys.CONTROL) \
        .perform()
    browser.get(href)


class element_has_css_class(object):
    """
    An expectation for checking that an element has a particular css class.
    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False


def login(browser, email, password, recovery_email, phone):
    try:
        print(phone)
        browser.get('https://www.youtube.com/')
        WebDriverWait(browser, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ytd-button-renderer.style-scope:nth-child(5) > a:nth-child(1)")))
        # sign_in_btn = browser.find_element_by_css_selector('a.yt-simple-endpoint.style-scope.ytd-button-renderer')
        sign_in_btn = browser.find_element_by_css_selector(
            'ytd-button-renderer.style-scope:nth-child(5) > a:nth-child(1)')
        sign_in_btn.click()

        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_inp = browser.find_element_by_id('identifierId')
        email_inp.send_keys(email)
        browser.find_element_by_id('identifierNext').click()  # đi đến trang nhập password
        sleep(5)
        # WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#headingText > content")))
        # heading_text = browser.find_element_by_css_selector('#headingText > content')
        # if heading_text.text == 'Welcome':
        #     print(heading_text.text)
        # elif heading_text.text == 'Account disabled':
        #     return 'disabled'

        WebDriverWait(browser, 60).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#headingText > content"),
                                                                          "Welcome"))
        next_btm = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "passwordNext")))
        password_inp = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                                        "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/content/section/div/content/div[1]/div/div[1]/div/div[1]/input")))
        password_inp.send_keys(password)
        browser.execute_script("arguments[0].click();", next_btm)
        try:
            WebDriverWait(browser, 30).until(
                EC.text_to_be_present_in_element((By.ID, "headingText"), 'Verify it\'s you'))
            print('Verify account')
            recovery_options = browser.find_elements_by_class_name('vdE7Oc')
            for recovery_option in recovery_options:
                print(recovery_option.text)
                if recovery_option.text == 'Confirm your recovery phone number':
                    print('Confirm your recovery phone number')
                    recovery_option.click()
                    sleep(10)
                    #
                    # select_country = WebDriverWait(browser, 60). \
                    #     until(EC.presence_of_all_elements_located(By.XPATH,
                    #                                               "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/content/section/div/content/div[2]/div/div[1]/div/div[1]/div[1]/div[233]"))
                    # select_country.click()
                    #
                    # vietnamese = WebDriverWait(browser, 60). \
                    #     until(EC.presence_of_all_elements_located(By.XPATH,
                    #                                               "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/content/section/div/content/div[2]/div/div[1]/div/div[2]/div[233]"))
                    # vietnamese.click()

                    # loop_time = 0
                    # while loop_time < 15:
                    #     phone_number_inp = None
                    #     try:
                    #
                    #         break
                    #     except Exception as ex:
                    #         if phone_number_inp:
                    #             phone_number_inp.clear()
                    #         loop_time += 1
                    phone = "+84{}".format(phone)
                    phone_number_inp = WebDriverWait(browser, 60). \
                        until(EC.presence_of_element_located((By.ID, "phoneNumberId")))
                    # phone_number_inp = browser.find_element_by_id('phoneNumberId')
                    phone_number_inp.click()

                    phone_number_inp.send_keys(phone)

                    next_btn = WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".zZhnYe")))
                    browser.execute_script("arguments[0].click();", next_btn)

                    # phone = "0{}".format(phone)
                    # phone_number_inp = WebDriverWait(browser, 60). \
                    #     until(EC.presence_of_element_located((By.ID, "phoneNumberId")))
                    # # phone_number_inp = browser.find_element_by_id('phoneNumberId')
                    # phone_number_inp.click()
                    #
                    # phone_number_inp.send_keys(phone)
                    #
                    # next_btn = WebDriverWait(browser, 30).until(
                    #     EC.presence_of_element_located((By.CSS_SELECTOR, ".zZhnYe")))
                    # browser.execute_script("arguments[0].click();", next_btn)

                elif recovery_option.text == 'Need to input recovery email':
                    print('Need to input recovery email')
                    recovery_option.click()
                    sleep(2)
                    while True:
                        try:
                            recovery_inp = browser.find_element_by_id('knowledge-preregistered-email-response')
                            recovery_inp.click()
                            recovery_inp.send_keys(recovery_email)

                            next_btn = browser.find_element_by_id('next')
                            browser.execute_script("arguments[0].click();", next_btn)
                            break
                        except:
                            pass

                elif recovery_option.text == 'Confirm your recovery email':
                    print('Confirm your recovery email')
                    recovery_option.click()
                    sleep(2)
                    while True:
                        try:
                            recovery_inp = WebDriverWait(browser, 60). \
                                until(EC.presence_of_element_located((By.ID, "identifierId")))
                            # recovery_inp = browser.find_element_by_id('identifierId')
                            recovery_inp.click()
                            recovery_inp.send_keys(recovery_email)

                            # next_btn = browser.find_element_by_css_selector('.zZhnYe')
                            next_btn = WebDriverWait(browser, 60). \
                                until(EC.presence_of_element_located((By.CSS_SELECTOR, ".zZhnYe")))
                            browser.execute_script("arguments[0].click();", next_btn)
                            break
                        except Exception as ex:
                            print(ex)

                            # WebDriverWait(browser, 30).until(EC.text_to_be_present_in_element((By.ID, "headingText"), 'Account Disabled'))
                            # return 'disabled'

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
        return 'success'
    except Exception as ex:
        print('Login failed: {}'.format(str(ex)))
        return 'fail'


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
        # watch_videos(browser, href)

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

        try:
            videos_reports = browser.find_elements_by_css_selector('.yt-uix-form-input-checkbox.report-video-checkbox')
            for i in range(4):
                video_report = random.choice(videos_reports)
                video_report.click()
        except Exception as ex:
            print('Can not check to video report: {}'.format(str(ex)))

        html = browser.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        return '1'
    except Exception as ex:
        print('Report channel failed: {}'.format(str(ex)))
        return '0'


def get_key_recaptcha(browser, xpath):
    try:
        browser.switch_to.default_content()
        iframe_switch = browser.find_element(By.XPATH, xpath)
        key = iframe_switch.get_attribute('src')
        keys = key.split('&')
        for item in keys:
            if 'k=' in item:
                key = item[2:]
                return key
    except Exception as ex:
        print('Can not switch to recaptcha checkbox: {}'.format(str(ex)))
        return None


def change_language(browser):
    try:
        while True:
            lang_btn = browser.find_element_by_id('yt-picker-language-button')
            lang_btn.click()
            sleep(2)
            langs = browser.find_elements_by_css_selector('.yt-picker-item > span')
            for lang in langs:
                if 'English' in lang.text:
                    lang.click()
                    return
    except Exception as ex:
        print('Change lang failed: {}'.format(str(ex)))


def stat_report(browser, login_status):
    while True:
        tmp_email = Email.find_random()
        email = tmp_email.email
        password = tmp_email.password
        recovery_email = tmp_email.recovery_email
        phone = tmp_email.phone
        login_response = login(browser, email, password, recovery_email, phone)
        if login_response == 'success':
            print('Logged in to youtube')
            break
        elif login_response == 'fail':
            print('{} can not login to youtube'.format(email))
            return
        elif login_response == 'disabled':
            print('{} is disabled'.format(email))
            # db.email.update({'_id': tmp_email['_id']}, {'$set': {'status': False}})
            return

    videos = Video.find_all()
    if len(videos) > 0:
        for index_video, video in enumerate(videos):
            report_needed = True
            browser.get(video.url)
            try:
                check_available = browser.find_element_by_css_selector('.reason')
                if check_available and check_available.text == 'Video unavailable':
                    video.status = 'deactive'
                    video.save_to_db()
                    report_needed = False
            except:
                pass

            try:
                if report_needed:
                    if index_video == 0:
                        # change language
                        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "avatar-btn")))
                        avatar_btn = browser.find_element_by_id('avatar-btn')
                        avatar_btn.click()

                        WebDriverWait(browser, 30).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "yt-icon.style-scope.ytd-compact-link-renderer")))
                        lang_btns = browser.find_elements_by_css_selector(
                            'yt-icon.style-scope.ytd-compact-link-renderer')
                        for index, btn in enumerate(lang_btns):
                            if index == 10:
                                btn.click()

                        WebDriverWait(browser, 30).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "p.style-scope.ytd-account-settings")))
                        lang_item = browser.find_elements_by_css_selector('p.style-scope.ytd-account-settings')
                        lang_btn = None
                        for item in lang_item:
                            if 'English (UK)' in item.text:
                                lang_btn = item
                        if lang_btn is not None:
                            lang_btn.click()

                    sleep(2)
                    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "button")))
                    buttons = browser.find_elements_by_id('button')
                    for button in buttons:
                        if button.get_attribute('aria-label') == 'More actions':
                            button.click()

                    sleep(2)
                    WebDriverWait(browser, 30).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".style-scope.ytd-menu-service-item-renderer")))
                    report_btn = browser.find_elements_by_css_selector('.style-scope.ytd-menu-service-item-renderer')
                    for btn in report_btn:
                        if btn.text == 'Report':
                            btn.click()

                    count = 0
                    while count < 10:
                        count += 1
                        titles = browser.find_elements_by_tag_name("yt-formatted-string")
                        for title in titles:
                            if title.text.lower().strip() == 'report video':
                                break
                        sleep(1)

                    report_reason = browser.find_elements_by_tag_name('yt-formatted-string')
                    for reason in report_reason:
                        if reason.text.lower() == 'spam or misleading':
                            browser.execute_script("arguments[0].click();", reason)

                    sleep(1)
                    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#input-4")))
                    dropdown_btn = browser.find_element_by_css_selector('#input-4')
                    browser.execute_script("arguments[0].click();", dropdown_btn)

                    sleep(1)
                    WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".style-scope.yt-options-renderer")))
                    reason = browser.find_elements_by_css_selector('.style-scope.yt-options-renderer')
                    for item in reason:
                        if item.text.lower().strip() == 'misleading thumbnail':
                            item.click()

                    sleep(2)
                    WebDriverWait(browser, 30).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".style-scope.yt-button-renderer.style-blue-text.size-default")))
                    text_btn = browser.find_elements_by_css_selector(
                        '.style-scope.yt-button-renderer.style-blue-text.size-default')
                    for btn in text_btn:
                        if btn.text == 'NEXT':
                            btn.click()

                    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "timestamp")))
                    input_8 = browser.find_element_by_css_selector('#input-8')
                    input_8.clear()
                    input_8.send_keys(random.randint(1, 20))
                    input_9 = browser.find_element_by_css_selector('#input-9')
                    input_9.clear()
                    input_9.send_keys(random.randint(1, 60))

                    # sleep(2)
                    # details_report = 'this video contains scam content'
                    # WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "textarea")))
                    # textarea = browser.find_element_by_id('textarea')
                    # textarea.send_keys(details_report)

                    sleep(3)
                    text_btn = browser.find_elements_by_css_selector(
                        '.style-scope.ytd-button-renderer.style-blue-text.size-default')
                    for btn in text_btn:
                        if btn.text == 'REPORT':
                            browser.execute_script("arguments[0].click();", btn)

                    count = 0
                    while count < 10:
                        count += 1
                        titles = browser.find_elements_by_id("title")
                        for title in titles:
                            if title.text.lower().strip() == 'thanks for reporting':
                                break
                        sleep(1)

                    video.count_success += 1
                    video.save_to_db()

            except Exception as ex:
                video.count_fail += 1
                video.save_to_db()
                print('Exception main: {}'.format(str(ex)))


def key_resolver_captcha(api_url):
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
                return response_key
            if 'ERROR_CAPTCHA_UNSOLVABLE' in response:
                return None
            sleep(5)
    else:
        print('Can not get key api 2captcha.com')


def report_license(browser):
    while True:
        tmp_email = Email.find_random()
        email = tmp_email.email
        password = tmp_email.password
        recovery_email = tmp_email.recovery_email
        phone = tmp_email.phone
        login_response = login(browser, email, password, recovery_email, phone)
        if login_response == 'success':
            print('Logged in to youtube')
            break
        elif login_response == 'fail':
            print('{} can not login to youtube'.format(email))
            return
        elif login_response == 'disabled':
            print('{} is disabled'.format(email))
            # db.email.update({'_id': tmp_email['_id']}, {'$set': {'status': False}})
            return

    captcha_status = True

    browser.get('https://www.youtube.com/copyright_complaint_form')

    try:
        title = browser.find_element_by_xpath('/html/body/div[1]/div/b')
        if title.text == 'About this page':
            xpath = '/html/body/div[1]/form/div/div/div/iframe'
            google_key = get_key_recaptcha(browser, xpath=xpath)
            current_url = browser.current_url
            captcha_resolver_api = 'http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}&here=now'.format(
                api_key, google_key, current_url)
            key_resolver = key_resolver_captcha(captcha_resolver_api)
            print(key_resolver)
            if key_resolver is not None:
                browser.switch_to.default_content()
                WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.ID, "g-recaptcha-response")))
                browser.execute_script(
                    "document.getElementById('g-recaptcha-response').style.display = 'block';")
                textarea_box = browser.find_element_by_id('g-recaptcha-response')
                textarea_box.send_keys(key_resolver)
                # submit_report_btn = browser.find_element_by_xpath('/html/body/div[1]/form/input[3]')
                # submit_report_btn.click()
                browser.execute_script("document.getElementById('captcha-form').submit();")
                sleep(3)
            else:
                captcha_status = False
    except Exception as ex:
        print('No Need to resolver captcha')

    videos = Video.find_all()
    for index_video, video in enumerate(videos):
        if captcha_status and video.id == 477:
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
            video_url_0.send_keys(video.url)

            issue_type_0 = Select(browser.find_element_by_id('issue_type_0'))
            issue_type_0.select_by_value('L')

            issue_details_wrapper = browser.find_element_by_class_name('issue_details_wrapper')
            conditional_value_validations = issue_details_wrapper.find_elements_by_css_selector(
                '.conditional-value-validation')
            for conditional_value_validation in conditional_value_validations:
                if conditional_value_validation.get_attribute('name') == 'issue_detail_L_title_0':
                    conditional_value_validation.send_keys(video.name)

            reason3 = 'entire video'
            position_marker = browser.find_element_by_class_name('position-marker-class-S-0')
            issue_details = position_marker.find_elements_by_css_selector('ul > li > label')
            for issue_detail in issue_details:
                issue_detail_text = issue_detail.text
                issue_detail_text = issue_detail_text.lower().strip()
                if issue_detail_text == reason3:
                    issue_detail.click()

            fake_user = FakeUser.find_random()

            owner_display_name = browser.find_element_by_id('owner_display_name')
            owner_display_name.send_keys(fake_user.name)

            requester_title = browser.find_element_by_id('requester_title')
            requester_title.send_keys(fake_user.name)

            requester_name = browser.find_element_by_id('requester_name')
            requester_name.send_keys(fake_user.name)

            address1 = browser.find_element_by_id('address1')
            address1.send_keys(fake_user.address_1)

            address2 = browser.find_element_by_id('address2')
            address2.send_keys(fake_user.address_2)

            city = browser.find_element_by_id('city')
            city.send_keys(fake_user.city)

            state = browser.find_element_by_id('state')
            state.send_keys(fake_user.state)

            zip_code = browser.find_element_by_id('zip')
            zip_code.send_keys(fake_user.zip_code)

            phone = browser.find_element_by_id('phone')
            phone.send_keys(fake_user.phone)

            country = Select(browser.find_element_by_id('country'))
            country.select_by_value('US')

            browser.find_element_by_id('checkbox_confirmation_1').click()
            browser.find_element_by_id('checkbox_confirmation_2').click()
            browser.find_element_by_id('checkbox_confirmation_3').click()
            browser.find_element_by_id('checkbox_confirmation_liability').click()
            browser.find_element_by_id('checkbox_confirmation_abuse_termination').click()
            owner_signature = browser.find_element_by_id('owner_signature')
            owner_signature.send_keys(fake_user.name)

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
                browser.execute_script("document.getElementById('submit_complaint').submit();")
                submit_report_btn = browser.find_element_by_id('submit_complaint_button')
                submit_report_btn.click()
                try:
                    change_language(browser)
                    content = browser.find_element_by_css_selector('.page-default > div > h1')
                    if content and 'Thank you' in content.text:
                        print('Submit report successfully')
                        video.count_success += 1
                        video.save_to_db()
                except Exception as ex:
                    print('Submit report failed: {}'.format(str(ex)))
                    video.count_fail += 1
                    video.save_to_db()


def get_proxy():
    # crawler_proxy = create_browser(None)
    # crawler_proxy.get('https://free-proxy-list.net/')
    # items = crawler_proxy.find_elements_by_class_name('odd')
    # items += crawler_proxy.find_elements_by_class_name('even')
    # data = []
    # for item in items:
    #     tds = item.find_elements_by_tag_name('td')
    #     # print("{}:{}".format(tds[0].text, tds[1].text))
    #     data.append({"host": tds[0].text, "port": tds[1].text})

    # crawler_proxy.quit()
    # for item in data:
    #     if ping_ok(item['host']):
    #         return item
    return None


def ping_ok(sHost):
    try:
        output = subprocess.check_output("ping -{} 1 {}". \
                                         format('n' if platform.system().lower() == "windows" else 'c', sHost),
                                         shell=True)
        output = str(output)
        print(output)
        index = output.index('time')
        ending = output.index('ms TTL')
        time = output[index + 5: ending]
        print(int(time))
        return int(time) < 300
    except Exception as e:
        print(e)
        return False


def create_browser(proxy, user_agent):
    capabilities = DesiredCapabilities.FIREFOX.copy()
    capabilities['marionette'] = True
    capabilities['acceptSslCerts'] = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("general.useragent.override", user_agent.name)
    profile.set_preference("media.volume_scale", "0.0")
    if proxy is not None:
        profile.set_preference("network.proxy.type", 1)
        # profile.set_preference("network.proxy.http", proxy['host'])
        # profile.set_preference("network.proxy.http_port",int(proxy['port']))
        # profile.set_preference("network.proxy.https",proxy['host'])
        # profile.set_preference("network.proxy.https_port",int(proxy['port']))
        # profile.set_preference("network.proxy.ftp",proxy['host'])
        # profile.set_preference("network.proxy.ftp_port",int(proxy['port']))
        # profile.set_preference("network.proxy.ssl",proxy['host'])
        # profile.set_preference("network.proxy.ssl_port",int(proxy['port']))
        profile.set_preference("network.proxy.socks", proxy['host'])
        profile.set_preference("network.proxy.socks_port", proxy['port'])
        profile.set_preference("network.proxy.socks_version", 5)

    options = webdriver.FirefoxOptions()

    print(sys.platform)
    if sys.platform == 'win32':
        geckodriver = 'etc/geckodriver-v0.21.0-win64/geckodriver.exe'
        binary = 'C:/Program Files/Mozilla Firefox/firefox.exe'
        # options.add_argument('--headless')
    else:
        geckodriver = 'etc/geckodriver-v0.21.0-linux64/geckodriver'
        binary = '/usr/bin/firefox'
        options.add_argument('--headless')

    browser = webdriver.Firefox(
        executable_path=geckodriver,
        firefox_options=options,
        capabilities=capabilities,
        firefox_binary=binary,
        firefox_profile=profile)
    browser.maximize_window()
    return browser


def start_app(session):
    browser = None
    # proxy = dict(
    #     host="127.0.0.1",
    #     port=9951
    # )
    proxy = None
    print('Start Report')

    try:
        agent = Agent.find_random()
        browser = create_browser(proxy, agent)
        login_status = False
        report_license(browser)
        browser.quit()
    except Exception as ex:
        print("Main exception error: {}".format(str(ex)))
        if browser:
            browser.quit()
