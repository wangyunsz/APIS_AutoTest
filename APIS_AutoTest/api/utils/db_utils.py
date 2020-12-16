# create by: wangyun
# create at: 2020/4/16 20:28
import pymysql

from api.utils.read_yaml import ReadYaml


class DBUtils:

    def __init__(self):
        """
        数据库基类
        """
        self.host = ReadYaml().get_value('database.host')
        self.port = ReadYaml().get_value('database.port')
        self.user = ReadYaml().get_value('database.user')
        self.password = ReadYaml().get_value('database.password')
        self.db_name = ReadYaml().get_value('database.name')
        self.charset = ReadYaml().get_value('database.charset')

        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                    database=self.db_name, charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    # 查询
    def search(self, sql, param):
        cur = self.cursor
        try:
            cur.execute(sql, param)
            result = cur.fetchall()
            return result
        except Exception as e:
            print('执行sql出错。')
            raise e
        finally:
            self.close()

    # 新增
    def add(self, sql, param):
        cur = self.cursor
        try:
            cur.execute(sql, param)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('执行sql出错，回滚。')
            raise e
        finally:
            self.close()

    # 修改
    def update(self, sql, param):
        cur = self.cursor
        try:
            cur.execute(sql, param)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('执行sql出错，回滚。')
            raise e
        finally:
            self.close()

    # 删除
    def delete(self, sql, param):
        cur = self.cursor
        try:
            cur.execute(sql, param)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('执行sql出错，回滚。')
            raise e
        finally:
            self.close()
