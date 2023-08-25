from email import policy
import sqlite3
class SqliteEM:
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        pass
    
    def get_coin_self_selection(self):
        res = []
        self.cur.execute('SELECT code FROM collect WHERE type = "c"')
        rows = self.cur.fetchall()
        for row in rows:
            res.append(row[0])
        
        return res

    def get_fund_self_selection(self):
        res = []
        self.cur.execute('SELECT code, name FROM collect WHERE type = "f"')
        rows = self.cur.fetchall()
        for row in rows:
            #res.append({"code": row[0], "name": row[1]})
            res.append(row[0])
        return res
    
    def get_asset_by_id(self, id):
        self.cur.execute('SELECT code, name, type FROM collect WHERE id == %d'%id) 
        rows = self.cur.fetchall()
        return { 
                    "code":rows[0][0], 
                    "name":rows[0][1],
                    "type":rows[0][2]
                }
    
    def get_accounts(self):
        res = []
        self.cur.execute('SELECT id, userid, duration, password FROM account')
        rows = self.cur.fetchall()
        for row in rows:
            res.append({"id": row[0],
                "arg":{
                    "userId": row[1],
                    "duration": row[2],
                    "authCode": "",
                    "type": "Z",
                    "password": row[3]
                }
            })
        return res
    
    def get_account_by_id(self, id):
       self.cur.execute('SELECT id, userid, duration, password FROM account') 
       rows = self.cur.fetchall()
       return rows[0][1]

    def get_account_policy(self, a_id):
        res = []
        self.cur.execute('SELECT id, account_id, type, asset_id, cash, cash_into, cash_inuse, asset_count, para, date, price FROM policy WHERE enabled == 1 AND account_id == %d'%a_id)
        rows = self.cur.fetchall()
        for row in rows:
            res.append({
                "id": row[0],
                "account_id": row[1],
                "type": row[2],
                "asset_id": row[3],
                "cash": row[4],
                "cash_into": row[5],
                "cash_inuse": row[6],
                "asset_count": row[7],
                "para": row[8],
                "date": row[9],
                "price": row[10]
            })
        return res
    
    def get_his_deals_contract_by_step(self, step, a_id):
        res = []
        cmd = 'SELECT contract_id  FROM his_deals WHERE step == %d AND account_id == %d'%(step, a_id)
        self.cur.execute(cmd)
        rows = self.cur.fetchall()
        for row in rows:
            res.append(row[0])
    
        return res
    
    def update_his_deals_vol(self, contract, vol, date):
        cmd = 'UPDATE his_deals SET step = 1, vol = "%s", date = "%s" WHERE contract_id == "%s"'%(str(vol), str(date), contract)
        self.cur.execute(cmd)
        self.conn.commit()
        return
    
    def get_his_deals_by_step_and_policy(self, step, a_id, p_id, code):
        res = []
        cmd = 'SELECT contract_id, direction, vol, cash FROM his_deals WHERE step == %d AND account_id == %d AND policy_id == %d AND asset_id == "%s"'%(step, a_id, p_id, code)
        self.cur.execute(cmd)
        rows = self.cur.fetchall()
        for row in rows:
            res.append({
                "contract_id": row[0],
                "direction": row[1],
                "vol": row[2],
                "cash": row[3]
            })
        
        return res
    
    def update_policy_asset_count(self, p_id, asset_count, cash_into):
        #cmd = 'SELECT asset_count, cash_into from policy WHERE id == %d'%p_id
        #self.cur.execute(cmd)
        #rows = self.cur.fetchall()
        cmd = 'UPDATE policy SET asset_count = "%s", cash_into = "%s" WHERE id == %d'%(asset_count, cash_into, p_id)
        self.cur.execute(cmd)
        self.conn.commit()
        return
    
    def update_his_deals_step(self, contract_id, step):
        cmd = 'UPDATE his_deals SET step = %d WHERE contract_id == "%s"' %(step, contract_id)
        self.cur.execute(cmd)
        self.conn.commit()
        return
    
    #def update_policy_cash_inuse(self, p_id, cash, today):
    #    cmd = 'SELECT cash, cash_inuse FROM policy WHERE id == %d'%p_id
    #    self.cur.execute(cmd)
    #    rows = self.cur.fetchall()
    #    ret_use = float(rows[0][1]) + float(cash)
    #    ret_cash = float(rows[0][0]) - float(cash)
    #    cmd = 'UPDATE policy SET cash_inuse = %s, cash = %s, date = %s WHERE id == %d'%(ret_use, ret_cash, today, p_id)
    #    self.cur.execute(cmd)
    #    self.conn.commit()
    
    def update_policy_status(self, policy_id, cash_inuse, cash, asset_count, today, price):
        if price is None:
            cmd = "UPDATE policy SET cash_inuse = %s, cash = %s, asset_count = %s, date = %s WHERE id == %d"%(cash_inuse, cash, asset_count, today, policy_id)
        else:
            cmd = "UPDATE policy SET cash_inuse = %s, cash = %s, asset_count = %s, date = %s, price = %s WHERE id == %d"%(cash_inuse, cash, asset_count, today, price, policy_id)
        
        self.cur.execute(cmd)
        self.conn.commit()


    def insert_his_deals(self, contract, a_id, p_id, code, dir, vol, today, step=0):
        if dir == "111":
            cmd = 'INSERT INTO his_deals(account_id, policy_id, step, asset_id, contract_id, direction, cash, date)' \
                    'VALUES ("%s", "%d", %d, "%s", "%s", "%s", "%s", "%s")' \
                    %(a_id, p_id, step, code, contract, dir, str(vol), today)
        else: 
            cmd = 'INSERT INTO his_deals(account_id, policy_id, step, asset_id, contract_id, direction, vol, date)' \
                    'VALUES ("%s", "%d", %d, "%s", "%s", "%s", "%s", "%s")' \
                    %(a_id, p_id, step, code, contract, dir, str(vol), today)
        self.cur.execute(cmd)
        self.conn.commit()
        return
    
    def get_asset_by_code(self, code):
        self.cur.execute('SELECT code, name, type, market FROM collect WHERE code == "%s"'%code) 
        rows = self.cur.fetchall()
        return { 
                    "code":rows[0][0], 
                    "name":rows[0][1],
                    "type":rows[0][2],
                    "market":rows[0][3]
                }
    def get_stock_self_selection(self):
        res = []
        self.cur.execute('SELECT code, name, market FROM collect WHERE type = "s"')
        rows = self.cur.fetchall()
        for row in rows:
            res.append({"code": row[0], "name": row[1], "market": row[2]})
        return res