import sqlite3
class AssetDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        pass

    def get_coin_self_selection(self):
        res = []
        self.cur.execute('SELECT id, symbol, type, market, name FROM asset WHERE type = "coin"')
        rows = self.cur.fetchall()
        for row in rows:
            res.append(
                {
                    "id":row[0],
                    "symbol":row[1],
                    "type":row[2],
                    "market":row[3],
                    "name": row[4]
                })
        
        return res

    def get_fund_self_selection(self):
        res = []
        self.cur.execute('SELECT id, symbol, type, market, name FROM asset WHERE type = "fund"')
        rows = self.cur.fetchall()
        for row in rows:
            #res.append({"code": row[0], "name": row[1]})
            res.append(
                {
                    "id": row[0],
                    "symbol": row[1],
                    "type": row[2],
                    "market": row[3],
                    "name": row[4]
                })
        return res
    
    def get_asset_by_id(self, id):
        self.cur.execute('SELECT symbol, name, type, market FROM asset WHERE id == %d'%id) 
        rows = self.cur.fetchall()
        return { 
                    "symbol":rows[0][0], 
                    "name":rows[0][1],
                    "type":rows[0][2],
                    "market": rows[0][3]
                }

    def get_stock_self_selection(self):
        res = []
        self.cur.execute('SELECT id, symbol, name, type, market FROM asset WHERE type = "stock"')
        rows = self.cur.fetchall()
        for row in rows:
            res.append(
                {
                    "id": row[0],
                    "symbol": row[1], 
                    "name": row[2], 
                    "type": row[3],
                    "market": row[4]
                })
        return res

    def get_asset_by_code(self, code):
        self.cur.execute('SELECT code, name, type, market FROM asset WHERE code == "%s"'%code) 
        rows = self.cur.fetchall()
        return { 
                    "code":rows[0][0], 
                    "name":rows[0][1],
                    "type":rows[0][2],
                    "market":rows[0][3]
                }
    