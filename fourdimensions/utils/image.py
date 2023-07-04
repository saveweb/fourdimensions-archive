import re


def toOrigin(url: str):
    """
    获取原图的方法：
        - 去掉域名里的 `-sign`
        - 把 `~` 后的字符串全部替换为 `tplv-banciyuan-obj.image`
    
    NOTE: 不确定 p3-bcy.bcyimg.com 有没有 WAF 风控。
    """
    
    """image demo:
    1. https://p3-bcy-sign.bcyimg.com/banciyuan/user/2353324/item/web/17aqk/54bb4220361a11eba34523c6d1a16ed2.jpg~tplv-banciyuan-4X6.image?x-expires=1702691343&x-signature=Z%2BUNSVwT9KU%2B33DIyYgVtuK8tLs%3D
    2. https://p3-bcy-sign.bcyimg.com/banciyuan/user/19/daily/176vm/00b01670a1ff11e486df2fc24feba7c7.jpg~tplv-banciyuan-w650.image?x-expires=1703003308&x-signature=wE6w%2BoOokmX%2BTGH%2F4Z4D8AtqDFw%3D
    3. https://p3-bcy-sign.bcyimg.com/banciyuan/coser/10081/post/177hq/6599ed805d5811e5829757ebf56f179f.jpg~tplv-banciyuan-sq360.image?x-expires=1703003863&x-signature=KjB6E8Fck2P22acE2xv0O%2FyXDio%3D
    4. https://p3-bcy-sign.bcyimg.com/banciyuan/4dd291e0c7af4cf0b12839ac44a03644~tplv-bcyx-yuan-logo-v1:wqnojZLnpZ54aWdlcgrljYrmrKHlhYMgLSBBQ0fniLHlpb3ogIXnpL7ljLo=.image?x-expires=1703000107&x-signature=i3Lvkyvom%2BJCYlyQjKl76IX1Blg%3D
    """
    assert "://p3-bcy-sign.bcyimg.com/" in url and "~" in url
    url = url.replace("://p3-bcy-sign.bcyimg.com/", "://p3-bcy.bcyimg.com/")
    url = re.sub(r"~.*", "~tplv-banciyuan-obj.image", url)
    return url