DEFAULT_HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"
}

GETFEEDS_AVAILABLE_PARAMS = {
    "index": {
        "name_cn": "首页",
        "name": "index",
        "url": "https://bcy.net/",
        "api": "https://bcy.net/apiv3/common/getFeeds",
        "api_params": {
            "refer": "feed",
            "direction": "loadmore"
            }
    }, 
    
    "illust": {
        "name_cn": "绘画",
        "name": "illust",
        "url": "https://bcy.net/illust",
        "api": "https://bcy.net/apiv3/common/getFeeds",
        "api_params": {
            "refer": "channel",
            "direction": "loadmore",
            "cid": 6618800650505421059
            }
    },
    
    "coser": {
        "name_cn": "COS",
        "name": "coser",
        "url": "https://bcy.net/coser",
        "api": "https://bcy.net/apiv3/common/getFeeds",
        "api_params": {
            "refer": "channel",
            "direction": "loadmore",
            "cid": 6618800694038102275
            }
    },
    
    "ganswer_channel": {
        "name_cn": "问答",
        "name": "ganswer_channel",
        "url": "https://bcy.net/group/discover",
        "api": "https://bcy.net/apiv3/common/getFeeds",
        "api_params": {
            "refer": "ganswer_channel",
            "direction": "loadmore",
            "cid": 6618029913129615630
            }
    },
        
    "novel": {
        "name_cn": "小说",
        "name": "novel",
        "url": "https://bcy.net/novel",
        "api": "https://bcy.net/apiv3/common/getFeeds",
        "api_params": {
            "refer": "channel",
            "direction": "loadmore",
            "cid": 6618800677680316675
        }
    }
}