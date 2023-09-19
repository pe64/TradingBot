BEGIN;

CREATE TABLE asset (
    id INTEGER PRIMARY KEY AUTOINCREMENT
  , symbol TEXT NOT NULL
  , name TEXT
  , type TEXT NOT NULL
  , market TEXT
);

INSERT INTO asset(id, symbol, name, type, market) VALUES(0, '0', '国债', 'bond', 'N/A');
INSERT INTO asset(id, symbol, name, type, market) VALUES(1, '001632', '天弘中证食品饮料ETF联接C', 'fund', '37');
INSERT INTO asset(id, symbol, name, type, market) VALUES(2, '003096', '中欧医疗健康混合C', 'fund', '142');
INSERT INTO asset(id, symbol, name, type, market) VALUES(3, '004643', '南方房地产ETF联接C', 'fund', '100');
INSERT INTO asset(id, symbol, name, type, market) VALUES(4, '004753', '广发中证传媒ETF联接C', 'fund', '34');
INSERT INTO asset(id, symbol, name, type, market) VALUES(5, '320007', '诺安成长混合', 'fund', '141');
INSERT INTO asset(id, symbol, name, type, market) VALUES(6, '004744', '易方达创业板ETF联接C', 'fund', '128');
INSERT INTO asset(id, symbol, name, type, market) VALUES(7, '011609', '易方达科创板50ETF联接C', 'fund', '128');
INSERT INTO asset(id, symbol, name, type, market) VALUES(8, '601166', '兴业银行', 'stock', 'sh');
INSERT INTO asset(id, symbol, name, type, market) VALUES(9, '000338', '潍柴动力', 'stock', 'sz');
INSERT INTO asset(id, symbol, name, type, market) VALUES(10, 'SOLUSDT', 'SOLUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(11, 'BTCUSDT', 'BTCUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(12, 'ETHUSDT', 'ETHUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(13, 'LTCUSDT', 'LTCUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(14, 'SOLUSDT', 'SOLUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(15, 'WLDUSDT', 'WLDUSDT', 'coin', 'binance');

COMMIT;