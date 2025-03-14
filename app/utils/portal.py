import re


def GetPhone(client):#返回手机号
    ssoclient = client.sso
    s = ssoclient.session

    res = s.get(url='https://portal.sdjzu.edu.cn/user/setting')
    phoneNumber = re.search(r'<input type="hidden" name="mobilePhone" id="phone" value="(.*?)"/>',res.text).group(1)
    return phoneNumber