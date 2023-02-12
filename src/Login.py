import sys
import tools.mysql as MySQLConnect
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.login import *
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QMouseEvent, QCursor


class LoginWindows(QMainWindow, Ui_MainWindow):
    mc = MySQLConnect.MysqlConnect()
    def __init__(self, parent=None):
        super(LoginWindows, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 按钮
        self.close_pushButton.clicked.connect(self.close)
        self.hidden_pushButton.clicked.connect(self.showMinimized)
        self.login_pushButton.clicked.connect(self.onLoginButtonClick)
        self.signUp_pushButton.clicked.connect(self.onSignUpButtonClick)

    # 窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 提示框
    def showMsgBox(self, msg):
        TipBox = QMessageBox(self.widget)
        TipBox.setText(msg)
        TipBox.setWindowFlags(
            TipBox.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowStaysOnTopHint)
        # TipBox.setStandardButtons(QMessageBox.NoButton)
        TipBox.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        TipBox.show()
        # 创建动画
        animation = QPropertyAnimation(TipBox, b"windowOpacity", self)
        animation.setStartValue(0.5)
        animation.setEndValue(1)
        animation.setDuration(500)

        # 启动动画
        animation.start()

        QTimer.singleShot(800, TipBox.close)
        pass

    # 登录按钮逻辑
    def onLoginButtonClick(self):
        userNum = self.user_lineEdit.text()
        userPassword=self.password_lineEdit.text()
        if (userNum!='') & (userPassword!=''):
           res = self.mc.selectOneByOne('user','user_num',userNum)
           if len(res) > 0:
               if res[0][2] == userPassword:
                   self.showMsgBox("登录成功")
                   # 后续操作...

               else:
                   self.showMsgBox("账号或密码错误")
           else:
               self.showMsgBox("无此账号")
        else:
            self.showMsgBox("请输入信息")
        pass

    # 注册按钮逻辑
    def onSignUpButtonClick(self):
        userNum = self.user_lineEdit.text()
        userPassword = self.password_lineEdit.text()
        if (userNum != '') & (userPassword != ''):
            try:
                res = self.mc.insertUser(userNum,userPassword)
                if res:
                    self.showMsgBox("注册成功")
                else:
                    self.showMsgBox("注册失败!错误!")
            except Exception as e:
                if e.args[0] == 1062:
                    self.showMsgBox("注册失败,账号已存在")
                print("insertSQL:",e)
        else:
            self.showMsgBox("请输入信息")
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywin = LoginWindows()
    mywin.show()
    sys.exit(app.exec_())
