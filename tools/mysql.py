import pymysql


class MysqlConnect():
    # Connect to the database
    conn = pymysql.connect(
        host="X.X.X.X",
        user="666",
        password="XXX",
        database="login"
    )
    # Create a cursor object
    cursor = conn.cursor()
    def selectAll(self,tableName):
        # Execute a SQL query
        self.cursor.execute("SELECT * FROM " + tableName)
        # Fetch the results of the query
        results =self.cursor.fetchall()
        return results
        # # Loop through the results and print each row
        # for row in results:
        #     print(row)
    def selectOneByOne(self,tableName,key,keyValue):
        sql = 'SELECT * FROM '+tableName+" where " + key +"=\'" + keyValue + "\'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    # INSERT INTO user(user_num,user_password) VALUES("asdas","66654")
    # INSERT INTO user(user_num,user_password) VALUES('111','4534')
    def insertUser(self,userNum,userPassword):
        sql = 'INSERT INTO user(user_num,user_password) VALUES('+"\'" +userNum +"\',"+ "\'"+userPassword+"\')"
        print(sql)
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            return True
        else:
            return False
        self.conn.commit()

    def closeCon(self):
        # Close the cursor and connection
        self.cursor.close()
        self.conn.close()



