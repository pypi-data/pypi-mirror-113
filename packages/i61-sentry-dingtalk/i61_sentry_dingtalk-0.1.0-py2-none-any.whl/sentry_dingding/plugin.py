# coding: utf-8

import time
import hmac
import hashlib
import base64
import urllib.parse

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm



DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}&timestamp={timestamp}&sign={sign}"
# default_title = u"【P{}】异常报警 \n [project]: {}"

class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'sankyutang'
    version = sentry_dingding.VERSION
    description = 'upgraded DingTalk integrations for sentry. '
    slug = 'i61-Sentry-DingTalk'
    title = 'i61-Sentry-DingTalk'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm
    
    def is_sign(self, secret, timestamp):
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign
        
    def create_title_str(self, event):
        # event_data = json.dumps(dict(event.data))
        level = event.data.get('level')
        level_msg = '发生异常报警'
        level_num = '0'
        if level == 'info':
            level_num = '3'
            level_msg = '产生日志记录'
        elif level == 'warning':
            level_num = "2"
            level_msg = '有警告提示'
        elif level == 'error':
            level_num = '1'
        else:
            level_num = "0"
        
        title = u"【P{}】项目[{}]{}".format(level_num, event.project.slug, level_msg)
        return title
    
    def create_text_str(self, title, group, event): 
        keyword = self.get_option('keyword', group.project)
        # event_data = self.get_option('data', event)
        # event_data = json.dumps(dict(event.data))
        # contexts = json.dumps(event_data.data, default=dumper, indent=10)
        # print event
        # print(event_data)
        # print(event_data.data)
        environment = event.data.get('environment', 'unknow')
        # print(environment)
        level = event.data.get('level', 'log')
        # print(level)
        req = event.data.get('request')
        # print(req)
        reqUrl = req.get('url')
        # print(reqUrl)
        contexts = event.data.get('contexts')
        # print(contexts)
        browser = contexts.get('browser')
        device = contexts.get('device')
        os = contexts.get('os')
        # print(browser)
        # print(device)
        # print(os)
        str_browser = u"{name} | {type} | {version}".format(
            name=browser.get('name'),
            type=browser.get('type'),
            version=browser.get('version')
        )
        # print(str_browser)
        str_device = u"{brand} | {family} | {model}".format(
            brand=device.get('brand'),
            family=device.get('family'),
            model=device.get('model')
        )
        # print(str_device)
        str_os = u"{name} {version}".format(
            name=os.get('name'),
            version=os.get('version')
        )
        # print(str_os)
        # environment = self.get_option('environment', event_data)
        # level = event_data.level
        
        
        text = u"### {title} \n #### {message} \n > **[Project]** {project}  \n  **[Env]** {env}  \n  **[platform]** {platform}  \n  **[level]** {level}  \n  **[OS]** {os_info}  \n  **[device]** {device_info}  \n  **[browser]** {browser_info}  \n  **[URL]** {reqUrl}  \n  {keyword} \n\n [[查看详情]({url})] \n\n  温馨提示：异常信息只保留几天，请及时查看并处理！ ".format(
            title=title,
            message=event.message,
            url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
            # event=str(event.message),
            keyword=keyword,
            project=event.project,
            platform=event.platform,
            env=environment,
            level=level,
            reqUrl=reqUrl,
            os_info=str_os,
            device_info=str_device,
            browser_info=str_browser
            # reqUrl=reqUrl
            # proj=event.tags.project,
            # id=event.event_id,
            # requestFrom=event.request.url,
            # Environment: {env} \n Project: {proj} \n Id: {id} \n RequestFrom:{requestFrom}
        )
        return text
        # return u'测试'

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option('access_token', group.project)
        keyword = self.get_option('keyword', group.project)
        secret = self.get_option('secret', group.project)
        timeStamp = str(round(time.time() * 1000))
        sign = self.is_sign(secret, timeStamp)
        send_url = DingTalk_API.format(token=access_token,timestamp=timeStamp,sign=sign)

        title = self.create_title_str(event)
        text = self.create_text_str(title, group, event)

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
