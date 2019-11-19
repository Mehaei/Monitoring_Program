# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2019-11-19 12:21:39
# @Last Modified by:   Mehaei
# @Last Modified time: 2019-11-19 12:36:23

import os
import sys
import time
import psutil
import logging
import logging.handlers

MONITOR_PROCESS = "qq"
FIND_RESULT = "kill"
CHECK_TIME_INTERVAL = 60
CONFIG_FILTER = "config"
LOG_DIR = "log"
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
    config_interval = 0
    if os.path.exists(config_file):
        with open(".config", "r") as f:
            config = f.readlines()
            for conf in config:
                if conf.startswith("MONITOR_PROCESS"):
                    config_process = conf.split("=")[-1].strip().strip("'")
                elif conf.startswith("FIND_RESULT"):
                    config_result = conf.split("=")[-1].strip().strip("'")
                elif conf.startswith("CHECK_TIME_INTERVAL"):
                    config_interval = int(conf.split("=")[-1].strip().strip("'"))
                else:
                    continue
    else:
        config_process, config_result, config_interval = MONITOR_PROCESS, FIND_RESULT, CHECK_TIME_INTERVAL
    return config_process, config_result, config_interval


def write_config(process_name, result, interval):
    with open(CONFIG_FILTER, "w") as f:
        f.write("MONITOR_PROCESS = '%s'\n" % process_name)
        f.write("FIND_RESULT = '%s'" % result)
        f.write("CHECK_TIME_INTERVAL = '%s'" % interval)
    logging.debug("save config success")


def kill_crawl_process(config_process_list, config_result) -> None:
    """
    find all process, and kill crawl process
    """
    pid = psutil.pids() 
    error_msg = ""
    for k,i in enumerate(pid): 
        try: 
            proc  = psutil.Process(i) 
            cmdline = proc.cmdline()

            logging.debug(cmdline)

            if " ".join(cmdline) in config_process_list:
                if config_result == "kill":
                    # kill process
                    cmdline.terminate()
                elif config_result == "restart":
                    # restart win
                    pass
                else:
                    # shutdown win
                    pass

        except Exception as e:
            error_msg = e

        finally:
            # send email
            pass


def main():
    config_process, config_result, config_interval = read_config()
    config_process_list = config_process.split(",")

    while True:
        kill_crawl_process(config_process_list, config_result)
        logging.debug("sleep: %s" % config_interval)
        time.sleep(config_interval)


if __name__ == "__main__":
    main()
