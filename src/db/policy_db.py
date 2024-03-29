import sqlite3
import json

class PolicyDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        pass
    
    def get_policys(self):
        res = []
        self.cur.execute('SELECT id, account_id, type, asset_id, cash, cash_into, cash_inuse, asset_count, timestamp, condition, execution_time FROM policy WHERE enabled == 1')
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
                "timestamp": row[8],
                "condition": json.loads(row[9]),
                "execute_time": json.loads(row[10])
            })
        return res

    def get_policy_by_account_id(self, a_id):
        res = []
        self.cur.execute('SELECT id, account_id, type, asset_id, cash, cash_into, cash_inuse, asset_count, timestamp, condition FROM policy WHERE enabled == 1 AND account_id == %d'%a_id)
        rows = self.cur.fetchall()
        for row in rows:
            res.append(
                {
                    "id": row[0],
                    "account_id": row[1],
                    "type": row[2],
                    "asset_id": row[3],
                    "cash": row[4],
                    "cash_into": row[5],
                    "cash_inuse": row[6],
                    "asset_count": row[7],
                    "timestamp": row[8],
                    "condition": json.loads(row[9])
                })
        return res
    

    def update_policy_status(self, policy_id, cash_inuse, cash, asset_count, today, condition = None):
        if condition is None:
            cmd = "UPDATE policy SET cash_inuse = %s, cash = %s, asset_count = %s, timestamp = %s WHERE id == %d" \
                %(cash_inuse, cash, asset_count, today, policy_id)
        else:
            cmd = "UPDATE policy SET cash_inuse = %s, cash = %s, asset_count = %s, timestamp = %s, condition = %s WHERE id == %d" \
                %(cash_inuse, cash, asset_count, today, condition, policy_id)
        
        self.cur.execute(cmd)
        self.conn.commit()
    
    def get_account_policy(self, a_id):
        res = []
        self.cur.execute('SELECT id, account_id, type, asset_id, cash, cash_into, cash_inuse, asset_count, timestamp, condition FROM policy WHERE enabled == 1 AND account_id == %d'%a_id)
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
                "timestamp": row[8],
                "condition": json.loads(row[9])
            })
        return res