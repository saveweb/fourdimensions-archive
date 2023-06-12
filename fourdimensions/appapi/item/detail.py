import requests
import json
from typing import Union

from fourdimensions.appapi.utils.auth import enc_data
from fourdimensions.appapi.const import DEFAULT_HEADER

class Detail:
    @staticmethod
    def get(item_id: Union[str, int], sess: requests.Session = None) -> dict:
        assert isinstance(item_id, (str, int))
        url = "https://api-hl.bcy.net/apiv2/item/detail"
        params = {
            "item_id": item_id,
        }
        enced_data = enc_data(json.dumps(params, separators=(",", ":")))
        real_params = {
            "data": enced_data,
        }
        r = sess.post(url, data=real_params, headers=DEFAULT_HEADER)
        r.raise_for_status()
        return r.json()


if __name__ == "__main__":
    sess = requests.Session()
    detail = Detail.get(
            item_id=7242590634538703933,
            sess=sess,
            )
    with open(__file__.replace(__file__.split("/")[-1], "detail-demo.json"), "w", encoding="utf-8") as f:
        json.dump(detail, f, indent=4, ensure_ascii=False)