import sqlite3
class AssetDB:
    def __init__(self, db_path):
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

    def get_stock_self_selection(self):
        res = []
        self.cur.execute('SELECT code, name, market FROM collect WHERE type = "s"')
        rows = self.cur.fetchall()
        for row in rows:
            res.append({"code": row[0], "name": row[1], "market": row[2]})
        return res

    def get_asset_by_code(self, code):
        self.cur.execute('SELECT code, name, type, market FROM collect WHERE code == "%s"'%code) 
        rows = self.cur.fetchall()
        return { 
                    "code":rows[0][0], 
                    "name":rows[0][1],
                    "type":rows[0][2],
                    "market":rows[0][3]
                }
    