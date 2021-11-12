import os
from time import sleep, time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util.cookie_manager import CookieManager
from util.driver_factory import DriverFactoty

username = '' # 自行填入使用者帳密
password = ''
cookieFile = 'sina_cookies.json'
user_id_file = "user_id.txt"
what_to_say = '亲，您好'

class Messager(object):
    def __init__(self):
        self.driver = DriverFactoty.create_driver(loadImage=False)
        self.wait = WebDriverWait(self.driver, 15)

    def login(self, username, password):
        # 有cookie檔了，讀cookie登入
        if os.path.isfile(cookieFile):
            # 重要: Before adding back the cookies, you need to browse to the same domain.
            driver.get('https://weibo.com/login.php') # 不帶cookies訪問
            driver.delete_all_cookies() # 刪除cookies
            CookieManager.read_cookies(driver, cookieFile)
            driver.get('https://weibo.com/login.php') # 恢復cookies後重新訪問

        # 尚未有cookie檔，以手動登入
        else:
            self.driver.get('https://weibo.com/login.php')
            self.wait.until(EC.presence_of_element_located((By.ID, 'loginname'))).send_keys(username)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))).send_keys(password)
            
            # 不知道為什麼新浪網的登入鈕 selenium點擊都沒反應
            # driver.find_element_by_xpath('//a[@node-type="submitBtn"]').click()
            
            is_continue = ''
            while is_continue != 'y' and is_continue != 'yes':
                is_continue = input('請手動登入後，輸入 y 繼續執行: ').lower()

            CookieManager.save_cookies(driver, cookieFile)
    
    def send_message(self, list_file_path: str, content: str):
        # 從txt檔讀取要發送訊息的會員清單
        fp = open(list_file_path, 'r')
        startTime = time() #計時開始

        for uid in fp:
            driver.get(f'https://api.weibo.com/chat/#/chat?to_uid={uid.strip()}')
            driver.refresh() # 新浪聊天在更換聊天對象時容易沒反應，重整確保頁面已更新
            sleep(3) # 避免發訊息過快
           
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//textarea'))).send_keys(content + Keys.ENTER)
            except Exception as e:
                print(f'uid: {uid}找不到會員')

        print(f'總計耗時{time() - startTime}秒')
        fp.close()

if __name__ == "__main__":
    sina = Messager()
    sina.login(username, password)
    sina.send_message(user_id_file, what_to_say)