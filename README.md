# -
华东交通大学校园网自动连接脚本，用于pc开机自动连接校园网/  ECJTU(East China Jiaotong University) campus network auto-connect script, used for automatically connecting to the campus network when the PC starts
必需准备
1、安装 Python（≥3.8）

2、安装 requests 库
   若缺失库，打开命令提示符，
   执行：  pip install requests

3、修改config中的账号、运营商与密码

4、启动设置
   win+r打开“运行”窗口，输入shell:startup打开windows启动文件夹，新建auto_login.pyw的快捷方式，使其开机时能自启动

5、日志
   脚本每次运行会自动记录日志，日志在auto_login.pyw的相同目录下
