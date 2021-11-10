import requests
from bs4 import BeautifulSoup

requests.urllib3.disable_warnings() # 關閉requests的警告

class Crawler(object):
    domain_url = 'https://tieba.baidu.com'
    member_list_url = 'https://tieba.baidu.com/bawu2/platform/listMemberInfo'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    MAX_PAGE = 458 # 翻頁的最大頁數，貼吧會員列表只給看到458頁，再往後會顯示空頁面

    # 把貼吧url轉換成貼吧的中文名稱
    @classmethod
    def group_url_to_group_name(cls, group_url: str):
        response = requests.get(group_url, verify=False, headers=cls.header)
        soup = BeautifulSoup(response.text, "html.parser") # html模式解析
        # 百度贴吧的html有語法錯誤，BeautifulSoup無法解析到要的資料，用string硬A
        # 參考 https://www.zhihu.com/question/38001837
        text = soup.get_text().strip()
        return text[:text.find('吧-百度贴吧')]

    # 從貼吧成員名單撈出每位會員的個人頁url
    @classmethod
    def get_member_profile_link(cls, group_name: str, startPage: int = 1, endPage: int = MAX_PAGE):
        payload = {
            'word': group_name, # "吧"字不用, ex.武汉吧，只需填武汉
            'ie': 'utf-8', # 把word轉成utf8
            'pn': '1',  # 頁數
        }
        last_page = cls.get_max_page(f'{cls.member_list_url}?word={group_name}&ie=utf-8')
        if endPage > last_page:
            endPage = last_page

        with open('id_result.txt', 'w') as fp:
            for i in range(startPage, endPage+1):
                print(f'正在抓取{group_name}吧 第{i}頁(/第{endPage}頁)')
                payload['pn'] = i
                response = requests.get(cls.member_list_url, verify=False, headers=cls.header, params=payload)
                soup = BeautifulSoup(response.text, "html.parser")
                memberList = soup.find_all('a', class_='user_name')
                for member in memberList:
                    try:
                        chat_link = cls.get_chat_link(member.get("href"))
                        fp.write(chat_link + '\n')
                    except Exception:
                        print(member.text + ' 個人頁面已關閉')

    # 撈出貼吧成員名單的最大頁數 (貼吧會員列表只給看到458頁)
    @classmethod
    def get_max_page(cls, group_member_list_url: str):
        response = requests.get(group_member_list_url, verify=False, headers=cls.header)
        soup = BeautifulSoup(response.text, "html.parser")
        total_page = int(soup.find('span', class_='tbui_total_page').text[1:-1]) # 共XX頁，去掉首尾各1個字
        if total_page > cls.MAX_PAGE:
            return cls.MAX_PAGE
        else:
            return total_page

    # 從會員的個人頁url取得私訊連結
    @classmethod
    def get_chat_link(cls, profile_link: str):
        url_profile = cls.domain_url + profile_link
        response = requests.get(url_profile, verify=False, headers=cls.header)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find('a', target='sixin').get("href").split('=')[1]

# test function
if __name__ == "__main__":
    group_name = Crawler.group_url_to_group_name('https://tieba.baidu.com/f?kw=%CE%E4%BA%BA')
    Crawler.get_member_profile_link(group_name, 1, 458)