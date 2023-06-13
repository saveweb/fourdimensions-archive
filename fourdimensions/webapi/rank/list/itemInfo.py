""" 占位 comment """

"""
# Web HTML 对应的榜单：

https://bcy.net/illust/toppost100
https://bcy.net/coser/toppost100 # html 路径是 coser，但是 api 那边 param 是 cos
https://bcy.net/novel/toppost100

## 参数：
    ?type={week|lastday|newPeople}&date=20230613
    周榜，日榜，新人榜。周榜的 date 也是每天都有。
"""

import json
from typing import List
import requests

from fourdimensions.webapi.const import DEFAULT_HEADER

class ItemInfo:
    class NoContentError(Exception):
        pass

    @staticmethod
    def get(ttype: str, sub_type: str, date: int, sess: requests.Session, page: int = 1):
        """
        Args:
            ttype: {illust|cos|novel} 类型榜
            sub_type: {week|lastday|newPeople} 子榜
            date: int, YYYYMMDD 格式，如 20230521

        Returns:
            r.json()

        Raises:
            ItemInfo.NoContentError: 所选榜单在 这天(date)/这页(page) 没内容
        """
        assert ttype in ["illust", "cos", "novel"]
        assert sub_type in ["week", "lastday", "newPeople"]
        assert 20000101 <= date <=20240101

        url = "https://bcy.net/apiv3/rank/list/itemInfo"
        params = {
            "p": page,
            "ttype": ttype,
            "sub_type": sub_type,
            "date": date,
        }
        r = sess.get(url, params=params)
        r.raise_for_status()
        response_json: dict = r.json()
        assert response_json.get('code', -1) == 0, response_json.get('msg')
        if response_json.get('data', {}).get('top_list_item_info'):
            return response_json
        
        raise ItemInfo.NoContentError("此页无内容")
    
    @staticmethod
    def extract_item_ids(iteminfo: dict) -> List[int]:
        assert iteminfo.get('data', {}).get('top_list_item_info')
        item_ids: List[int] = []
        item_ids.extend([int(item['item_detail']["item_id"]) for item in iteminfo['data']['top_list_item_info']])

        return item_ids

    @staticmethod
    def extract_uids(iteminfo: dict) -> List[int]:
        assert iteminfo.get('data', {}).get('top_list_item_info')
        item_ids: List[int] = []
        item_ids.extend([int(item['item_detail']["uid"]) for item in iteminfo['data']['top_list_item_info']])

        return item_ids



if __name__ == '__main__':
    sess = requests.Session()
    sess.headers.update(DEFAULT_HEADER)
    from itertools import count
#   for ttype in ["illust", "cos", "novel"]:
    for page in count(1):
        print(f'== {page} ==')
        try:
            iteminfo = ItemInfo.get(ttype="illust", sub_type="lastday", date=20230613, sess=sess, page=page)
            item_ids = ItemInfo.extract_item_ids(iteminfo)
            uids = ItemInfo.extract_uids(iteminfo)
            print('item_ids:',item_ids)
            print('uids:', uids)
        except ItemInfo.NoContentError:
            if page == 1:
                raise # 此榜单在这一天没有任何数据
            else:
                print('完成')
                break
        else:
            with open(__file__.replace(__file__.split("/")[-1], "iteminfo-demo.json"), "w", encoding="utf-8") as f:
                json.dump(iteminfo, f, indent=4, ensure_ascii=False)
