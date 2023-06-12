import requests
from typing import List

class selfPosts:

    @staticmethod
    def get(uid, since: int = 0, sess: requests.Session = None) -> dict:
        """ query https://bcy.net/apiv3/user/selfPosts 
        
        Args:
            since: 从这个时间戳开始，第一次查询时为 0 (最新)
        
        """

        url = "https://bcy.net/apiv3/user/selfPosts"
        params = {
            "uid": uid,
            "since": since,
        }
        r = sess.get(url,params=params)
        r.raise_for_status()

        return r.json()

    @staticmethod
    def find_newest_since(data: dict) -> int:
        """ 从 get() 返回的数据中找到最新的 since """
        since = data['data']['items'][-1]['since']
        since = int(since)

        return since

    @staticmethod
    def get_all_item_ids(uid, sess: requests.Session = None) -> List[str]:
        """ 提取用户的全部 item_id """
        since = 0
        item_ids = [] # type: list[str]
        while True:
            print(since, end='\r')
            data = selfPosts.get(uid, since, sess)
            if not data['data'].get('items'):
                break
            since = selfPosts.find_newest_since(data)
            item_ids.extend([item['item_detail']["item_id"] for item in data['data']['items']])
        assert len(item_ids) == len(set(item_ids))

        return item_ids

if __name__ == "__main__":
    sess = requests.Session()
    item_ids = selfPosts.get_all_item_ids(uid=int(input("uid: ")), sess=sess)
    print(item_ids)
