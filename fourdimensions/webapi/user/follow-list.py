# API https://bcy.net/apiv3/user/follow-list

import json
import requests
from typing import List

class Follow_List:
    class NoContentError(Exception):
        pass
    @staticmethod
    def get(uid: int, page: int, follow_type: int, sess: requests.Session = None):
        """ query https://bcy.net/apiv3/user/follow-list
        
        Args:
            uid: 用户id
            page: 从 1 开始
            follow_type: 0 - TA的关注
                         1 - TA的粉丝
                         3 - TA关注的圈子
        
        Return:
            r.json()
        
        Raise:
            follow_list.NoContentError

        """
        assert follow_type in [0, 1, 3]

        url = "https://bcy.net/apiv3/user/follow-list"
        params = {
            "uid": uid,
            "page": page,
            "follow_type": follow_type
        }

        r = sess.get(url, params=params)
        r.raise_for_status()
        response_json: dict = r.json()
        assert response_json.get('code', -1) == 0, response_json.get('msg')
    
        if follow_type in [0, 1]:
            if response_json.get('data', {}).get('user_follow_info'):
                return response_json
        elif follow_type == 3:
            if response_json.get('data', {}).get('user_follow_circles'):
                return response_json

        # print(response_json)
        raise Follow_List.NoContentError("此页无内容")

    @staticmethod
    def extract_uids(follow_list: dict) -> List[int]:
        """ NOTE: 只接受 follow_type 为 0 或 1 的 follow_list"""
        assert follow_list.get('data', {}).get('user_follow_info'), "只接受 follow_type 为 0 或 1 的 follow_list"
        item_ids: List[int] = []
        item_ids.extend([int(item["uid"]) for item in follow_list['data']['user_follow_info']])

        return item_ids
    
    @staticmethod
    def extract_circle_id(follow_list: dict) -> List[int]:
        # TODO: ...
        raise NotImplementedError

if __name__ == "__main__":
    sess = requests.session()
    from itertools import count
    for page in count(1):
        print(f"== {page} ==")
        try:
            follow_list = Follow_List.get(uid=4366886634525245, page=page, follow_type=1, sess=sess)
            uids = Follow_List.extract_uids(follow_list)
            print("uids:", uids)
        except Follow_List.NoContentError:
            print('完成')
            break
        else:
            with open(__file__.replace(__file__.split("/")[-1], "follow-list-demo.json"), "w", encoding="utf-8") as f:
                json.dump(follow_list, f, indent=4, ensure_ascii=False)
