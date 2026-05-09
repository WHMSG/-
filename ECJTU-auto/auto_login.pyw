import requests
import re
import socket
import datetime
import time
import os

# 获取脚本所在目录的绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 拼接日志文件完整路径
LOG_FILE = os.path.join(SCRIPT_DIR, "login_log.txt")


def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {msg}\n")

def get_local_ip():
    """获取本机内网IP（通过连接外部地址获取）"""
    try:
        # 创建一个socket连接，获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        log(f"获取本机IP失败: {e}")
        return None

def get_auth_params():
    """尝试访问外部网站，从重定向中获取认证参数"""
    try:
        # 访问一个外部网站，触发重定向到认证页面
        # 注意：校园网通常会把所有HTTP请求重定向到认证页面
        r = requests.get("http://www.baidu.com", allow_redirects=False, timeout=5)
        if r.status_code == 302 and "Location" in r.headers:
            location = r.headers["Location"]
            log(f"重定向地址: {location}")
            # 从URL中提取参数
            # 例如：http://172.16.2.100:801/eportal/?c=ACSetting&a=Login&wlanuserip=10.16.45.161&...
            match = re.search(r"http://([^/]+)(/eportal/\?.*)", location)
            if match:
                base_url = f"http://{match.group(1)}:801{match.group(2)}"
                # 去除可能的锚点
                base_url = base_url.split('#')[0]
                return base_url
        log("未从重定向获取到参数")
        return None
    except Exception as e:
        log(f"获取认证参数异常: {e}")
        return None

def login():
    log("=== 脚本启动 ===")

    # 第一步：尝试从重定向获取完整的登录URL
    login_url = get_auth_params()
    if not login_url:
        log("无法获取动态参数，尝试使用本地IP构造URL")
        local_ip = get_local_ip()
        if not local_ip:
            log("无法获取本地IP，登录失败")
            return
        # 使用固定模板构造URL（假设其他参数固定）
        login_url = f"http://172.16.2.100:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.16.2.100&iTermType=1&wlanuserip={local_ip}&wlanacip=null&wlanacname=null&mac=00-00-00-00-00&ip={local_ip}&enAdvert=0&queryACIP=0&loginMethod=1"
        log(f"构造的URL: {login_url}")

    from config import ACCOUNT,PASSWORD

    # 第二步：提交登录表单
    form_data = {
        
        "DDDDD": ",0,"+ACCOUNT,     # 请替换为你的学号（保留运营商后缀）
                                                 #@cmcc中国移动  @telecom中国电信  @unicom中国联通

        "upass": PASSWORD,                     # 请替换为你的密码
        "R1": "0",
        "R2": "0",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "OMKKey": "123456",
        "buttonClicked": ""
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "http://172.16.2.100:801/",
    }

    try:
        log(f"尝试登录，URL: {login_url}")
        # 注意：有些认证系统需要先GET一下登录页面获取Cookie，但之前成功时没要，先不加
        response = requests.post(login_url, data=form_data, headers=headers, timeout=5, allow_redirects=False)
        log(f"状态码: {response.status_code}")
        if response.status_code == 302:
            log("✅ 登录成功（收到302）")
            # 可选的后续验证
            time.sleep(2)
            # 尝试访问百度验证
            try:
                test = requests.get("http://www.baidu.com", timeout=3)
                if test.status_code == 200:
                    log("✅ 网络已连通")
            except:
                log("⚠️ 网络可能尚未连通")
        else:
            log(f"❌ 登录失败，响应前200字符: {response.text[:200]}")
    except Exception as e:
        log(f"请求异常: {e}")

    log("=== 脚本结束 ===")

if __name__ == "__main__":
    login()