import requests
from typing import List

# 参考格式 https://bcy.net/apiv3/cmt/reply/list?page=1&item_id=()&limit=15&sort=hot

class reply_list:
    @staticmethod
    def get(item_id, page: int=1, limit:int =15, sort:str ='hot', sess: requests.Session = None):
        """ query https://bcy.net/apiv3/cmt/reply/list
        
        Args:
            item_id: 需要爬取评论的主楼/动态本身的编号
            page: 评论页码
            limit: 每页最大评论数量

        """

        url = "https://bcy.net/apiv3/cmt/reply/list"
        params = {
            "page": page,
            "item_id": item_id,
            "limit": limit,
            "sort": sort
        }
        r = sess.get(url,params=params)
        r.raise_for_status()

        return r.json()

if __name__ == "__main__":
    sess = requests.session()
    reply = reply_list.get(7240818866773826618, sess=sess)
    print(reply)