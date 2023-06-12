# API https://bcy.net/apiv3/user/follow-list

import requests
from typing import List

class follow_list:
    @staticmethod
    def get(uid: int, page: int=1, follow_type: int=0, sess: requests.Session = None):
        """ query https://bcy.net/apiv3/user/follow-list
        
        Args:
            uid: 用户id
            page: 关注页面的页面数，这里相当于“划到了几次页面底部”
            follow_type: 0 - TA的关注
                         1 - TA的粉丝
                         3 - TA关注的圈子

        """

        url = "https://bcy.net/apiv3/user/follow-list"
        params = {
            "uid": uid,
            "page": page,
            "follow_type": follow_type
        }

        r = sess.get(url, params=params)
        r.raise_for_status()

        return r.json()

if __name__ == "__main__":
    sess = requests.session()
    reply = follow_list.get(4366886634525245, follow_type=1, sess=sess)
    print(reply)