import wat
from lib import mycfg
import time
import requests

def run(api, d):
    # headers = {'Content-Type': 'application/json'}
    url = mycfg.urlPre + api
    response = requests.post(url, json=d)
    if response.status_code == 200:
        rtn = response.json()
        wat.d(rtn)
        return rtn
    else:
        wat.d(response.status_code, response.text)
        raise Exception("status_code %s, text: %s" % (response.status_code, response.text))

try:
    run('/ajaxAt/process/nodeAddDo', {
        "name": "标题 %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    })

    # run('/ajaxAt/process/nodeEditDo', {
    #     "name": "标题 %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    #     "id": 500
    # })

except Exception as e:
    print('exception: ' + e.__str__())
