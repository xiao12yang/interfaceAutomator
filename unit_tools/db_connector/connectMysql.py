from fileinput import close

import pymysql
import pymysql.cursors
from unit_tools.handle_data.configParse import ConfigParser
from unit_tools.log_util.recordlog import logs

config = ConfigParser()


class ConnectMysql:
    """
    连接MySQL数据库，进行增删改查
    """

    def __init__(self):
        self.conf = {
            'host': config.get_mysql_conf('host'),
            'port': int(config.get_mysql_conf('port')),
            'user': config.get_mysql_conf('user'),
            'password': config.get_mysql_conf('password'),
            'database': config.get_mysql_conf('database'),
        }

        try:
            self.conn = pymysql.connect(**self.conf)
            # 获取操作游标
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info(f'成功连接到数据库ip：{self.conf.get("host")}')
        except Exception as e:
            logs.error(f'连接数据库失败，原因：{e}')

    def query(self, sql, fetchall=False):
        """
        查询数据库数据
        :param sql: 查询的SQL语句
        :param fetchall: 查询全部数据，默认为False查询单挑数据
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            if fetchall:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchone()
        except Exception as e:
            logs.error(f'查询数据库内容出现异常，原因：{e}')
        finally:
            close()
    def delete(self, sql):
        """
        删除数据库内容
        :param sql: 删除的sql语句
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logs.info(f'数据库数据删除成功')
        except Exception as e:
            logs.error(f'删除数据库数据出现异常，原因：{e}')
        finally:
            close()
    def close(self):
        """
        断开数据库连接
        :return:
        """
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        return True

if __name__ == '__main__':
    con = ConnectMysql()
    print(con)
    sql = "select * from ecs_users"
    res = con.query(sql)
    print(res)
