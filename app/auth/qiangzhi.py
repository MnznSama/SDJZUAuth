import base64
import re
import requests


class QZClient:
    """山东建筑大学强智教务系统"""

    baseURL = 'https://xjwgl.sdjzu.edu.cn/jsxsd/'
    verifycode = 'verifycode.servlet'

    def __init__(self, session=None):
        """
        初始化 QZClient，支持外部传入 session
        :param session: 可选的 requests.Session 对象
        """
        self.session = session if session else requests.Session()
        self.is_login = False

    def is_logged_in(self):
        """检查当前 session 是否仍然有效"""
        return self.is_login and bool(self.session.cookies.get_dict())

    def get_verifycode(self):
        """
        获取验证码
        :return: 验证码图片字节流
        """
        return self.session.get(self.baseURL + self.verifycode).content

    def login(self, student_id, password, verifycode):
        """
        登录到教务系统
        :param student_id: 学号
        :param password: 密码
        :param verifycode: 验证码
        :return: 登录成功后的 cookie
        """
        encode = base64.b64encode(student_id.encode()).decode() + "%%%" + base64.b64encode(password.encode()).decode()
        data = {
            "loginMethod": "LoginToXk",
            "userAccount": student_id,
            "userPassword": password,
            "RANDOMCODE": verifycode,
            "encoded": encode
        }
        r = self.session.post(self.baseURL + '/xk/LoginToXk', data)
        msg = re.findall('<font color="red" size="2" id="showMsg">(.*)</font>', r.text)
        if msg:
            raise ValueError(msg[0].strip())

        cookie = self.session.cookies.get_dict()
        if 'JSESSIONID' not in cookie:
            raise ValueError('登录失败，未获取到有效的会话信息')

        self.is_login = True
        return cookie

    def get_session(self):
        """返回当前 session"""
        return self.session
