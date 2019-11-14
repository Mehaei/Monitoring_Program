# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2019-11-13 10:21:20
# @Last Modified by:   Mehaei
# @Last Modified time: 2019-11-13 18:53:54

import os
import sys
import time
import psutil
import logging
import logging.handlers
from threading import Thread
from multiprocessing import Process, Event
from PyQt5.QtCore import QCoreApplication, QProcess
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QApplication,
                            QMessageBox, QPushButton, QLabel, QLineEdit, QGridLayout, QRadioButton)

MONITOR_PROCESS = "qq"
FIND_RESULT = "kill"
CONFIG_FILTER = ".config"
LOG_DIR = ".log"
CONFIG_DONE = Event()

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s',
    handlers=[logging.handlers.RotatingFileHandler("%s/%s" % (LOG_DIR, "run_debug.log"), maxBytes=1024 * 1024 * 10, backupCount=5, encoding="utf-8")]
)


def read_config(config_file=CONFIG_FILTER):
    config_process = ""
    config_result = ""
    if os.path.exists(config_file):
        with open(".config", "r") as f:
            config = f.readlines()
            for conf in config:
                if conf.startswith("MONITOR_PROCESS"):
                    config_process = conf.split("=")[-1].strip().strip("'")
                elif conf.startswith("FIND_RESULT"):
                    config_result = conf.split("=")[-1].strip().strip("'")
                else:
                    continue
    else:
        config_process, config_result = MONITOR_PROCESS, FIND_RESULT
    return config_process, config_result


class ConfigUI(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initUI()
        self._read_config()

    def _initUI(self):

        self.resize(600, 300)
        self.center()
        self.cwd = os.getcwd()

        process_name = QLabel('Process Name : ')

        self.process_name_edit = QLineEdit()
        self.process_name_edit.setPlaceholderText("Please Monitoring Process Name e.g.: cs,qq, defalut: %s" % MONITOR_PROCESS)

        find_result = QLabel('Find Result : ')

        self.result_shut = QRadioButton('shutdown')
        #默认选中result_shut
        self.result_shut.setChecked(True)

        self.result_kill = QRadioButton('kill')
        self.result_restart = QRadioButton('restart')

        self.default_config = QPushButton('Default', self)
        self.default_config.clicked.connect(self.restore_default_config)

        self.confirm = QPushButton('Confirm', self)
        self.confirm.clicked.connect(self.confirm_start_monitor)

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(process_name, 1, 0)
        grid.addWidget(self.process_name_edit, 1, 1, 1, 4)

        grid.addWidget(find_result, 2, 0)
        grid.addWidget(self.result_shut, 2, 1)
        grid.addWidget(self.result_kill, 2, 2)
        grid.addWidget(self.result_restart, 2, 4)

        grid.addWidget(self.default_config, 4, 3)
        grid.addWidget(self.confirm, 4, 4)

        self.setLayout(grid) 

        self.setWindowTitle('Process Monitoring')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _read_config(self):
        if os.path.exists(CONFIG_FILTER):
            config_process, config_result = read_config()
            self.process_name_edit.setText(config_process)
            self.set_btn_checked(text=config_result)
        else:
            pass
        logging.debug("read config success")

    def _write_config(self):
        with open(".config", "w") as f:
            f.write("MONITOR_PROCESS = '%s'\n" % self.process_name_edit.text())
            f.write("FIND_RESULT = '%s'" % self.result)
        logging.debug("save config success")
        CONFIG_DONE.set()

    def restore_default_config(self):
        self.process_name_edit.setText(MONITOR_PROCESS)
        self.set_btn_checked(text=FIND_RESULT)
        QMessageBox.information(self, "Success Message", "Default Restored Success")

    def warning(self, title, content):
        QMessageBox.warning(self, title, content)

    def set_btn_checked(self, button=None, text="shutdown"):
        btn_list = [self.result_shut, self.result_kill, self.result_restart]
        if button:
            button.setChecked(True)
        else:
            for btn in btn_list:
                if btn.text() == text:
                    btn.setChecked(True)

    def confirm_start_monitor(self):
        btn_list = [self.result_shut, self.result_kill, self.result_restart]
        self.result = ""
        for btn in btn_list:
            if btn.isChecked():
                self.result = btn.text()

        if all((self.process_name_edit.text(), self.result)):
            reply = QMessageBox.question(self, 'Confirm Config',
                                 "Monitor Process: %s\nFind Use Result: %s\nAre you sure use this config?" % (self.process_name_edit.text(), self.result), QMessageBox.Yes |
                                 QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self._write_config()
                # self.start()
                self.close()
            else:
                pass
        else:
            self.warning("Warning", "Please Input Monitor Process or Choose Find Use Result")

    # def closeEvent(self, event):

    #     reply = QMessageBox.question(self, 'Message',
    #                                  "Are you sure to quit?", QMessageBox.Yes |
    #                                  QMessageBox.No, QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def start(self): 
        m = MonitorProcess()
        m.start()


def kill_crawl_process() -> None:
    """
    find all process, and kill crawl process
    """
    pid = psutil.pids() 
    error_msg = ""
    for k,i in enumerate(pid): 
        try: 
            proc  = psutil.Process(i) 
            # logging.debug k,i,"%.2f%%"%(proc.memory_percent()),"%",proc.name(),proc.exe() 
            cmdline = proc.cmdline()
            logging.debug(cmdline)
            # if " ".join(cmdline) in _KILL_PROCESS_COMMAND:
            #     cmdline.terminate()

            # if all((len(cmdline) == 2, cmdline[0] == "python3", cmdline[-1].split("/")[-1] in _CRAWL_SPIDER_FILE)):
            #     cmdline.terminate()

        except Exception as e:
            error_msg = e

        finally:
            # send email
            pass


class MonitorProcess(Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_process, self.config_result = read_config()

    def run(self):
        while 1:
            logging.debug("%s, %s" % (self.config_process, self.config_result))
            time.sleep(2)


class ConfigUIpProcess(Process):
    def run(self):
        app = QApplication(sys.argv)
        ex = ConfigUI()
        sys.exit(app.exec_())


def main():
    c = ConfigUIpProcess()
    c.start()
    c.join()
    if CONFIG_DONE.is_set():
        m = MonitorProcess()
        m.start()
        m.join()


def test():
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")


if __name__ == '__main__':
    main()




