# API https://bcy.net/apiv3/group/getGroupDetail

import json
import requests
from typing import List

from fourdimensions.webapi.const import DEFAULT_HEADER

class getGroupDetail:
    class ItemNotFoundError(Exception):
        pass

    @staticmethod
    def get(gid:int, sess: requests.Session = None):
        """ query https://bcy.net/apiv3/group/getGroupDetail
        
        Args:
            gid: 话题id

        Returns:
            r.json()


        Raises:
            getGroupDetail.ItemNotFoundError: item不存在或暂时不可见。一般是 gid 不存在
        """

        # session刚创建时，其中不会有用于鉴权的_csrf_token。
        # 所以此处需要多访问一步原始的话题(group)网页，获取_csrf_token。
        if "_csrf_token" not in sess.cookies:
            r = sess.get(f"https://bcy.net/group/list/{gid}")
        _csrf_token = sess.cookies["_csrf_token"]

        url = "https://bcy.net/apiv3/group/getGroupDetail"
        data = {
            "gid": gid,
            "_csrf_token": _csrf_token
        }

        r = sess.post(url, data=data)
        r.raise_for_status()

        response_json: dict = r.json()
        if response_json.get('code', -1) == 500001 and response_json.get('msg', '') == "item不存在或暂时不可见":
            raise getGroupDetail.ItemNotFoundError(response_json.get('msg'))
        assert response_json.get('code', -1) == 0, response_json.get('msg')

        return r.json()

if __name__ == "__main__":
    sess = requests.session()
    sess.headers.update(DEFAULT_HEADER)
    for gid in [763842, 7638420000]: # 第一个存在，第二个不存在
        try:
            print('gid:', gid)
            group_detail = getGroupDetail.get(gid, sess=sess)
        except getGroupDetail.ItemNotFoundError as e:
            print(str(e))
        else:
            with open(__file__.replace(__file__.split("/")[-1], "group_detail-demo.json"), "w", encoding="utf-8") as f:
                json.dump(group_detail, f, indent=4, ensure_ascii=False)
            print('成功')
