# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2019-11-12 17:49:29
# @Last Modified by:   Mehaei
# @Last Modified time: 2019-11-13 14:34:30
from PyQt5.QtWidgets import QLabel, QWidget, QRadioButton, QApplication, QPushButton, QMessageBox, QButtonGroup, QGridLayout
import sys
import psutil


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(300, 200)
        # self.center()
        process_name = QLabel('Process Name')

        self.btn1=QRadioButton('Button1')
        #默认选中btn1
        self.btn1.setChecked(True)
        #toggled信号与槽函数绑定
        self.btn1.toggled.connect(lambda :self.btnstate(self.btn1))
        # layout.addWidget(self.btn1)

        self.btn2 = QRadioButton('Button2')
        self.btn2.toggled.connect(lambda: self.btnstate(self.btn2))
        # layout.addWidget(self.btn2)
        grid = QGridLayout()

        grid.setSpacing(5)

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(process_name, 1, 0)
        grid.addWidget(self.btn1, 1, 2)
        grid.addWidget(self.btn2, 1, 3)

        self.setLayout(grid) 

        self.setWindowTitle('Process Monitoring')
        self.show()

    def btnstate(self,btn):
    #输出按钮1与按钮2的状态，选中还是没选中
        if btn.text()=='Button1':
            if btn.isChecked()==True:
                print(btn.text()+"is selected")
            else:
                print(btn.text()+"is deselected")

        if btn.text()=="Button2":
            if btn.isChecked() == True:
                print(btn.text() + "is selected")
            else:
                print(btn.text() + "is deselected")

    def rbclicked(self):
        if self.bg1.checkedId() == 11:
            self.info1 = '你是'
        elif self.bg1.checkedId() == 12:
            self.info1 = '我是'
        elif self.bg1.checkedId() == 13:
            self.info1 = '他是'            
        else:
            self.info1 = ''
        QMessageBox.information(self,'What?',self.info1)


def kill_crawl_process() -> None:
    """
    find all process, and kill crawl process
    """
    pid = psutil.pids() 
    error_msg = ""
    for k,i in enumerate(pid): 
        try: 
            proc  = psutil.Process(i) 
            # print k,i,"%.2f%%"%(proc.memory_percent()),"%",proc.name(),proc.exe() 
            cmdline = proc.cmdline()
            print(cmdline)
            # if " ".join(cmdline) in _KILL_PROCESS_COMMAND:
            #     cmdline.terminate()

            # if all((len(cmdline) == 2, cmdline[0] == "python3", cmdline[-1].split("/")[-1] in _CRAWL_SPIDER_FILE)):
            #     cmdline.terminate()

        except Exception as e:
            error_msg = e

        finally:
            # send email
            pass


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # ex = Example()
    # sys.exit(app.exec_())
    kill_crawl_process()
