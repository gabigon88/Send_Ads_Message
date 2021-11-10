from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
import SimpleDriverFactory

username = '' # 自行填入使用者帳密
password = ''
what_to_say = '亲，您好，交个朋友'
user_list_file = "tianya_user_id.txt"

class Messager(object):
    def __init__(self):
        self.driver = SimpleDriverFactory.create_driver(loadImage=2)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self, username, password):
        self.driver.get('http://groups.tianya.cn/')
        self.wait.until(EC.presence_of_element_located((By.ID, 'js_login'))).click()
        self.wait.until(EC.presence_of_element_located((By.ID, 'vwriter'))).send_keys(username)
        self.wait.until(EC.presence_of_element_located((By.ID, 'vpassword'))).send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

    def send_message(self, list_file_path: str, content: str):
        startTime = time() #計時開始
        fp = open(list_file_path, 'r') 
        for url in fp:
            self.driver.get(url)
            if '出错了' in self.driver.title:
                print(f'{url.strip()} 用戶不存在')
                continue
            
            # 要先加關注才能私訊，如果未加關注就先按關注
            followBtn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="relate-oper"]/a')))
            if '已加关注' not in followBtn.text:
                followBtn.click()
                try: # 把關注後的彈跳窗關閉，但不知道為什麼有時候彈跳窗不會出現
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//input[@class="cancel"]'))).click()
                except Exception:
                    pass
                    
            self.wait.until(EC.presence_of_element_located((By.ID, 'sendMsg_content'))).send_keys(content)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="sendmsg-btn"]'))).click()
            sleep(1)
                
        print(f'總計耗時{time() - startTime}秒')
        fp.close()

if __name__ == "__main__":
    tianya = Messager()
    tianya.login(username, password)
    tianya.send_message(user_list_file, what_to_say)