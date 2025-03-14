# 本文件用于生成签名，构造请求参数
# 用于请求校园一卡通服务接口

from datetime import datetime
import urllib.parse
import hashlib

# 签名加密密钥（常量）
MD5_KEY_YM = 'ok15we1@oid8x5afd@'


def generate_sign(datadict, hashkey=MD5_KEY_YM):
    """
    计算请求的 Sign 值，并返回追加 Sign 后的数据字典
    :param datadict: dict, 原请求参数
    :param hashkey: str, 加密密钥（默认使用常量 MD5_KEY_YM）
    :return: str, 计算得到的 Sign 值
    """
    if not isinstance(datadict, dict):
        raise ValueError("参数 datadict 必须是字典类型")

    # 如果数据中没有时间参数 "Time"，则自动添加当前时间
    if "Time" not in datadict:
        datadict["Time"] = datetime.now().strftime("%Y%m%d%H%M%S")

    # 对参数字典进行排序
    sorted_keys = sorted(datadict.keys())

    # 按字典序拼接参数，并追加密钥
    data_str = "|".join(str(datadict[key]) for key in sorted_keys) + "|" + hashkey

    # 计算 MD5 哈希值
    sign_hash = hashlib.md5(data_str.encode("utf-8")).hexdigest()

    return sign_hash


def build_query(datadict):
    """
    构造 URL 查询字符串（包含 Sign 值）
    :param datadict: dict, 请求参数
    :return: str, 生成的查询字符串
    """
    if not isinstance(datadict, dict):
        raise ValueError("参数 datadict 必须是字典类型")

    # 计算 Sign 并追加到请求参数中
    sign_str = generate_sign(datadict)
    datadict["Sign"] = sign_str
    datadict["ContentType"] = "application/json"

    # 进行 URL 编码并拼接查询字符串
    query_string = urllib.parse.urlencode(datadict)

    return query_string


if __name__ == '__main__':
    # 示例请求参数
    data = {
        'Percode': 'test'
    }

    # 计算 Sign
    sign = generate_sign(data)

    # 生成 URL 查询字符串
    query_string = build_query(data)

    print(f"SIGN: {sign}\nQueryString: {query_string}")
