from urllib import parse
import requests
import json
import os

work_url = 'http://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi'
imageSizeName = [None, '215x120', '1024x768', '1280x720', '1280x1024', '1440x900', '1920x1080', '1920x1200', '1920x1440']

def GetWorkList(page):
    params = {
        '_':              '1520233935086',
        '_everyRead':     'true',
        'activityId':     '2735',
        'iActId':         '2735',
        'iAMSActivityId': '51991',
        'iFlowId':        '267733',
        'iListNum':       '20',
        'iModuleId':      '2735',
        'iOrder':         '0',
        'iSortNumClose':  '1',
        'iTypeId':        '2',
        'jsoncallback':   'jQuery171020414929862122522_1520232562762',
        'page':           page,
        'sDataType':      'JSON',
        'sVerifyCode':    'ABCD',
        'totalpage':      '0'
    }
    r = requests.get(work_url, params=params)
    work_raw = r.text
    work_json = work_raw[work_raw.find('(')+1 : -2]
    worklist = json.loads(parse.unquote(work_json))
    return worklist

def Download(worklist):
    for work in worklist['List']:
        path = work['sProdName']
        if not os.path.exists(path):
            os.mkdir(path)

        for i in range(1, 9):
            node_name = 'sProdImgNo_' + str(i)
            img_url = work[node_name][:-3] + '0'
            filename = os.path.join(path, imageSizeName[i] + '.jpg')
            if DownloadImg(img_url, filename):
                print("下载成功: %s, %s"%(path, imageSizeName[i]))

def DownloadImg(img_url, filename):
    try:
        r = requests.get(img_url, timeout=15)
    except:
        print("下载出错, %s, %s"%(e, img_url))

    with open(filename, 'wb') as f:
        f.write(r.content)
    return True

if __name__ == '__main__':
    for i in range(1, 10):
        worklist = GetWorkList(i)
        Download(worklist)
