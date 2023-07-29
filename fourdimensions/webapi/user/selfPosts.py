import requests
from typing import List, Union

class selfPosts:

    @staticmethod
    def get(uid: Union[int, str], since: int = 0, sess: requests.Session = None) -> dict:
        assert isinstance(uid, (str, int))
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
    def get_all_item_ids(uid: Union[str, int], sess: requests.Session = None) -> List[int]:
        """ 提取用户的全部 item_id """

        since = 0
        item_ids: List[int] = []
        while True:
            print(since, end='\r')
            data = selfPosts.get(uid, since, sess)
            if not data['data'].get('items'):
                break
            since = selfPosts.find_newest_since(data)
            item_ids.extend([int(item['item_detail']["item_id"]) for item in data['data']['items']])
        assert len(item_ids) == len(set(item_ids))

        return item_ids
    
    @staticmethod
    def get_all_items(uid: Union[str, int], sess: requests.Session = None) -> List[dict]:
        """ 提取用户的全部 items """

        since = 0
        items: List[dict] = []
        while True:
            print(since, end='\r')
            data = selfPosts.get(uid, since, sess)
            if not data['data'].get('items'):
                break
            since = selfPosts.find_newest_since(data)
            items.extend(data['data']['items'])
        # assert len(items) == len(set(items))

        return items

if __name__ == "__main__":
    sess = requests.Session()
    item_ids = selfPosts.get_all_item_ids(uid=1398173406082551, sess=sess)
    print(item_ids)
