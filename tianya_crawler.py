import requests
from time import time
from bs4 import BeautifulSoup

requests.urllib3.disable_warnings() # 關閉requests的警告

class Crawler(object):
    member_list_base_url = 'http://groups.tianya.cn/group_home.jsp'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    MAX_PAGE = 10000 # 翻頁的最大頁數，天涯沒有限制可翻到第幾頁
    output_file = 'tianya_user_id.txt'

    @classmethod
    def get_member_profile_link(cls, group_id: str, startPage: int = 1, endPage: int = MAX_PAGE):
        payload = {
            'itemId': group_id,
            'tabNum': '4',
            'curPageNo': '1',
        }
        last_page = cls.get_max_page(f'{cls.member_list_base_url}?tabNum=4&itemId={group_id}')
        if endPage > last_page:
            endPage = last_page

        startTime = time() #計時開始
        with open(cls.output_file, 'w') as fp:
            for i in range(startPage, endPage+1):
                print(f'正在抓取 第{i}頁(/第{endPage}頁)')
                payload['curPageNo'] = i
                response = requests.get(cls.member_list_base_url, verify=False, headers=cls.header, params=payload)
                soup = BeautifulSoup(response.text, "html.parser")
                memberList = soup.find_all('ul', class_='user-avatar clearfix')[2].find_all('a')
                for member in memberList:
                    chat_link = member.get("href")
                    fp.write(chat_link + '\n')
        print(f'總計耗時{time() - startTime}秒')

    @classmethod
    def get_max_page(cls, group_member_list_url: str):
        response = requests.get(group_member_list_url, verify=False, headers=cls.header)
        soup = BeautifulSoup(response.text, "html.parser")
        total_page = int(soup.find('div', class_='atl-pages').get("_maxpage"))
        return total_page

# test function
if __name__ == "__main__":
    Crawler.get_member_profile_link('163889', 1, 5)