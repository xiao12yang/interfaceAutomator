# -*- coding:utf-8 -*-
import logging
import os
import time
from config.setting import FILE_PATH
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份
import colorlog

logs_path = FILE_PATH['log']

# 日志格式
if not os.path.exists(logs_path):
    os.mkdir(logs_path)

log_file_name = logs_path + r'\test_{}.log'.format(time.strftime('%Y%m%d'))
log_err_file_name = logs_path + r'\test_{}_err.log'.format(time.strftime('%Y%m%d'))


class HandleLogs:
    @classmethod
    def setting_log_color(cls):
        log_color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s - %(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s',
            log_colors=log_color_config)
        return formatter

    @classmethod
    def output_logs(cls):
        logger = logging.getLogger(__name__)
        steam_formatter = cls.setting_log_color()

        # 防止重复打印日志
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s')
            # 把日志输出到控制台
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(steam_formatter)
            logger.addHandler(sh)

            # 把日志输出到文件中
            fh = RotatingFileHandler(log_file_name,
                                     mode='a',
                                     maxBytes=5242880,
                                     backupCount=7,
                                     encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(log_format)
            logger.addHandler(fh)
            # 错误日志文件
            fh_err = RotatingFileHandler(log_err_file_name,
                                         mode='a',
                                         maxBytes=5242880,
                                         backupCount=7,
                                         encoding='utf-8')
            fh_err.setLevel(logging.ERROR)
            fh_err.setFormatter(log_format)
            logger.addHandler(fh_err)

        return logger


handle = HandleLogs()
logs = handle.output_logs()
if __name__ == "__main__":
    logs.info('hello world')
    logs.debug('hello world')
    logs.warning('hello world')
    logs.error('hello world')
    logs.critical('hello world')
