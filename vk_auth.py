__author__ = 'Gor'
import urllib.request as ur
import urllib.parse as up
import http.cookiejar as hc
import lxml.html, re
import requests as r
#http://habrahabr.ru/post/143972/   and    https://github.com/dzhioev/vk_api_auth/blob/master/vk_auth.py

class parser:
    """Парсим формы в поисках нужных полей для подтверждения вопросов"""
    def __init__(self, response):
        html = lxml.html.fromstring(response)
        self.params = {}
        self.get_data(html)

    def get_data(self, html):
        self.url = html.xpath('//form')[0].get('action')
        for i in html.xpath('//input'):
            if i.get("type") in ["hidden", "text", "password"]:
                self.params[i.get("name")] = i.get("value")

def auth(email, password, client_id, scope):
    opener = ur.build_opener(ur.HTTPCookieProcessor(hc.CookieJar()), ur.HTTPRedirectHandler())
    response = r.get("http://oauth.vk.com/oauth/authorize?redirect_uri=http://oauth.vk.com/blank.html&response_type=token&client_id=%s&scope=%s&display=wap"%(str(client_id), str(scope))).content
    pars = parser(response)
    pars.params["email"] = email
    pars.params["pass"] = password
    res = opener.open(pars.url, up.urlencode(pars.params).encode('cp1251'))
    try: key = re.findall('access_token=[a-zA-Z0-9]+', res.geturl())[0][13:]
    except:
        pars = parser(res.read())
        res = opener.open(pars.url, up.urlencode(pars.params).encode('cp1251'))
        key = re.findall('access_token=[a-zA-Z0-9]+', res.geturl())[0][13:]
    return key
