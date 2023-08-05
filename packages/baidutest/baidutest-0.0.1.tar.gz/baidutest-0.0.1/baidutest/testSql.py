import pymysql

#操作数据库
'''
    1.连接数据库，通过connect函数连接，生成connection对象
    2.定义游标cursor，再通过我们游标执行脚本并获取结果
    3.关闭连接
'''
db = pymysql.connect(host="localhost",user="root",password="88888888",database="world")
'''
    常用方法：
    1.cursor():使用当前连接创建并返回游标
    2.commit():提交当前事务,如果对数据库中的数据做了修改，必须要做提交的动作
    3.rollback():回滚当前事务
    4.close():关闭当前连接
'''
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
'''
    游标操作方法：
    1.execute():执行数据库查询或命令，将结果从数据库返回给客户端
    2.fetchone():获取结果集的下一行
    3.fetchall():获取结果集的所有行
    4.fetchmany():获取结果集的几行
'''
# 执行脚本
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT * from city")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print(data)

# 关闭数据库连接
db.close()