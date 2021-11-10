from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

class DriverFactoty:
    @staticmethod
    def create_driver(headless: bool = False, loadImage: bool = True):
        options = Options()
        options.add_argument("--window-size=1600,900")
        options.add_argument("--window-position=1920,0")
        options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 禁止打印log
        options.add_argument('--disable-gpu') # Temporarily needed if running on Windows.
        options.add_argument('--no-sandbox') # Bypass OS security model

        if headless:
            options.add_argument('--headless') # 啟動無頭模式
        
        if loadImage:
            flag = 1
        else:
            flag = 2

        prefs = { # 1代表允許加載、2代表禁止加載
            'profile.default_content_setting_values': {
                'notifications': 2, # 禁用瀏覽器彈窗
                'images': flag, # 禁止圖片加載
            }
        }
        options.add_experimental_option('prefs', prefs) 

        browser = webdriver.Chrome(options=options) # 使用 Chrome 的 WebDriver
        # wait = WebDriverWait(browser, 20)
        
        return browser