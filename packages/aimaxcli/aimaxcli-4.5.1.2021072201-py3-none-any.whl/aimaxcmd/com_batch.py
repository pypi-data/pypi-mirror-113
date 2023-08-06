import os

from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command
import aimaxcmd.cmds_base as base
import logging
import requests
import aimaxsdk.tool as tool
import json
import time

from aimaxcmd.yml_list import Yml

ymlkey ={}

class CommonBatchAdd(Command,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonBatchAdd, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonBatchAdd, self).get_parser(prog_name))
        i = len(parser.prog.split(' '))
        return parser



    def take_action(self, parsed_args):
        super(CommonBatchAdd, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        headers = {"Content-Type": "application/json"}
        body = {}
        base_url = "http://{}:{}/s".format(auth_info["address"], auth_info["port"])
        base_uri = base_url
        filepath = input("Please input file: ")
        with open(filepath,'r') as f:
            lines = f.readlines()
            for line in lines:
                time.sleep(2)
                line = line.encode('utf-8').decode()
                user_dic  = json.loads(line.strip())
                print(user_dic['username']) # 结果 {'province': 'GuangDong', 'city': 'ShenZhen'}
                print(user_dic['groupId']) # 结果 {'province': 'GuangDong', 'city': 'ShenZhen'}
                print(line.strip())



                #查询是否重复
                base_url = base_uri
                base_url = "{}{}".format(base_url,"/api/auth/user")
                base_url = "{}/{}".format(base_url,user_dic['username'])
                if token:
                    base_url = "{}?token={}".format(base_url,token)
                body_data = json.dumps(line.strip())
                print(base_url)
                response = requests.get(base_url, headers=headers)
                print(response)
                ok,sid = tool.parse_response(response, "obj","id")
                print(sid)

                if ok:
                    print("用户已存在： {} ".format(user_dic['username']))
                    continue
                else:
                    print("用户不存在： {}  开始添加".format(user_dic['username']))
                #harbor
                base_url = base_uri
                base_url = "{}{}".format(base_url,"/api/image/images/addHarborUser")
                if token:
                    base_url = "{}?token={}".format(base_url,token)
                base_url = "{}&{}={}".format(base_url,"harborUser",user_dic['username'])
                base_url = "{}&{}={}".format(base_url,"groupId",user_dic['groupId'])
                body_data = json.dumps(body)
                print(base_url)
                response = requests.post(base_url, data=body_data, headers=headers)
                ok,psd = tool.parse_response(response, "user","password")
                print(psd)
                if ok:
                    self.app.LOG.info("Succeed to add1 ")
                else:
                    self.app.LOG.info("Failed to add {}".format(body_data))
                #解析 response的user获取password
                #user
                base_url = base_uri
                base_url = "{}{}".format(base_url,"/api/auth/user")
                if token:
                    base_url = "{}?token={}".format(base_url,token)
                base_url = "{}&{}={}".format(base_url,"harborUser",user_dic['username'])
                base_url = "{}&{}={}".format(base_url,"password",psd)
                body_data = line.strip()
                print(base_url)
                response = requests.post(base_url, data=body_data.encode('utf-8'), headers=headers)
                print(response)
                ok = tool.parse_response(response, None)
                if ok:
                    self.app.LOG.info("Succeed to add2 ")
                else:
                    self.app.LOG.info("Failed to add {}".format(body_data))

                #根据username获取userid
                base_url = base_uri
                base_url = "{}{}".format(base_url,"/api/auth/user")
                base_url = "{}/{}".format(base_url,user_dic['username'])
                if token:
                    base_url = "{}?token={}".format(base_url,token)
                body_data = json.dumps(line.strip())
                print(base_url)
                response = requests.get(base_url, headers=headers)
                print(response)
                ok,uid = tool.parse_response(response, "obj","id")
                print(uid)
                if ok:
                    self.app.LOG.info("Succeed to add3 ")
                else:
                    self.app.LOG.info("Failed to add {}".format(body_data))

                #解析 response的user获取userid
                #user
                base_url = base_uri
                base_url = "{}{}".format(base_url,"/api/auth/quotas")
                if token:
                    base_url = "{}?token={}".format(base_url,token)
                userquota = user_dic['userquota']
                userquota['userId'] = uid
                body_data = json.dumps(userquota)
                print(userquota)
                print(base_url)
                response = requests.post(base_url, data=body_data, headers=headers)
                print(response)
                ok = tool.parse_response(response, None)
                if ok:
                    self.app.LOG.info("Succeed to add4 ")
                else:
                    self.app.LOG.info("Failed to add {}".format(body_data))

                #创建存储卷
                #user
                base_url = base_uri
                base_url = "{}{}".format(base_url,"/api/storage/volumes/dirs/homedir")
                if token:
                    base_url = "{}?token={}".format(base_url,token)
                userquota = user_dic['userquota']
                userquota['userId'] = uid
                body_data = json.dumps(userquota)
                print(userquota)
                print(base_url)
                response = requests.post(base_url, data=body_data, headers=headers)
                print(response)
                ok = tool.parse_response(response, None)
                if ok:
                    self.app.LOG.info("Succeed to add5 ")
                else:
                    self.app.LOG.info("Failed to add {}".format(body_data))
            f.closed




def fun_zab(fun_name,str):
    #print('11111111111111111111111111111111111111')
    if fun_name == 'zab':
        return "{}{}".format(str,'-zabbix-agent')
    return str