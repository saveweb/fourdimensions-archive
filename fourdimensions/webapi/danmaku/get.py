import json
import logging
import requests

from fourdimensions.webapi.const import DEFAULT_HEADER

from typing import TypedDict


class Danmaku(TypedDict):
    item_id: str
    danmaku_id: int
    bcy_uid: int
    text: str
    text_color: str
    show_digg_num: bool
    offset_time: int
    digg_count: int
    bury_count: int
    device_id: int
    ctime: int
    app_id: int
    digg_status: int
    status: int
    source: int


class Danmakus:
    class NoDanmakuError(Exception):
        pass

    @staticmethod
    def get(item_id: int, sess: requests.Session, duration: int = 10000000, offset_time: int = 0):
        """
        Args:
            item_id: 动态编号
            duration: 返回的弹幕列表的最大时长（毫秒），改大了不会报错
            offset_time: 返回的弹幕列表的起始时间（毫秒），第一次请求是 0，后续请求是上一次请求的最后一个弹幕的 end_end_offset_time
        Returns:
            r.json()
        Raises:
            Danmaku.NoDanmakuError: 未找到弹幕
        """

        url = "https://bcy.net/apiv3/danmaku/get"
        params = {
            "item_id": item_id,
            "duration": duration,
            "offset_time": offset_time
        }

        r = sess.get(url, params=params)
        r.raise_for_status()

        response_json: dict = r.json()
        assert response_json.get('code', -1) == 0, response_json.get('msg')
        if response_json.get('data', {}).get('danmakus'):
            return response_json

        logging.info(f"{item_id} 的弹幕列表为空: {r.text}")
        raise Danmakus.NoDanmakuError(f"{item_id} 的弹幕列表为空")

    @staticmethod
    def get_all(item_id: int, sess: requests.Session, duration: int = 10000000, offset_time: int = 0) -> list[Danmaku]:
        """ 获取所有弹幕
        Args:
            item_id: 动态编号
            duration: 返回的弹幕列表的最大时长（毫秒），改大了不会报错
            offset_time: 返回的弹幕列表的起始时间（毫秒），第一次请求是 0，后续请求是上一次请求的最后一个弹幕的 end_end_offset_time
        Returns:
            list[Danmaku]
        Raises:
            Danmaku.NoDanmakuError: 未找到弹幕
        """

        danmakus: list[Danmaku] = []
        while True:
            try:
                response_json = Danmakus.get(
                    item_id, sess, duration, offset_time)
            except Danmakus.NoDanmakuError:
                break
            danmakus.extend(response_json['data']['danmakus'])
            offset_time = response_json['data']['end_offset_time']
        return [Danmaku(danmaku) for danmaku in danmakus]


if __name__ == "__main__":
    sess = requests.session()
    sess.headers.update(DEFAULT_HEADER)
    try:
        danmaku = Danmakus.get_all(7183032689077787660, sess=sess)
        with open(__file__.replace(__file__.replace("\\", '/').split("/")[-1], "danmaku-demo.json"), "w", encoding="utf-8") as f:
            json.dump(danmaku, f, ensure_ascii=False, indent=4)
        print("弹幕数量:", len(danmaku))
    except Danmakus.NoDanmakuError:
        print("没有弹幕")
