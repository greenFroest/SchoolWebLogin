import sys, os, time
import socket
import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal


class SchoolWebLogin(QtWidgets.QWidget):

    # 初始化登陆界面
    def __init__(self):
        super().__init__()
        self.lb_x = 60

        self.userip = ""
        self.userpass = ""
        self.user_data = []

        self.bt1 = QPushButton('一键登录', self)
        self.bt2 = QPushButton('更新', self)

        self.lb_user = QtWidgets.QLabel(self)
        self.lb_pass = QtWidgets.QLabel(self)

        self.line_edit_user = QLineEdit(self)
        self.line_edit_pass = QLineEdit(self)

        self.Login_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": ""
        }

        self.Post_data = {
            "action": "login",
            "ac_id": "",
            "user_ip": "",
            "nas_ip": "",
            "user_mac": "",
            "url": "",
            "drop": "0",
            "username": "",
            "password": ""
        }

        self.InitUI()
        self.Get_user_data_file()

    # 设置按钮
    def Set_Pushbutton(self):
        self.bt1.move(50, 250)
        self.bt1.setObjectName('Submit')
        self.bt1.clicked.connect(self.Auto_login)
        self.bt2.move(220, 250)
        self.bt2.setObjectName('Update')
        self.bt2.clicked.connect(self.Save_user_data)

    # 设置标签
    def Set_Labels(self):
        self.lb_user.setText("学号：")
        self.lb_user.move(self.lb_x, 100)

        self.lb_pass.setText("密码：")
        self.lb_pass.move(self.lb_x, 150)

    # 设置编辑框
    def Set_LineEdit(self):
        self.line_edit_user.move(150, 100)
        self.line_edit_pass.move(150, 150)

    # 获取用户学号和密码
    def Get_user_data_line(self):
        self.userip = self.line_edit_user.text()
        self.userpass = self.line_edit_pass.text()

        if self.userip == "":
            QMessageBox.question(self, '提示', '学号为空!',
                                 QMessageBox.Yes, QMessageBox.Yes)
            return 0
        elif self.userpass == "":
            QMessageBox.question(self, '提示', '密码为空！',
                                 QMessageBox.Yes, QMessageBox.Yes)
            return 0

        return 1

    # 保存用户学号和密码
    def Save_user_data(self):
        file_path = os.getcwd() + "/login_data.ini"

        T = os.path.exists(file_path)
        if T == 1:
            f = open(file_path, "r+")
        else:
            f = open(file_path, "w")

        flag = self.Get_user_data_line()

        if flag == 0:
            return
        else:
            f.truncate()
            f.write(self.userip + "\n")
            f.write(self.userpass)
            QMessageBox.question(self, '提示', '更新用户数据成功！',
                                 QMessageBox.Yes, QMessageBox.Yes)

    def Get_user_data_file(self):
        temp = []
        file_path = os.getcwd() + "/login_data.ini"
        T = os.path.exists(file_path)
        if T == 1:
            f = open(file_path, "r+")
            for line in f.readlines():
                temp.append(line.strip('\n'))
            if len(temp) == 2:
                self.userip = temp[0]
                self.userpass = temp[1]
                self.line_edit_user.setText(str(temp[0]))
                self.line_edit_pass.setText(str(temp[1]))
            f.close()
        else:
            return

    def Get_url(self):
        url_head_str = "http://172.18.246.34/srun_portal_pc.php?"
        host_name = socket.getfqdn(socket.gethostname())
        host_ip = socket.gethostbyname(host_name)

        self.Post_data['user_ip'] = host_ip

        url_par_str = 'ac_id=' + str("26") + \
                           '&wlanuserip=' + str(self.Post_data['user_ip']) + \
                           '&wlanacname='
        real_url = url_head_str + url_par_str

        self.Login_headers['Referer'] = real_url
        return real_url

    def Auto_login(self):
        self.Open_Wifi()
        self.Get_user_data_line()

        file_path = os.getcwd() + "/login_data.ini"
        T = os.path.exists(file_path)
        if T == 0:
            f = open(file_path, "w")

            flag = self.Get_user_data_line()

            if flag == 0:
                return
            else:
                f.truncate()
                f.write(self.userip + "\n")
                f.write(self.userpass)

        login_data = [str(self.userip), str(self.userpass)]
        url = self.Get_url()
        self.Post_data['ac_id'] = '26'
        self.Post_data['username'] = login_data[0]
        self.Post_data['password'] = login_data[1]
        requests.post(url, data=self.Post_data, headers=self.Login_headers)


    def Open_Wifi(self):
        os.system('netsh wlan connect name=HEU-WLAN')
        time.sleep(1)

    def InitUI(self):
        self.resize(400, 400)
        self.setWindowTitle("哈工程自动上网小助手")
        self.Set_Pushbutton()
        self.Set_Labels()
        self.Set_LineEdit()
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SchoolWebLogin = SchoolWebLogin()
    sys.exit(app.exec_())