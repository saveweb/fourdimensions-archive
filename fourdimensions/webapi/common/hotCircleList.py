# API https://bcy.net/apiv3/common/hotCircleList

import json
import requests
from typing import List

from fourdimensions.webapi.const import DEFAULT_HEADER

class hotCircleList:
    class NoContentError(Exception):
        pass
    @staticmethod
    def get(offset: int = 0, sess: requests.Session = None):
        """ query https://bcy.net/apiv3/common/hotCircleList
        
        Args:
            offset: 偏移量，使用方法上相当于page。
        
        Return:
            r.json()
        
        Raise:
            hotCircleList.NoContentError

        """

        url = "https://bcy.net/apiv3/common/hotCircleList"
        params = {
            "offset": offset
        }

        r = sess.get(url, params=params)
        r.raise_for_status()
        response_json: dict = r.json()
        assert response_json.get('code', -1) == 0, response_json.get('msg')
    
        if response_json.get('data', {}):
            return response_json

        raise hotCircleList.NoContentError("此页无内容")

if __name__ == '__main__':
    sess = requests.session()
    sess.headers.update(DEFAULT_HEADER)
    circlefeed = hotCircleList.get(0, sess=sess)
    print(circlefeed)