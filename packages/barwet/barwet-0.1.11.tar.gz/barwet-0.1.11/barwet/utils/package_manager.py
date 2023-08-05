import os

def install_package(package_name):
    package_name = package_name.replace("_", "-")  # 下载pip fake_useragent 包时  包名是:fake-useragent
    p = os.popen("pip list --format=columns")  # 获取所有包名 直接用 pip list 也可获取
    pip_list = p.read()  # 读取所有内容
    if package_name in pip_list:
        print("已经安装{}".format(package_name))
        return True
    else:
        print("没有安装{}!即将自动安装,请稍后".format(package_name))
        p = os.popen("pip install {}".format(package_name))
        if "Success" in p.read():
            print("安装{}成功!".format(package_name))
            return True if "Success" in p.read() else False