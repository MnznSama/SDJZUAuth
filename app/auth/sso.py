import requests


class SSOAuth:
    """山东建筑大学 SSO 统一认证"""

    SSO_URL = 'https://sso.sdjzu.edu.cn/index.php?'

    def __init__(self):
        """初始化一个 Session 对象，保证所有请求复用同一会话"""
        self.session = requests.Session()




    def is_logged_in(self):
        """检查当前 session 是否仍然有效"""
        return self.is_login and bool(self.session.cookies.get_dict())

    def login(self, student_id, password, location_url):
        """
        通过 SSO 登录系统
        :param str student_id: 学号
        :param str password: 密码
        :param str location_url: 需要登录的系统 URL
        :return dict: 登录后的 cookies
        """
        if not student_id or not password or not location_url:
            raise ValueError('学号、密码和目标系统 URL 不能为空')

        payload = {
            'rid': 'verifyWebUser',
            '_eventId': 'submit',
            'username': student_id,
            'password': password,
            'locationurl': location_url
        }

        try:
            response = self.session.get(url=self.SSO_URL, params=payload, allow_redirects=False)
        except requests.RequestException as e:
            raise ConnectionError(f"网络请求失败: {e}")

        if response.status_code != 302:
            raise ValueError('登录失败，请检查学号和密码是否正确')

        cookies = self.session.cookies.get_dict()
        if not cookies.get('PHPSESSID') or not cookies.get('CTTICKET'):
            raise ValueError('登录失败，未获取到有效的会话信息')

        if 'etong.sdjzu.edu.cn' in location_url:
            # 处理 e通二次跳转
            etong_url = response.headers.get('Location')
            if not etong_url:
                raise ValueError('二次跳转 URL 解析失败')

            try:
                etong_url = self.session.get(etong_url, cookies={'PHPSESSID': cookies['PHPSESSID'], 'CTTICKET': cookies['CTTICKET']}, allow_redirects=False).headers.get('Location')
                if etong_url:
                    self.session.get(etong_url, cookies={'PHPSESSID': cookies['PHPSESSID'], 'CTTICKET': cookies['CTTICKET']})
            except requests.RequestException as e:
                raise ConnectionError(f"二次跳转失败: {e}")

            # 重新获取 cookies 确保有效
            cookies = self.session.cookies.get_dict()
            if not cookies.get('CTTICKET') or not cookies.get('PHPSESSID'):
                raise ValueError('登录失败，未获取到有效的会话信息')

        if 'xjwgl.sdjzu.edu.cn' in location_url:
            # 处理教务系统二次跳转
            qz_url = response.headers.get('Location')
            if not qz_url:
                raise ValueError('二次跳转 URL 解析失败')

            try:
                response = self.session.get(qz_url)
            except requests.RequestException as e:
                raise ConnectionError(f"二次跳转失败: {e}")

            if response.status_code != 200:
                raise ValueError('登录失败，未获取到有效的会话信息')

            cookies = self.session.cookies.get_dict()
            if 'JSESSIONID' not in cookies:
                raise ValueError('登录失败，未获取到有效的会话信息')

        self.is_login = True
        return cookies

    def get_session(self):
        """返回当前 session"""
        return self.session

