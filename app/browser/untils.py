# -*- coding: utf-8 -*-
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def find_report_link(s):
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
