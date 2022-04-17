import re
import pytest
import requests
from common.yaml_util import YamlUtil

class TestRequest:
    def login(self, username, password):
        url = 'http://121.41.98.227/backend/login/'
        user = {"name": username, "pwd": password}
        rep = requests.request('post', url, json=user)
        if rep.json()['error']['code'] == 10001:
            print("登录失败")
        else:
            print("登录成功")
            YamlUtil().write_extract_yaml({'Set-Cookie': re.match(r"(.*) 'Set-Cookie': '(.*?); expires=", str(rep.headers), re.M | re.I).group(2)})
        return rep.json()

    @pytest.mark.run(order=1)
    def test_login_01(self):
        """用户名和密码正确"""
        u1 = self.login("root", "root")
        assert u1['success'] == True

    @pytest.mark.run(order=2)
    def test_login_02(self):
        """用户名正确，密码错误"""
        u2 = self.login("root", "1234")
        assert u2['error']['code'] == 10001
        # print(u1['error'])

    @pytest.mark.run(order=5)
    def test_logout(self):
        url = 'http://121.41.98.227/backend/logout/'
        headers = {"Cookie": YamlUtil().read_extract_yaml('Set-Cookie')}
        rep = requests.request('delete', url, params=headers)
        assert rep.json()['success'] == True
        TestRequest.cookies = ''

    @pytest.mark.run(order=3)
    def test_userInfo(self):
        url = 'http://121.41.98.227/backend/user/'
        headers = {"Cookie": YamlUtil().read_extract_yaml('Set-Cookie')}
        rep = requests.request('get', url, headers=headers)
        assert rep.json()['data']['name'] == "root"

    @pytest.mark.run(order=4)
    def test_projectlist(self):
        url = 'http://121.41.98.227/backend/projects/'
        headers = {"Cookie": YamlUtil().read_extract_yaml('Set-Cookie')}
        rep = requests.request('get', url, params=headers)
        assert rep.json()['success'] == True

