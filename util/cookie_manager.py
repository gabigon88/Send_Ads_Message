import json
from requests import session
from selenium import webdriver

class CookieManager:
    @staticmethod
    def save_cookies(driver: webdriver, cookieFile):
        cookies = driver.get_cookies()
        jsonCookies = json.dumps(cookies)
        with open(cookieFile, 'w') as f:
            f.write(jsonCookies)
        print(f'cookies已保存為{cookieFile}')

    @staticmethod
    def read_cookies(driver: webdriver, cookieFile):
        with open(cookieFile, 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
            for cookie in listCookies:
                driver.add_cookie(cookie)
        print(f'cookies已成功讀取為{cookieFile}')

    @staticmethod
    def driver_set_cookies(driver: webdriver, cookieList):
        for cookie in cookieList:
            driver.add_cookie(cookie)
        print(f'driver已加入cookies, {cookieList}')

    @staticmethod
    def driver_get_cookies(driver: webdriver):
        cookiesList = driver.get_cookies()
        return cookiesList

    @staticmethod
    def session_set_cookies(requests_session: session, cookiesDict):
        for cookie in cookiesDict:
            requests_session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        print(f'session已加入cookies, {cookiesDict}')

    @staticmethod
    def session_get_cookies(session: session):
        cookiesDict = session.cookies.get_dict()
        return cookiesDict 