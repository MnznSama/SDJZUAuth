import json


def GetRoomInfo(client):
    """
    获取宿舍信息
    :param client: SDJZUClient对象
    :return str:  一个json，包含roomName，userName，PhotoUrl，roommatesInfos等信息，其中roommatesInfos是一个列表，包含每个室友的userName，userId，phone，photo等信息
    """
    ssoclient = client.sso
    s = ssoclient.session


    res = s.post(url='https://static.sdjzu.edu.cn/dormTaskAPI/basic/myRoomPageAtHomeInfo',allow_redirects=False)
    data = res.json().get('data')
    roomInfo = data.get('roomInfo')
    userInfo = data.get('userInfo')
    res = s.post(url='https://static.sdjzu.edu.cn/dormTaskAPI/basic/getRoommatesInfo')
    output_data = {
        'roomName': roomInfo.get('roomName'),
        'userInfo': {
            'userName': userInfo.get('userName'),
            'photoUrl': f"https://safecampus.sdjzu.edu.cn/photo/view/{userInfo.get('idPhotoUrl')}"
        },
        'roommates': []
    }
    for roommate in res.json().get('data').get('roommatesInfos'):
        output_data['roommates'].append({
            'userName': roommate.get('userName'),
            'userId': roommate.get('userId'),
            'phone': roommate.get('phone'),
            'photo': f"https://safecampus.sdjzu.edu.cn/photo/view/{roommate.get('idPhotoUrl')}"
        })
    return json.dumps(output_data, ensure_ascii=False)