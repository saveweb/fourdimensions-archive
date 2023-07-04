import datetime
from itertools import count
import json
import os
import threading
import requests
from fourdimensions.webapi.const import DEFAULT_HEADER

from fourdimensions.webapi.rank.list.itemInfo import ItemInfo

def main():
    sess = requests.Session()
    sess.headers.update(DEFAULT_HEADER)
    today = datetime.date.today()
    print(today)
    threads = []
    for ttype in ["illust", "cos", "novel"]:
        for sub_type in ["lastday", "newPeople"]:
            # multithread
            t = threading.Thread(target=download_ranking, args=(today, ttype, sub_type, sess))
            threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
def download_ranking(today: datetime.date, ttype: str, sub_type: str, sess: requests.Session):
    continued_failed = 0
    # 从今天开始，往前无限期爬取
    # date: int, 20230613 -> 20230612 -> ...
    for date in count(int(today.strftime("%Y%m%d")), -1):
        # check date is valid
        try:
            # 又不是不能用
            datetime.datetime.strptime(str(date), '%Y%m%d')
        except ValueError:
            continue

        if os.path.exists(f'data/ranking-uids-{ttype}-{sub_type}-{date}.txt'):
            print(f'== {ttype} {sub_type} {date} 已存在 ==')
            continue

        print(f'== {ttype} {sub_type} {date} ==')
        try:
            iteminfo = ItemInfo.get(ttype=ttype, sub_type=sub_type, date=date, sess=sess, page=1)
            item_ids = ItemInfo.extract_item_ids(iteminfo)
            uids = ItemInfo.extract_uids(iteminfo)
            print('item_ids:',len(item_ids))
            print('uids:', len(uids))
            write_iteminfo(ttype,sub_type,date,iteminfo)
            write_item_ids(ttype,sub_type,date,item_ids)
            write_uids(ttype,sub_type,date,uids)
        except ItemInfo.NoContentError:
            continued_failed += 1
            if continued_failed >= 100:
                print(f"!=== {ttype} {sub_type} {date} 完成 ===!")
                break
            print('空，下一个', continued_failed)
            continue

def write_iteminfo(ttype,sub_type,date,iteminfo: dict):
    with open(f"data/ranking-iteminfo-{ttype}-{sub_type}-{date}.json", "w", encoding="utf-8") as f:
        json.dump(iteminfo, f, ensure_ascii=False)
def write_item_ids(ttype,sub_type,date,item_ids: list):
    with open(f"data/ranking-item_ids-{ttype}-{sub_type}-{date}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(map(str, item_ids)))
def write_uids(ttype,sub_type,date,uids: list):
    with open(f"data/ranking-uids-{ttype}-{sub_type}-{date}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(map(str, uids)))

if __name__ == '__main__':
    main()