import pymysql
import pandas as pd

class DBModel:
    def __init__(self):
        self.db_diet = pymysql.connect(
            user='root',
            passwd='111111',
            host='127.0.0.1',
            db='db_diet',
            charset='utf8'
        )

        self.cursor = self.db_diet.cursor(pymysql.cursors.DictCursor)

    def selectAll(self):
        # select table
        sql = "SELECT * FROM `history`;"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        result = pd.DataFrame(result)
        print(result)

    def selectByNameDate(self, username, userdate):
        # select table
        sql = "SELECT * FROM `history` WHERE username='{}' AND userdate='{}';"\
            .format(username, userdate)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        result = pd.DataFrame(result)
        # print('date: {}, breakfast: {}, lunch: {}, dinner{}'
        #       .format(result['userdate'][0], result['breakfast'][0], result['lunch'][0], result['dinner'][0]))
        return [result['breakfast'][0], result['lunch'][0], result['dinner'][0]]

    def insert(self, username, userdate, eatTime, foodname):
        # 기존에 데이터가 있는지 확인
        sql = "SELECT * FROM `history` WHERE username='{}' AND userdate = '{}';" \
            .format(username, userdate)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if result:
            print(username + '데이터 존재함')
            # update
            sql = '''UPDATE history SET {}='{}'
             WHERE username = '{}' AND userdate = '{}';'''\
                .format(eatTime, foodname, username, userdate)
            self.cursor.execute(sql)
            self.db_diet.commit()
            print('update complete')
        else:
            print(username + '데이터 추가함')
            # insert
            sql = '''INSERT INTO `history` (username, userdate, {})
             VALUES ('{}', '{}', '{}');'''.format(eatTime, username, userdate, foodname)
            self.cursor.execute(sql)
            self.db_diet.commit()
            print('insert complete')

if __name__ == '__main__':
    print('DataBaseModel run')
    dbm = DBModel()
    
    ## select test
    # foodList = dbm.selectByNameDate('테스트', '2021-05-20')
    # print(foodList)
    
    ## insert test
    # dbm.insert('테스트4', '2021-05-20', 'dinner', '햄버거')
    