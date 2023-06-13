# API https://bcy.net/apiv3/common/circleFeed?circle_id=48707&since=rec:2&sort_type=1&grid_type=10
# since: (const str)"rec:"+str(int(page))
#      此处since充当的作用相当于page
# sort_type: 1 热门动态
#            2 最新动态

# 用于https://bcy.net/tag/48707之类的圈子页面。
# 打开这个页面时，其中会默认填充20个item。

import json
import requests
from typing import List

from fourdimensions.webapi.const import DEFAULT_HEADER

class CircleFeed:
    class NoContentError(Exception):
        pass
    @staticmethod
    def get(circle_id: int, since: str = "rec:0", sort_type: int = 1, grid_type: int = 10, sess: requests.Session = None):
        """ query https://bcy.net/apiv3/common/circleFeed
        
        Args:
            circle_id: 圈子id
            since: 从这个页面开始
                   需要注意：第一次查询时不一定为 "rec:0"！
                   目前只捕获到"rec:2"及以后一些的记录！
                   务必注意这里的since不是单纯的int，而是"rec:%d"的格式！
            sort_type: 1 - 热门动态
                       2 - 最新动态
            grid_type: 【暂时作用不明】
        
        Return:
            r.json()
        
        Raise:
            CircleFeed.NoContentError

        """
        assert sort_type in [1, 2]

        url = "https://bcy.net/apiv3/common/circleFeed"
        params = {
            "circle_id": circle_id,
            "since": since,
            "sort_type": sort_type,
            "grid_type": grid_type
        }

        r = sess.get(url, params=params)
        r.raise_for_status()
        response_json: dict = r.json()
        assert response_json.get('code', -1) == 0, response_json.get('msg')
    
        if response_json.get('data', {}):
            return response_json

        raise CircleFeed.NoContentError("此页无内容")

if __name__ == '__main__':
    sess = requests.session()
    sess.headers.update(DEFAULT_HEADER)
    circlefeed = CircleFeed.get(48707, since="rec:0", sort_type=1, sess=sess)
    print(circlefeed)