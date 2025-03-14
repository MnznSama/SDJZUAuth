# SDJZUAuth

📜
本项目基于 GNU General Public License v3.0 (GPLv3) 开源。

⚠️
本 SDK 仅供学习和研究使用，不得用于任何违反学校规定或国家法律的行为。开发者对使用本 SDK 产生的任何后果不承担责任。请确保您的使用符合相关法律法规。
## 📌 介绍
`SDJZUAuth` 是一个 Python SDK，旨在提供对 **山东建筑大学** 各大系统的认证和数据交互功能，包括但不限于：
- **H5 页面**
- **Portal 门户**
- **教务系统（强智）**
- **校园一卡通（e通）**

本 SDK 旨在简化开发者访问学校各系统的流程，提供统一的身份认证接口，便于各开发者使用。
SDK所使用账号密码为**智慧建大**app账号信息，不会被记录或上传至服务器，仅用于登录学校系统。

## 🚀 功能
- **SSO 统一认证**
- **强智教务系统登录（SSO/账号密码）**
- **一卡通系统登录**
- **课表查询**
- **个人信息/舍友信息查询**
- **宿舍电费余额查询**

---
## 🔧 使用示例
### SSO 登录强智教务系统
```python
from app.client import SDJZUClient

client = SDJZUClient(username="学号", password="密码")
client.login_qiangzhi() #参数可选，默认使用SSO账号信息登录
print("登录成功，Cookies:", client.sso.session.cookies.get_dict())
```
### 查询宿舍信息
```python
import app.utils as utils
from app.client import SDJZUClient
client = SDJZUClient(username="学号", password="密码")
client.login_etong()
print(utils.etong.GetAccInfo(client))
```
---

# 📂 项目结构
```
sdjzu-sdk/ # 项目根目录 
│── auth/ # 认证模块 
│ │── __init__.py # 模块初始化 
│ │── sso.py # SSO 统一认证 
│ │── qiangzhi.py # 强智教务系统认证 
│── utils/ # 工具类 
│ │── __init__.py # 模块初始化 
│ │── etong.py # 有关校园一卡通的工具类
│ │── jw.py # 有关强智教务系统的工具类
│ │── h5.py # 有关H5平台的工具类
| |—— portal.py # 有关门户系统的工具类
| |—— SignGEN.py # 校园一卡通签名生成
│── client.py # SDK 客户端
│── example.py #调用示例
```


## 📜 目录说明
- **`auth/`** - 认证模块，包含山东建筑大学 SSO 认证和强智教务系统登录实现。
- **`utils/`** - 存放各种辅助函数，例如签名处理等。
- **`examples.py`** - 示例代码，方便用户快速上手。

## 📌 说明
- 所有 API 入口都在 `auth/` 目录下，可直接调用 `SSOAuth` 或 `QZClient` 进行身份验证，当然，推荐使用client进行统一调用。
- `examples.py` 提供使用示例，方便开发者参考。
