import time
from Crypto.Hash import MD5

def getVideoReqUrl(vid, ts=None):
    if not ts:
        ts = time.time()
    user = 'duanzi'
    vtype = 'mp4'
    params = {
        'ts': ts,
        'user': user,
        'version': 1,
        'video': vid,
        'vtype': 'mp4',
    }

    signstr = ''.join(['%s%s' % (k,v) for k,v in sorted(params.items())]) + '5b94cab514c082702dca7f4c776e1b42'
    signret = MD5.new(signstr.encode('utf-8')).hexdigest()
    return f"https://ib.snssdk.com/video/play/1/{user}/{ts}/{signret}/{vtype}/{vid}?codec_type=3&projectTag=tag&player_version=2.10.78.22&ssl=0&format_type=mp4"

if __name__ == '__main__':
    print(
        getVideoReqUrl("v0d040g10000ciem7gbc77ucui5ha1bg")
    )

