
from app.utils import build_query
import xml.etree.ElementTree as ET
import json


def GetAccInfo(client):
    """
    获取一卡通信息
    :param client: SDJZUclient对象
    :return str json: 返回一个json，包含name，class, percode，idcard等信息
    """
    ssoclient = client.sso
    s = ssoclient.session

    #获取一卡通信息
    data = {
        "Percode": client.student_id,
    }
    string = build_query(data)

    res = s.post(
        url='https://etong.sdjzu.edu.cn/easytong_app/GetAccInfoByPercode',
        params=string
    )
    root = ET.fromstring(res.text)
    data_dict = {child.tag: child.text for child in root}
    data = {'name': data_dict.get('AccName'),
            'class': data_dict.get('AccDepName'),
            'percode': data_dict.get('PersonID'),
            'idcard': data_dict.get('IDNo')}
    result = json.dumps(data, ensure_ascii=False)
    return result

def GetBuildingList(client):
    """
    获取宿舍楼列表, 用于电费查询
    :param client:
    :return str: 返回一个Json，key是楼号，value是楼号对应的楼号
    """
    ssoclient = client.sso
    s = ssoclient.session
    data = {
        "AreaNo": "1",
        "ItemNum": "2",
    }

    string = build_query(data)

    res = s.post(
        url='https://etong.sdjzu.edu.cn/easytong_app/GetBuildingInfoByAreaNo',
        params=string
        )
    data = json.loads(res.text)
    buildingList = {'buildingList': []}
    for building in data['dormList']:
        buildingList['buildingList'].append({
            'name': building['name'],
            'no': building['no']
        })
    buildingList = json.dumps(buildingList, ensure_ascii=False)
    return buildingList

def GetRoomList(client, building_no):
    """
    获取宿舍列表, 用于电费查询
    :param client: SDJZUclient对象
    :param building_no: 宿舍楼序号
    :return str: 返回一个Json，key是宿舍号，value是宿舍号对应RoomNo
    """

    ssoclient = client.sso
    s = ssoclient.session

    data = {
        "AreaNo": "1",
        "BuildingNo": building_no,
        "ItemNum": "2",
    }

    string = build_query(data)

    res = s.post(
        url='https://etong.sdjzu.edu.cn/easytong_app/GetRoomInfo',
        params=string
        )
    roomList = {
        "roomList": []
    }
    for room in json.loads(res.text)['dormList']:
        roomList['roomList'].append({
            'name': room['name'],
            'no': room['no']
        })
    return json.dumps(roomList, ensure_ascii=False)

def GetRoomBalanceByRoomNo(client, building_no, room_no):

    ssoclient = client.sso
    s = ssoclient.session

    data = {
        "AreaNo": "1",
        "AccNum": "0",
        "BuildingNo": building_no,
        "FloorNo": "0",
        "RoomNo": room_no,
        "ItemNum": "2",
    }

    string = build_query(data)

    res = s.post(
        url='https://etong.sdjzu.edu.cn/easytong_app/GetPayAccInfoNew',
        params=string
        )
    data = json.loads(res.text)
    balance = data.get('balance')
    return balance

def getRoomBalanceByRoomName(client,room_name):

    ssoclient = client.sso
    s = ssoclient.session

    lighting_id = None
    ac_id = None

    dorm_name = ''.join([char for char in room_name if char.isalpha()])
    room_no = ''.join([char for char in room_name if char.isdigit()])
    data = GetBuildingList(client)
    buildingList = json.loads(data)
    for dorm in buildingList["buildingList"]:
        if dorm_name in dorm["name"]:
            if "照明" in dorm["name"] and "空调" not in dorm["name"]:
                lighting_dormid = dorm["no"]
            elif "空调" in dorm["name"] and "照明" not in dorm["name"]:
                ac_dormid = dorm["no"]
            elif "照明" in dorm["name"] and "空调" in dorm["name"]:
                lighting_dormid = dorm["no"]
                ac_dormid = dorm["no"]

    if (lighting_dormid is None) or (ac_dormid is None):
        raise ValueError("未找到对应宿舍信息"+room_name)

    data = GetRoomList(client,lighting_dormid)
    roomList = json.loads(data)
    for room in roomList["roomList"]:
        if room_no in room["name"]:
            lighting_id = room["no"]
    data = GetRoomList(client,ac_dormid)
    roomList = json.loads(data)
    for room in roomList["roomList"]:
        if room_no in room["name"]:
            ac_id = room["no"]

    balance_light = GetRoomBalanceByRoomNo(client,lighting_dormid,lighting_id)
    balance_ac = GetRoomBalanceByRoomNo(client,ac_dormid,ac_id)
    return balance_light, balance_ac




