# API https://bcy.net/apiv3/common/getFeeds
# 瀑布流加载接口

import json
import requests
from typing import List

from fourdimensions.webapi.const import DEFAULT_HEADER, GETFEEDS_AVAILABLE_PARAMS

class getFeeds:
    class NoContentError(Exception):
        pass
    @staticmethod
    def get(cid: int = 6618800650505421059, refer: str = "feed", direction: str = "loadmore", sess: requests.Session = None):
        """ query https://bcy.net/apiv3/common/hotCircleList
        
        Args:
            cid: 分区编号。
            refer: 分区属性。
            direction: 瀑布流加载方向。
                以上参数请使用fourdimensions.webapi.const中提供的参数 GETFEED_AVAILABLE_PARAMS
                不要自行定义，否则可能无法按预期加载瀑布流。
        
        Return:
            r.json()
        
        Raise:
            getFeeds.NoContentError

        """

        url = "https://bcy.net/apiv3/common/getFeeds"
        params = {
            "cid": cid,
            "refer": refer,
            "direction": direction
        }

        r = sess.get(url, params=params)
        r.raise_for_status()
        response_json: dict = r.json()
        assert response_json.get('code', -1) == 0, response_json.get('msg')
    
        if response_json.get('data', {}):
            return response_json

        raise getFeeds.NoContentError("此页无内容")

    @staticmethod
    def extract_item_ids(iteminfo: dict) -> List[int]:
        assert iteminfo.get('data', {}).get('item_info')
        item_ids: List[int] = []
        item_ids.extend([int(item['item_detail']["item_id"]) for item in iteminfo['data']['item_info']])

        return item_ids

    @staticmethod
    def extract_uids(iteminfo: dict) -> List[int]:
        assert iteminfo.get('data', {}).get('item_info')
        item_ids: List[int] = []
        item_ids.extend([int(item['item_detail']["uid"]) for item in iteminfo['data']['item_info']])

        return item_ids

if __name__ == '__main__':
    sess = requests.session()
    sess.headers.update(DEFAULT_HEADER)
    feed = getFeeds.get(0, sess=sess)
    print(feed)
    # with open('getFeeds-demo.json', 'w', encoding='UTF-8') as f:
    #     json.dump(feed, f, indent=2, ensure_ascii=False)
    print(getFeeds.extract_item_ids(feed))
    print(getFeeds.extract_uids(feed))