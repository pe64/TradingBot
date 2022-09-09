import sqlite3
import json
import time

class SqliteObj:

    def __init__(self, db_path) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        pass

    def get_stock_self_selection(self):
        self.cur.execute("SELECT scode, market FROM self_select")
        rows = self.cur.fetchall()
        return rows

    def get_fund_self_selections(self):
        self.cur.execute("SELECT fcode FROM self_select")
        rows = self.cur.fetchall()
        return rows

    def get_fund_last_history_charge_date(self, fcode):
        try:
            cmd ="SELECT fsrq FROM f%s ORDER BY id DESC LIMIT 1"%fcode 
            self.cur.execute(cmd)
            rows = self.cur.fetchall()
            return rows[0][0]
        except:
            return None

    def get_stock_last_history_charge_date(self, scode):
        try:
            cmd ="SELECT fsrq FROM s%s ORDER BY id DESC LIMIT 1"%scode 
            self.cur.execute(cmd)
            rows = self.cur.fetchall()
            return rows[0][0]
        except:
            return None

    def get_stock_history_charge_by_date(self, scode, date):
        try:
            cmd = 'SELECT end_charge FROM s%s WHERE fsrq == "%s"'%(scode, date) 
            self.cur.execute(cmd)
            rows = self.cur.fetchall()
            return rows[0][0]
        except:
            return None

    def get_fund_history_charge_by_date(self, scode, date):
        try:
            cmd = 'SELECT dwjz, jzzzl FROM f%s WHERE fsrq == "%s"'%(scode, date) 
            self.cur.execute(cmd)
            rows = self.cur.fetchall()
            return rows[0][0], rows[0][1]
        except:
            return None, None




    def get_stock_last_history_charge_list(self, scode, start_date, end_date):
        self.cur.execute("SELECT fsrq, end_charge FROM s%s"%scode)
        rows = self.cur.fetchall()
        charge_list = []
        start_ts = time.strptime(start_date, "%Y-%m-%d") 
        end_ts = time.strptime(end_date, "%Y-%m-%d")
        for row in rows:
            ts = time.strptime(row[0], "%Y-%m-%d")
            if start_ts < ts and ts < end_ts :
                charge_list.append(row[1])

        return charge_list


    def create_fund_history_table(self, fcode):
        try:
            self.cur.execute("CREATE TABLE f%s (id INTEGER PRIMARY KEY, fsrq DATE NOT NULL, dwjz FLOAT NOT NULL, jzzzl FLOAT);"%fcode)
        except:
            pass
        pass
    
    def create_stock_history_table(self, scode):
        try:
            cmd = "CREATE TABLE s%s (id INTEGER PRIMARY KEY, fsrq DATE NOT NULL, start_charge FLOAT , end_charge FLOAT, max_charge FLOAT, min_charge FLOAT, cjl INTEGER, cjr FLOAT, zhen_f FLOAT, zhang_f FLOAT, hsl FLOAT);"%scode
            self.cur.execute(cmd)
        except:
            pass

    def insert_fund_history_charges(self, his, fcode):
        today = time.strftime("%Y-%m-%d", time.localtime())
        arr = json.loads(his).get("Datas")

        date = self.get_fund_last_history_charge_date(fcode)
        if date is None:
            self.create_fund_history_table(fcode) 
            self.conn.commit()
            ts1 = time.strptime("1990-1-1", "%Y-%m-%d")
        else:
            ts1 = time.strptime(date,"%Y-%m-%d")

        for node in arr:
            ts2 = time.strptime(node["FSRQ"], "%Y-%m-%d") 
            if ts2 > ts1 and node["FSRQ"] != today:
                if len(node["JZZZL"]) == 0:
                    self.cur.execute('INSERT INTO f%s (fsrq, dwjz) VALUES ("%s", %s);'%(fcode, node["FSRQ"], node["DWJZ"]))
                else:
                    self.cur.execute('INSERT INTO f%s (fsrq, dwjz, jzzzl) VALUES ("%s", %s, %s);'%(fcode, node["FSRQ"], node["DWJZ"], node["JZZZL"]))

                self.conn.commit()

    def insert_stock_history_charge(self, his, scode):
        today = time.strftime("%Y-%m-%d", time.localtime())
        date = self.get_stock_last_history_charge_date(scode)
        if date is None:
            self.create_stock_history_table(scode) 
            self.conn.commit()
            ts1 = time.strptime("1990-1-1", "%Y-%m-%d")
        else:
            ts1 = time.strptime(date, "%Y-%m-%d")

        for node in his:
            val = node.split(',')
            ts2 = time.strptime(val[0], "%Y-%m-%d")
            if ts2 > ts1 and val[0] != today:
                self.cur.execute('INSERT INTO s%s (fsrq, start_charge, end_charge, max_charge, min_charge, cjl, cjr, zhen_f, zhang_f, hsl) VALUES ' 
                            '("%s", %s, %s, %s, %s, %s, %s, %s, %s, %s);' \
                            %(scode, val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[10]))

                self.conn.commit()


    def update_fund_real_time_charge(self, fcode, js):
        charge = js["Expansion"]["GZ"]
        self.cur.execute("UPDATE self_select SET real_time_charge = '%s' WHERE fcode = '%s'"%(charge, fcode))
        self.conn.commit()


def get_fund_last_history_charge_list(db_path, scode, start_date, end_date):
    pass