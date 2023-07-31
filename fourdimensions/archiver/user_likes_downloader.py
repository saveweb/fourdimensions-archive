import base64
from datetime import datetime
import json
import os
import uuid
import shutil
import time
from pathlib import Path
from typing import List, Union
import requests
from fourdimensions.utils.image import toOrigin
from fourdimensions.webapi.user.selfPosts import selfPosts
from fourdimensions.appapi.snssdk import getVideoReqUrl
from fourdimensions.webapi.const import DEFAULT_HEADER as WEB_HEADER
from fourdimensions.appapi.const import DEFAULT_HEADER as APP_HEADER

import pymongo

mongo_client = None

def init_mongo_client():
    global mongo_client
    if mongo_client is None:
        mongo_client = pymongo.MongoClient(input("Mongo URI:"))

def get_item_detail(item_id: Union[str,int]) -> dict:
    if isinstance(item_id, int):
        item_id = str(item_id)
    global mongo_client
    if mongo_client is None:
        init_mongo_client()
    item = mongo_client.banciyuan.item.find_one({
        'item_id': item_id
    })
    if item is None:
        raise ValueError(f"item_id {item_id} not found in db")
    return item['detail'] if 'detail_fullfix' not in item else item['detail_fullfix']

REFRESH = True
def main():
    sess = requests.Session()
    # add a hook to print the url of each request
    def print_request(r, *args, **kwargs):
        print(f"{r.url}")
    sess.hooks['response'].append(print_request)

    likes_json_file = Path(input("likes*-$user-$timestamp.json 的路径:")).expanduser().resolve()
    # likes_collects-1816028322995044-1690801071375
    user_id = os.path.basename(likes_json_file).split('-')[1]

    user_likes_path = Path(f'./data/user_likes/{user_id}')

    likes_data_v2 = False

    with open(likes_json_file, 'r', encoding='utf-8') as f:
        likes_data: Union[List[dict], dict] = json.load(f)
    if isinstance(likes_data, List):
        items = likes_data
    elif isinstance(likes_data, dict):
        items = []
        likes_data_v2 = True
        items.extend(likes_data['likedata'])
        items.extend(likes_data['collectdata'])
    else:
        raise ValueError(f"likes_data is neither a list nor a dict")

    if (user_likes_path / 'items').exists(): # legacy likes_data_v1 dir
        # mv items to likedata-items
        print("!!!detected legacy likes_data_v1 dir!!!")
        time.sleep(5)
        # shutil.move(str(user_likes_path / 'items'), str(user_likes_path / 'likedata-items'))
    out_put_text_list = []
    for item_index, item in enumerate(items, 1):
        if 'out_put_text' in locals():
            print(out_put_text)
            out_put_text_list.append(out_put_text)
        out_put_text = ""
        current_like_source = 'likedata'
        if likes_data_v2:
            current_like_source = 'likedata' if item_index <= len(likes_data['likedata']) else 'collectdata'
        item_id = item["item_id"]
        item_id = str(item_id)
        try:
            item_detail = get_item_detail(item_id)
        except ValueError as e:
            print(e)
            with open(f"{user_id}-lost_item_ids", "a") as f:
                f.write(item_id+"\n")
            item_detail = item
        item_dir = user_likes_path / f'{current_like_source}-items' / item_id
        item_detail_path = item_dir /f"{item_id}.json"
        if item_detail_path.exists() and (not REFRESH):
            continue
        print(f"Starting item ({item_index}/{len(items)}): {item_id}")

        item_ctime = item_detail["ctime"]
        item_uname = item_detail["uname"]
        item_ctime_iso = datetime.fromtimestamp(int(item_ctime)).isoformat()

        # item_plain = item_detail["origin_item_detail"]["plain"] if item_detail.get("origin_item_detail") else item_plain
        out_put_text += f"tem_id: {item_id} by {item_uname} at {item_ctime_iso}:\n"
        out_put_text += f"likesdata_source: {current_like_source}\n"
        if item_title := item_detail.get("title", ""):
            out_put_text += f"title: {item_title}\n"
        if item_type := item_detail.get("type", ""):
            out_put_text += f"type: {item_type}\n"
        if item_plain := item_detail.get("plain", ""):
            out_put_text += f"plain: {item_plain}\n"
        if item_detail_plain := item_detail.get("detail_plain", ""):
            out_put_text += f"detail_plain: {item_detail_plain}\n"
        if item_content := item_detail.get("content", ""):
            out_put_text += f"content: {item_content}\n"
        if summary := item_detail.get("summary", ""):
            out_put_text += f"summary: {summary}\n"
        if item_pic_num := item_detail.get("pic_num", ""):
            out_put_text += f"pic_num: {item_pic_num}\n"
        if item_post_tags := item_detail.get("post_tags", ""):
            tag_names = []
            for tag in item_post_tags:
                tag_names.append(tag['tag_name'])
            out_put_text += f"post_tags: #{' #'.join(tag_names)}\n"
        if item_collection := item_detail.get("collection", ""):
            out_put_text += f"collection_title: {item_collection['title']}\n"

        # download pic
        sess.headers.update(WEB_HEADER)
        img_url_map = {}
        img_url_map_path = item_dir / 'img_url_map.json'
        if (not os.path.exists(img_url_map_path)):
            _uni_image_list = item_detail['multi']
            assert isinstance(_uni_image_list, list)
            if 'image_list' in item_detail:
                _uni_image_list.extend(item_detail['image_list'])
            _ori_url_added = set()
            _index = 0
            for image_detail in _uni_image_list:
                _any_url = image_detail['path']
                _ori_url = toOrigin(_any_url)
                if _ori_url not in _ori_url_added:
                    _index += 1
                    _ori_url_added.add(_ori_url)
                    img_url_map[_any_url] = {
                        'index': _index,
                        'ori_url': _ori_url,
                        'img_filename_local': f'{_index}.jpg',
                    }
            if img_url_map:
                out_put_text += f"[实际备份图片数: {len(img_url_map)}]\n"
                img_url_map_path.parent.mkdir(parents=True, exist_ok=True)
                with open(img_url_map_path, 'w', encoding='utf-8') as f:
                    json.dump(img_url_map, f, ensure_ascii=False, indent=1, separators=(',', ':'))

            for img_ele in img_url_map.values():
                item_index:int = img_ele['index']
                img_filename_local:str = img_ele['img_filename_local']
                img_path = item_dir / img_filename_local
                _ori_url = img_ele['ori_url']
                if not os.path.exists(img_path):
                    r = sess.get(_ori_url)
                    r.raise_for_status()

                    with open(img_path, 'wb') as f:
                        f.write(r.content)
                    ...

        # download video
        if item_detail['type'] == 'video':
            vid = item_detail['video_info']['vid']
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
                video_detail_path.parent.mkdir(parents=True, exist_ok=True)
                with open(video_detail_path, 'w', encoding='utf-8') as f:
                    json.dump(video_detail, f, ensure_ascii=False, indent=1, separators=(',', ':'))
            max_size = -1
            best_video_option = None
            if video_detail["video_info"]["data"]["message"] == "未通过审核，视频无法播放":
                print(f"Skipping {item_id} {video_detail['video_info']['data']['message']}")
                out_put_text += "[未通过审核，视频无法播放]\n"
                continue
            for video_option in video_detail["video_info"]["data"]["video_list"].keys():
                if video_detail["video_info"]["data"]["video_list"][video_option]["size"] > max_size:
                    max_size = video_detail["video_info"]["data"]["video_list"][video_option]["size"]
                    best_video_option = video_option
            assert best_video_option is not None
            out_put_text += f"[视频 {max_size // 1024}KiB]\n"
            video_path = video_dir / f"vid_{vid}.mp4"
            # 部分视频 size 返回 0
            if os.path.exists(video_path) and (os.path.getsize(video_path) == max_size or max_size == 0):
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
        
        if not os.path.exists(item_detail_path):
            item_detail_path.parent.mkdir(parents=True, exist_ok=True)
            with open(item_detail_path, 'w', encoding='utf-8') as f:
                json.dump(item_detail, f, ensure_ascii=False, indent=1, separators=(',', ':'))
    if REFRESH:
        with open(user_likes_path / f'{user_id}-likes-posts_plain.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(out_put_text_list))

if __name__ == "__main__":
    main()
