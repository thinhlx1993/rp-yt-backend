# coding=utf-8
import os
import logging
import subprocess
import time
import sys
import random
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logging.basicConfig(level=logging.INFO,
                    filename="/opt/rp-yt-backend/app/browser/start.log",
                    format="%(asctime)s:%(levelname)s:%(message)s")


def create_pymongo():
    client = MongoClient("167.99.145.231",
                         username="admin",
                         password="1234567a@",
                         authSource="admin")
    db = client['test-yt']
    return db


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
    profile.set_preference("media.volume_scale", "0.0")
    profile.set_preference("general.useragent.override", user_agent['name'])
    profile.update_preferences()
    options = webdriver.FirefoxOptions()

    if os.environ.get('headless') != "0":
        options.add_argument("--headless")
        logging.info("Start headless mode")

    if sys.platform == 'win32':
        geckodriver = '../../etc/geckodriver-v0.21.0-win64/geckodriver.exe'
        binary = 'C:/Program Files/Mozilla Firefox/firefox.exe'
    else:
        geckodriver = '/opt/rp-yt-backend/etc/geckodriver-v0.21.0-linux64/geckodriver'
        binary = '/usr/bin/firefox'

    browser = webdriver.Firefox(
        executable_path=geckodriver,
        firefox_options=options,
        capabilities=capabilities,
        firefox_binary=binary,
        firefox_profile=profile)
    return browser


def get_urls_from_google(keyword, browser):
    browser.get('https://www.google.com.vn/search?q={}&tbm=vid'.format(keyword))
    search_btn = browser.find_element_by_id('mKlEF')
    search_btn.click()
    time.sleep(3)
    browser.refresh()
    videos = browser.find_elements_by_css_selector('div.rc > h3.r > a')
    for video in videos:
        href = video.get_attribute('href')
        if href and 'youtube' in href:
            video.click()
            time.sleep(random.randint(5, 50))
            browser.back()


def get_urls_from_youtube(views_channel, browser, db):
    logging.info("Start watching video")
    keyword = views_channel['keyword']
    browser.get('https://www.youtube.com/results?search_query={}'.format(keyword))
    time.sleep(2)
    items = browser.find_elements_by_tag_name('a')
    index = 0
    videos = list()

    for item in items:
        href = item.get_attribute('href')
        if href and 'watch' in href:
            videos.append(href)
    print(len(videos))
    while index < len(videos):
        browser.get(videos[index])
        index += 1
#         try:
#             player = browser.find_element_by_id('player')
#             if player:
#                 player.click()
#         except Exception as ex:
#             print('Can not start video')
        db.views.update({'_id': views_channel['_id']},
                        {'$inc': {'count': 1}})
        time.sleep(random.randint(5, 50))
        browser.back()
    logging.info("Quit browser")
    browser.quit()


def fake_ip():
    subprocess.call(['sudo', 'killall', 'firefox'])
    subprocess.call(['sudo', 'service', 'fakeip', 'restart'])


def watch_video():
    fake_ip()
    db = create_pymongo()
    totals = db.agents.count({'status': True})
    agent = db.agents.find({'status': True}).limit(-1).skip(random.randint(0, totals)).next()
    print(agent['name'])
    browser = create_browser(agent)
    browser.set_window_size(1920, 1080)
    browser.set_window_position(0, 0)
    browser.maximize_window()
    browser.get('https://youtube.com')
    views_channel_totals = db.views.count({'status': 'active'})
    views_channel = db.views.find({'status': 'active'}).limit(-1).skip(random.randint(0, views_channel_totals)).next()
    print(views_channel['keyword'])
    if views_channel:
        get_urls_from_youtube(views_channel, browser, db)
    else:
        logging.info("Not found channel")


if __name__ == "__main__":
    while True:
        try:
            watch_video()
        except Exception as ex:
            watch_video()
            print('Exception: {}'.format(str(ex)))
            logging.info("Exception: {}".format(str(ex)))
            break
