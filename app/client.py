from auth.sso import SSOAuth
from auth.qiangzhi import QZClient

class SDJZUClient:
    """山东建筑大学 SDK 入口"""
    student_id = ""
    password = ""

    def __init__(self, student_id, password):
        """初始化 SDK 并登录"""
        self.sso = SSOAuth()
        self.qz = QZClient()
        self.student_id = student_id
        self.password = password

    def login_portal(self):
        """登录到门户系统"""
        self.sso.login(self.student_id, self.password, 'https://portal.sdjzu.edu.cn/')
        return self.sso

    def login_h5(self):
        """登录到 H5 页面"""
        self.sso.login(self.student_id, self.password, 'https://static.sdjzu.edu.cn/h5-dorm/#/')
        return self.sso

    def login_qiangzhi(self, sso=True, v_code=""):
        """登录到强智教务系统
        :param bool sso: 是否使用 SSO 登录
        :param str v_code: 验证码（非 SSO 登录时需要）
        :return: QZClient 对象
        """
        if sso:
            # SSO 登录
            self.sso.login(self.student_id, self.password, 'https://xjwgl.sdjzu.edu.cn/sso.jsp')
            return self.sso
        else:
            # **非 SSO 登录，复用 SSO 的 session**
            if not v_code:
                raise ValueError('请提供验证码')

            self.qz.login(self.student_id, self.password, v_code)
            return self.qz

    def get_verifycode(self):
        """获取验证码
        :return: 验证码图片字节流
        """
        return self.qz.get_verifycode()

    def login_etong(self):
        """登录到一卡通系统"""
        self.sso.login(self.student_id, self.password, 'https://etong.sdjzu.edu.cn/sso/home/index?cShoolType=1')
        return self.sso

