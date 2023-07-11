import base64
import json
import os
import shutil
import time
from pathlib import Path
import requests
from fourdimensions.appapi.item.detail import Detail
from fourdimensions.utils.image import toOrigin
from fourdimensions.webapi.user.selfPosts import selfPosts
from fourdimensions.appapi.snssdk import getVideoReqUrl
from fourdimensions.webapi.const import DEFAULT_HEADER as WEB_HEADER
from fourdimensions.appapi.const import DEFAULT_HEADER as APP_HEADER

users = [
        "int64",# 此处添加用户 uid
    ]


def main():
    sess = requests.Session()
    # add a hook to print the url of each request
    def print_request(r, *args, **kwargs):
        print(f"{r.url}")
    sess.hooks['response'].append(print_request)

    for uid in users:
        user_path = Path(f'./data/users/{uid}')
        uid = str(uid)
        if not os.path.exists(user_path / 'item_ids.txt'):
            sess.headers.update(WEB_HEADER)
            item_ids = selfPosts.get_all_item_ids(uid=uid, sess=sess)
        else:
            with open(user_path / 'item_ids.txt', 'r', encoding='utf-8') as f:
                item_ids = [int(item_id) for item_id in f.read().splitlines()]
        os.makedirs(user_path,  exist_ok=True)
        with open(user_path / 'item_ids.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join([str(item_id) for item_id in item_ids]))
        for index, item_id in enumerate(item_ids, 1):
            print(f"Starting item ({index}/{len(item_ids)}): {item_id}")
            item_id = str(item_id)
            item_dir = user_path / 'items' / item_id
            item_detail_path = item_dir /f"{item_id}.json"
            if os.path.exists(item_detail_path):
                item_detail = json.load(open(item_detail_path, 'r', encoding='utf-8'))
            else:
                sess.headers.update(APP_HEADER)
                item_detail = Detail.get(item_id, sess=sess)
                os.makedirs(item_dir, exist_ok=True)
                with open(item_detail_path, 'w', encoding='utf-8') as f:
                    json.dump(item_detail, f, ensure_ascii=False, indent=1, separators=(',', ':'))
            
            # download pic
            sess.headers.update(WEB_HEADER)
            img_url_map = {}
            img_url_map_path = item_dir / 'img_url_map.json'
            if (not os.path.exists(img_url_map_path)) or True:
                for index, multi in enumerate(item_detail['data']['multi'], 1):
                    # TODO: save to file
                    old_img_fielname_local = item_dir / f'{index}.pic'
                    img_filename_local = f'{index}.jpg'
                    img_path = item_dir / img_filename_local
                    if os.path.exists(old_img_fielname_local):
                        shutil.move(old_img_fielname_local, img_path)
                    any_url = multi['path']
                    ori_url = toOrigin(any_url)
                    if not os.path.exists(img_path):
                        r = sess.get(ori_url)
                        r.raise_for_status()

                        with open(img_path, 'wb') as f:
                            f.write(r.content)
                        ...

                    img_url_map[any_url] = {
                        'index': index,
                        'ori_url': ori_url,
                        'img_filename_local': img_filename_local,
                    }
                if img_url_map:
                    with open(img_url_map_path, 'w', encoding='utf-8') as f:
                        json.dump(img_url_map, f, ensure_ascii=False, indent=1, separators=(',', ':'))

            # download video
            if item_detail['data']['type'] == 'video':
                vid = item_detail['data']['video_info']['vid']
                video_dir = item_dir / "video"
                video_detail_path = video_dir / f"vid_{vid}.json"
                if os.path.exists(video_detail_path):
                    video_detail = json.load(open(video_detail_path, 'r', encoding='utf-8'))
                else:
                    video_req_url = getVideoReqUrl(vid)
                    sess.headers.update({
                        "User-Agent": "okhttp/3.10.0.1",
                    })
                    video_req = sess.get(video_req_url)
                    video_req.raise_for_status()
                    video_detail = video_req.json()
                    os.makedirs(video_detail_path.parent, exist_ok=True)
                    with open(video_detail_path, 'w', encoding='utf-8') as f:
                        json.dump(video_detail, f, ensure_ascii=False, indent=1, separators=(',', ':'))
                max_size = 0
                best_video_option = None
                if video_detail["video_info"]["data"]["message"] == "未通过审核，视频无法播放":
                    print(f"Skipping {item_id} {video_detail['video_info']['data']['message']}")
                    continue
                for video_option in video_detail["video_info"]["data"]["video_list"].keys():
                    if video_detail["video_info"]["data"]["video_list"][video_option]["size"] > max_size:
                        max_size = video_detail["video_info"]["data"]["video_list"][video_option]["size"]
                        best_video_option = video_option
                assert best_video_option is not None
                video_path = video_dir / f"vid_{vid}.mp4"
                if os.path.exists(video_path) and os.path.getsize(video_path) == max_size:
                    print(f"Skipping {item_id} {max_size}/{max_size}")
                    continue
                main_url = base64.b64decode(video_detail["video_info"]["data"]["video_list"][best_video_option]["main_url"]).decode('utf-8')
                sess.headers.update({
                    "User-Agent": "ttplayer(2.9.52.21),AVMDL-1.0.31.1-boringssl-boringssl-ANDROID",
                    "X-MDL-User-Agent": "AVMDL-1.0.31.1-boringssl-boringssl-ANDROID",
                    "X-ReqType": "play",
                    "icy-metadata": "1",
                    "Range": "bytes=0-",
                })
                video_req = sess.get(main_url, stream=True)
                video_req.raise_for_status()
                with open(video_path, 'wb') as f:
                    donwloaded_size = 0
                    for chunk in video_req.iter_content(chunk_size=1024*1024):
                        donwloaded_size += len(chunk)
                        print(f"Downloading {item_id} {donwloaded_size}/{max_size}", end='\r')
                        f.write(chunk)
                # time.sleep(3)

if __name__ == "__main__":
    main()