import pytest
import requests
from common.yaml_util import YamlUtil
from testcases.test_start import TestRequest

def test_servicelist():
    url = 'http://121.41.98.227/backend/services/?project_id=7'
    # TestRequest().login("root", "root")
    headers = {"Cookie": YamlUtil().read_extract_yaml('Set-Cookie')}
    rep = requests.request('get', url, headers=headers)
    assert rep.json()['data'][0]['project_id'] == 7

def test_addservice():
    url = 'http://121.41.98.227/backend/services/'
    headers = {"Cookie": YamlUtil().read_extract_yaml('Set-Cookie')}
    json = {"name": "模块1", "description": "模块1", "project_id": 7}
    rep = requests.request('post', url, headers=headers, json=json)
    YamlUtil().write_extract_yaml({"service_id": rep.json()['data']['id']})
    assert rep.json()['success'] == True

def test_delservice():
    url = 'http://121.41.98.227/backend/service/'+str(YamlUtil().read_extract_yaml('service_id'))+'/'
    print(url)
    headers = {"Cookie": YamlUtil().read_extract_yaml('Set-Cookie')}
    rep = requests.request('delete', url, headers=headers)
    assert rep.json()['success'] == True