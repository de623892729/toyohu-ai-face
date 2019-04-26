# -*- coding: utf-8 -*-
"""
Created on Wed May 30 16:33:14 2018

@author: Administrator
"""
from flask import Flask, url_for
from flask_cors import CORS
from aip import AipFace
from base64 import b64encode
from base64 import b64decode
import time
import json
from flask import request

""" 你的 APPID AK SK """
APP_ID = '你的app——Id'
API_KEY = '你的api_key'
SECRET_KEY = '你的secret_key'

# 获取一个百度api客户端
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

app = Flask(__name__)
CORS(app)

# 构建返回对象
def rtnObj(code, msg, data=None):
    if data != None:
        return json.dumps({ "code":code, "msg":msg, "data": data }, ensure_ascii=False)
    else:
        return json.dumps({ 'code':code, 'msg':msg }, ensure_ascii=False)

@app.route('/')
def index(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '****************童育汇 人脸识别服务程序****************'

# 提取人脸数据
@app.route('/facesDetect/')
def facesDetect(faceurl=None, imageType=None):
#    image = 'https://reso.toyohu.com/crs/picture/0_1527583084001_pointStore.png?imageView2/2/w/640'


    if imageType == "BASE64":
        image = faceurl
        imageType = "BASE64"
    else:
        if not request.args.get("faceurl"):
            return rtnObj(0,'必须输入图片地址')
        if request.args.get("faceurl").upper().startswith('HTTP'):
            image = request.args.get("faceurl")
            imageType = "URL"
        else:
            with open(request.args.get("faceurl"), "rb") as imageFile:
                byte_content = imageFile.read()
            base64_bytes = b64encode(byte_content)
            image = base64_bytes.decode('utf-8')
            imageType = "BASE64"

    options = {}
    options["max_face_num"] = 10
    options["face_field"] = "age,expression,gender,glasses,landmark,race,quality,facetype,faceshape,beauty"
    rtn = client.detect(image, imageType, options) 
    print('-----------------------------------------------------')

    if rtn['error_code'] == 0:

        print('脸数量：', rtn['result']['face_num'])

#        #检查图片大小
        if (rtn['result']['face_list'][0]['location']['width'] < 200 or rtn['result']['face_list'][0]['location']['height'] < 200):
            return rtnObj(4,'照片中脸太小')
        else:
            return rtnObj(1, '', rtn['result'])

        return rtnObj(1, '', rtn['result'])
    else:
        if rtn['error_code'] == 222202:
            print('***************************')
            return rtnObj(2,'没有检测到人脸')
        else:
            return rtnObj(0,'检测出错')
# 提取人脸数据
@app.route('/facesNum/')
def facesNum(faceurl=None, imageType=None):
#    image = 'https://reso.toyohu.com/crs/picture/0_1527583084001_pointStore.png?imageView2/2/w/640'


    if imageType == "BASE64":
        image = faceurl
        imageType = "BASE64"
    else:
        if not request.args.get("faceurl"):
            return rtnObj(0,'必须输入图片地址')
        if request.args.get("faceurl").upper().startswith('HTTP'):
            image = request.args.get("faceurl")
            imageType = "URL"
        else:
            with open(request.args.get("faceurl"), "rb") as imageFile:
                byte_content = imageFile.read()
            base64_bytes = b64encode(byte_content)
            image = base64_bytes.decode('utf-8')
            imageType = "BASE64"

    options = {}
    options["max_face_num"] = 10
    options["face_field"] = "age,expression,gender,glasses,landmark,race,quality,facetype,faceshape,beauty"
    rtn = client.detect(image, imageType, options) 
    print('-----------------------------------------------------')

    if rtn['error_code'] == 0:

        return rtnObj(1, '', rtn['result']['face_num'])
    else:
        if rtn['error_code'] == 222202:
            print('***************************')
            return rtnObj(2,'没有检测到人脸')
        else:
            return rtnObj(0,'检测出错')
        
# 人脸检查Core
def faceDetect(image, imageType):

    options = {}
    options["max_face_num"] = 2
    options["face_field"] = "age,angel,expression,gender,glasses,landmark,race,quality,facetype,faceshape,beauty"

    rtn = client.detect(image, imageType, options)
    print(rtn)
    if rtn['error_code'] == 0:
        # 如果脸数量大于1张，错误
        if rtn['result']['face_num'] > 1:
            return rtnObj(3,'只能有一张脸')
        else:
            #检查图片大小
            if (rtn['result']['face_list'][0]['location']['width'] < 150 or rtn['result']['face_list'][0]['location']['height'] <150):
                return rtnObj(4,'请靠近镜头')
            else:
                if(rtn['result']['face_list'][0]['location']['rotation'] > 10 or rtn['result']['face_list'][0]['location']['rotation'] <-10):
                    return rtnObj(5,'照片中面部偏移的幅度过大')
                else:
                    if(rtn['result']['face_list'][0]['angle']['yaw'] >8 or rtn['result']['face_list'][0]['angle']['yaw'] <-8):
                        return rtnObj(5,'请勿左右旋转')
                    else:
                        if(rtn['result']['face_list'][0]['angle']['pitch'] > 15 or rtn['result']['face_list'][0]['angle']['pitch'] <-15):
                            return rtnObj(5,'请勿抬头或低头')
                        else:
                            if(rtn['result']['face_list'][0]['angle']['roll'] > 8 or rtn['result']['face_list'][0]['angle']['roll'] <-8):
                                return rtnObj(5,'请保持端正')
                            else:
                                if(rtn['result']['face_list'][0]['face_probability'] <0.8):
                                    return rtnObj(6,'无法识别')
                                else:
                                    if(rtn['result']['face_list'][0]['quality']['blur'] >0.2):
                                        return rtnObj(7,'照片太模糊')
                                    else:
                                        if(rtn['result']['face_list'][0]['quality']['illumination'] <120):
                                            return rtnObj(8,'光照度不够')
                                        else:
                                            if(rtn['result']['face_list'][0]['quality']['completeness']!=1):
                                                return rtnObj(9,'脸部不完整')
                                            else:
                                                print(rtn['result']['face_list'][0]['face_token'])
                                                return rtnObj(1, '可以使用', rtn['result'])
    else:
        if rtn['error_code'] == 222202:
            return rtnObj(2,'没有检测到人脸')
        else:
            return rtnObj(0,'检测出错')

# 人脸检查（错误情况：没有， 超过一人，脸太小，），并返回人脸数据 —— (Base64字符串方式)
@app.route('/faceDetectByBase64/', methods=['POST'])
def faceDetectByBase64(facestr=None):
#    image = 'E:\\baiduFace\\faces\\hk.jpg'
    if not request.form['facestr']:
        return rtnObj(0,'必须输入图片的Base64编码字符串')

    image = request.form['facestr'].replace("data:image/jpg;base64,", "")
    imageType = "BASE64"

    return faceDetect(image, imageType)

# 人脸检查（错误情况：没有， 超过一人，脸太小，），并返回人脸数据 —— (本地文件方式)
@app.route('/faceDetectByLocalfile/')
def faceDetectByLocalfile(faceurl=None):
#    image = 'E:\\baiduFace\\faces\\hk.jpg'
    if request.args.get("faceurl"):
        faceurl = request.args.get("faceurl")
    else:
        faceurl = faceurl

    with open(faceurl, "rb") as imageFile:
        byte_content = imageFile.read()
    base64_bytes = b64encode(byte_content)
    image = base64_bytes.decode('utf-8')
    imageType = "BASE64"
    print(image)
    return faceDetect(image, imageType)
#    return image

# 人脸检查（错误情况：没有， 超过一人，脸太小，），并返回人脸数据 —— (Url文件方式)
@app.route('/faceDetectByUrl/')
def faceDetectByUrl(faceurl=None):
#    image = 'https://reso.toyohu.com/crs/picture/0_1527583084001_pointStore.png?imageView2/2/w/640'
    if request.args.get("faceurl"):
        image = request.args.get("faceurl")
    else:
        image = faceurl
    imageType = "URL"

    return faceDetect(image, imageType)

# 人脸检查（错误情况：没有， 超过一人，脸太小，），并返回人脸数据 —— (Url文件方式)
@app.route('/faceDetect/')
def faceDetectAll(faceurl=None):
#    image = 'https://reso.toyohu.com/crs/picture/0_1527583084001_pointStore.png?imageView2/2/w/640'
    if not request.args.get("faceurl"):
        return rtnObj(0,'必须输入图片地址')

    if request.args.get("faceurl").upper().startswith('HTTP'):
        image = request.args.get("faceurl")
        imageType = "URL"
    else:
        with open(request.args.get("faceurl"), "rb") as imageFile:
            byte_content = imageFile.read()
        base64_bytes = b64encode(byte_content)
        image = base64_bytes.decode('utf-8')
        imageType = "BASE64"

    return faceDetect(image, imageType)

# 人脸注册
@app.route('/faceRegister/')
def faceRegister():
    # 参数检验
    if not request.args.get("faceurl"):
        return rtnObj(0,'必须输入人脸图片地址')
    if not request.args.get("userid"):
        return rtnObj(0,'必须输入用户Id')

    #调用获取头像方法
    face = faceDetectByUrl(request.args.get("faceurl"))
    faceObj = json.loads(face)
    print(faceObj)
    if faceObj['code'] == 1:
        facetoken = faceObj['data']['face_list'][0]['face_token']
        image = facetoken
        imageType = 'FACE_TOKEN'
        if request.args.get("groupId"):
            groupId = request.args.get("groupId")
        else:
            groupId = "karltest" #多集合直接逗号分隔
        userId = request.args.get("userid")
        options = {}
        if request.args.get("userInfo"):
            options["user_info"] = request.args.get("userInfo")

        rtn = client.addUser(image, imageType, groupId, userId, options)
        if rtn['error_code'] == 0:
            return rtnObj(1, '', rtn['result'])
        else:
            print(rtn['error_msg'])
            return rtnObj(0,'注册出错')
    else:
        return rtnObj(0,'检测出错')

# 人脸更新
@app.route('/faceUpdate/')
def faceUpdate():
    # 参数检验
    if not request.args.get("faceurl"):
        return rtnObj(0,'必须输入人脸图片地址')
    if not request.args.get("userid"):
        return rtnObj(0,'必须输入用户Id')

    #调用获取头像方法
    face = faceDetectByUrl(request.args.get("faceurl"))
    faceObj = json.loads(face)
    if faceObj['code'] == 1:
        facetoken = faceObj['data']['face_list'][0]['face_token']
        image = facetoken
        imageType = 'FACE_TOKEN'
        if request.args.get("groupId"):
            groupId = request.args.get("groupId")
        else:
            groupId = "karltest" #多集合直接逗号分隔
        userId = request.args.get("userid")
        options = {}
        if request.args.get("userInfo"):
            options["user_info"] = request.args.get("userInfo")

        rtn = client.updateUser(image, imageType, groupId, userId, options)
        if rtn['error_code'] == 0:
            return rtnObj(1, '', rtn['result'])
        else:
            print(rtn['error_msg'])
            return rtnObj(0,'注册出错')
    else:
        return rtnObj(0,'检测出错')

# 按用户id查找人脸
@app.route('/faceByUser/')
def faceByUser(userid=None):
    # 参数检验
    if not request.args.get("userid"):
        return rtnObj(0,'必须输入用户Id')

    if request.args.get("userid"):
        userId = request.args.get("userid")
    else:
        userId = userid

    if request.args.get("groupId"):
        groupId = request.args.get("groupId")
    else:
        groupId = "karltest" #多集合直接逗号分隔

    # 通过用户id搜索faceToken
    rtn = client.faceGetlist(userId, groupId)
    if rtn['error_code'] == 0:
        if len(rtn['result']['face_list']) > 0:
            return rtnObj(1, '', rtn['result']['face_list'])
        else:
            return rtnObj(2,'没有对应的用户数据')
    else:
        print(rtn['error_msg'])
        return rtnObj(0,'查找用户出错')

# 获取用户组中用户列表
@app.route('/userList/')
def userList():
    if request.args.get("groupId"):
        groupId = request.args.get("groupId")
    else:
        groupId = "karltest" #多集合直接逗号分隔ZZ

    rtn = client.getGroupUsers(groupId)
    if rtn['error_code'] == 0:
        if len(rtn['result']['user_id_list']) > 0:
            return rtnObj(1, '', rtn)
        else:
            return rtnObj(2,'没有用户')
    else:
        print(rtn['error_msg'])
        return rtnObj(0,'查找用户出错')

# 获取用户组中删除用户
@app.route('/faceUnRegister/')
def faceUnRegister():
    # 参数检验
    if not request.args.get("userid"):
        return rtnObj(0,'必须输入用户Id')

    userId = request.args.get("userid")
    if request.args.get("groupId"):
        groupId = request.args.get("groupId")
    else:
        groupId = "karltest" #多集合直接逗号分隔

    # 通过用户id搜索faceToken，调接口删除之
    faces = faceByUser(userId)

    faceObj = json.loads(faces)
    if faceObj['code'] == 1:
        for face in faceObj['data']:     # 第一个实例
            print(face['face_token'])
            facetoken = face['face_token']
            result = client.faceDelete( userId, groupId, facetoken)
            if result['error_code'] != 0:
                return rtnObj(0,'移除用户出错')
                break
        return rtnObj(1,'移除用户成功')
    else:
        return rtnObj(0, faceObj['msg'])

# 用户组中查找用户
@app.route('/faceSearch/', methods=['GET', 'POST'])
def faceSearch(groupIdList=None):

    if request.args.get("groupId"):
        groupId = request.args.get("groupId")
    else:
        groupId = "karltest" #多集合直接逗号分隔

    # 先找出图片中的每一张脸
    if request.method == 'POST':
        facedata = json.loads(request.data)
        faces = facesDetect(facedata['faceurl'], "BASE64")
    else:
        if not request.args.get("faceurl"):
            return rtnObj(0,'必须输入头像图片地址')
        faces = facesDetect(request.args.get("faceurl"))

    facesObj = json.loads(faces)
    print(facesObj)
    if facesObj['code'] == 1:
        faceArray = []
        for face in facesObj['data']['face_list']:
            # 脸逐个查找
            rtn = client.search(face['face_token'], 'FACE_TOKEN', groupId);
            if rtn['error_code'] == 0:
                if (rtn['result']['user_list'][0]['score'] >= 60):
                    faceArray.append(rtn['result']['user_list'][0])
        if len(faceArray) > 0:

            # 如果是base64，保存为本地图片,图片名称使用到毫秒的时间戳
            if request.args.get("imageType") == "BASE64":
                imgdata = b64decode(facedata['faceurl'])
                timestamp = time.time()
                time_local = time.localtime(timestamp)
                dt = time.strftime("%Y%m%d%H%M%S",time_local)
                picname = 'outpic/' + dt + '.jpg'
                
                # 增加水印
                
                
                file = open(picname, 'wb')
                file.write(imgdata)
                file.close()

                return rtnObj(1, '', {'pic':picname, 'user_list': faceArray})
            else:
                return rtnObj(1, '', {'pic':request.args.get("faceurl"), 'user_list': faceArray})
        else:
            return rtnObj(0,'查找出错1')
    else:
        return rtnObj(0,'查找出错2')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)