# coding=utf-8
import pymysql
from pathlib import Path
import environ
import os

env = environ.Env()
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
env_name = env.str('PROJECT_ENV', 'local')
# reading .env file
env_file = 'env/.%s.env' % env_name
env.read_env(os.path.join(ROOT_DIR, env_file))


def init_db():
    user = env('MYSQL_USER', default='user')
    passwd = env('MYSQL_PASSWORD', default='passwd')
    host = env('MYSQL_HOST', default='host')
    port = env.int('MYSQL_PORT', default='port')
    db = env('MYSQL_DB', default='db')
    conn = pymysql.connect(user=user, passwd=passwd, host=host, port=port)
    cursor = conn.cursor()
    try:
        cursor.execute("create database if not exists %s default charset utf8mb4 collate utf8mb4_unicode_ci;" % (db))
        # 提交执行
        conn.commit()
    except Exception:
        pass
    finally:
        # 不论try中的代码是否抛出异常，这里都会执行
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()


if __name__ == "__main__":
    init_db()
