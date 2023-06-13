import requests
import json
from typing import Union

from fourdimensions.appapi.utils.auth import enc_data
from fourdimensions.appapi.const import DEFAULT_HEADER

class Detail:
    @staticmethod
    def get(uid: int, sess: requests.Session = None) -> dict:
        assert isinstance(uid, int)
        url = "https://api.bcy.net/apiv2/user/detail"
        params = {
            "uid": uid,
        }
        enced_data = enc_data(json.dumps(params, separators=(",", ":")))
        real_params = {
            "data": enced_data,
        }
        r = sess.post(url, data=real_params)
        r.raise_for_status()
        return r.json()


if __name__ == "__main__":
    sess = requests.Session()
    sess.headers.update(DEFAULT_HEADER)
    detail = Detail.get(
            uid=4314949551391112,
            sess=sess,
            )
    with open(__file__.replace(__file__.split("/")[-1], "detail-demo.json"), "w", encoding="utf-8") as f:
        json.dump(detail, f, indent=4, ensure_ascii=False)