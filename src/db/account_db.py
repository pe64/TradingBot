import sqlite3

class AccountDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        pass
    
    def get_binance_accounts(self):
        res = []
        self.cur.execute('SELECT id, userid, duration, password FROM account WHERE type = "binance"')
        rows = self.cur.fetchall()
        for row in rows:
            res.append({
                "id": row[0],
                "API_KEY": row[1],
                "API_SECRET": row[3]
            })
        return res

    def get_account_by_id(self, id):
       self.cur.execute('SELECT id, userid, duration, password FROM account') 
       rows = self.cur.fetchall()
       return rows[0][1]

    def get_eastmoney_accounts(self):
        res = []
        self.cur.execute('SELECT id, userid, duration, password FROM account WHERE type = "eastmoney"')
        rows = self.cur.fetchall()
        for row in rows:
            res.append({
                    "id": row[0],
                    "userId": row[1],
                    "duration": row[2],
                    "authCode": "",
                    "type": "Z",
                    "password": row[3]
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
    
