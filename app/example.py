import json

from client import SDJZUClient
import utils

def loginQZ(sso=True):
    client = SDJZUClient(studentid, password)
    if sso:
        client.login_qiangzhi()
        return client
    verifycode_data = client.get_verifycode()
    with open('verifycode.png', 'wb') as f:
        f.write(verifycode_data)

    from PIL import Image
    image = Image.open("verifycode.png")
    image.show()
    verifycode_value = input('请输入验证码: ')

    client.login_qiangzhi(sso=False, v_code=verifycode_value)

    return client

def loginEtong():
    client = SDJZUClient(studentid, password)
    client.login_etong()
    return client

def loginPortal():
    client = SDJZUClient(studentid, password)
    client.login_portal()
    return client

def loginH5():
    client = SDJZUClient(studentid, password)
    client.login_h5()
    return client

def getEtongInfo(client=None):
    if client is None:
        print("❌ 未登录, 自动登录")
        client=loginEtong()
    return utils.etong.GetAccInfo(client)

def getRoomInof(client=None):
    if client is None:
        print("❌ 未登录, 自动登录")
        client=loginH5()
    return utils.h5.GetRoomInfo(client)

def getPhoneNum(client=None):
    if client is None:
        print("❌ 未登录, 自动登录")
        client=loginPortal()
    return utils.portal.GetPhone(client)

def getBuildingList(client=None):
    if client is None:
        print("❌ 未登录, 自动登录")
        client=loginEtong()
    return utils.etong.GetBuildingList(client)

def getRoomList(client, building_no):
    if client is None:
        print("❌ 未登录, 自动登录")
        client=loginEtong()
    return utils.etong.GetRoomList(client, building_no)

def getRoomBalanceByRoomNo(client, building_no, room_no):
    if client is None:
        print("❌ 未登录, 自动登录")
        client=loginEtong()
    return utils.etong.GetRoomBalanceByRoomNo(client, building_no, room_no)

def getRoomBalanceByRoomName(client, room_name):
    if client is None:
        print("❌ 未登录, 自动登录")
        client=loginEtong()
    return utils.etong.getRoomBalanceByRoomName(client, room_name)

def getRoomBalanceByAccount(client=None):
    roomInfo = json.loads(getRoomInof(client))
    room_name = roomInfo.get('roomName')
    balance_light, balance_ac = getRoomBalanceByRoomName(client, room_name)
    return balance_light, balance_ac

def getClassSchedule(client=None, sso=True):
    if client is None:
        print("❌ 未登录, 自动使用"+ ("SSO" if sso else "强智")  + "强智登录")
        client = loginQZ(sso)
    session = client.sso.session if sso else client.qz.session
    return utils.jw.get_classSchedule(session)


if __name__ == '__main__':

    studentid = ''
    password = ''
    first_week_date = "2025-02-24"

    try:
        print("🔑 登录强智教务系统中...")
        client = loginQZ()
        print("  ✅ 登录成功")

        print("  🔍 获取课表中...")
        schedule = getClassSchedule(client)
        print("  ✅ 获取课表成功")
        print(schedule)

        print("🔑 登录H5平台中...")
        client = loginH5()
        print("  ✅ 登录成功")

        print("  🔍 获取宿舍信息中...")
        roomInfo = getRoomInof(client)
        print("  ✅ 获取宿舍信息成功")
        print(roomInfo)

        print("🔑 登录Portal服务中...")
        client = loginPortal()
        print("  ✅ 登录成功")

        print("  🔍 获取手机号中...")
        phone = getPhoneNum(client)
        print("  ✅ 获取手机号成功")
        print(phone)

        print("🔑 登录一卡通服务中...")
        client = loginEtong()
        print("  ✅ 登录成功")

        print("  🔍 获取个人信息中...")
        info = getEtongInfo(client)
        print("  ✅ 获取个人信息成功")
        print(info)


        print("  🔍 获取宿舍余额中...")
        balance = getRoomBalanceByAccount(client)
        print("  ✅ 获取宿舍余额成功")
        print(balance)



    except Exception as e:
        print("❌ 登录失败:", e)