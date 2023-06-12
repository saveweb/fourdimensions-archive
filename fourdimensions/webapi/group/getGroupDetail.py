# API https://bcy.net/apiv3/group/getGroupDetail

import requests
from typing import List

class getGroupDetail:
    @staticmethod
    def get(gid:int, sess: requests.Session = None):
        """ query https://bcy.net/apiv3/group/getGroupDetail
        
        Args:
            gid: 话题id
            sess: requests创建的session，此处需要用到其中的_csrf_token鉴权，所以必须填写。

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

        return r.json()

if __name__ == "__main__":
    sess = requests.session()
    reply = getGroupDetail.get(763842, sess=sess)
    print(reply)