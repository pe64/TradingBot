BEGIN;

CREATE TABLE asset (
    id INTEGER PRIMARY KEY AUTOINCREMENT
  , symbol TEXT NOT NULL
  , name TEXT
  , type TEXT NOT NULL
  , market TEXT
);

INSERT INTO asset(id, symbol, name, type, market) VALUES(1, '0', '国债', 'bond', 'N/A');
INSERT INTO asset(id, symbol, name, type, market) VALUES(2, '001632', '天弘中证食品饮料ETF联接C', 'fund', '37');
INSERT INTO asset(id, symbol, name, type, market) VALUES(3, '003096', '中欧医疗健康混合C', 'fund', '142');
INSERT INTO asset(id, symbol, name, type, market) VALUES(4, '004643', '南方房地产ETF联接C', 'fund', '100');
INSERT INTO asset(id, symbol, name, type, market) VALUES(5, '004753', '广发中证传媒ETF联接C', 'fund', '34');
INSERT INTO asset(id, symbol, name, type, market) VALUES(6, '320007', '诺安成长混合', 'fund', '141');
INSERT INTO asset(id, symbol, name, type, market) VALUES(7, '004744', '易方达创业板ETF联接C', 'fund', '128');
INSERT INTO asset(id, symbol, name, type, market) VALUES(8, '011609', '易方达科创板50ETF联接C', 'fund', '128');
INSERT INTO asset(id, symbol, name, type, market) VALUES(9, '013810', '广发科创50ETF发起式联接A', 'fund', '34');
INSERT INTO asset(id, symbol, name, type, market) VALUES(10, '110020', '易沪深300ETF联接A', 'fund', '128');
INSERT INTO asset(id, symbol, name, type, market) VALUES(11, '007379', '易方达上证50ETF联接A', 'fund', '128');
INSERT INTO asset(id, symbol, name, type, market) VALUES(12, '000307', '易方达黄金ETF联接A', 'fund', '128');
INSERT INTO asset(id, symbol, name, type, market) VALUES(13, '601166', '兴业银行', 'stock', 'sh');
INSERT INTO asset(id, symbol, name, type, market) VALUES(14, '000338', '潍柴动力', 'stock', 'sz');
INSERT INTO asset(id, symbol, name, type, market) VALUES(15, 'SOLUSDT', 'SOLUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(16, 'BTCUSDT', 'BTCUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(17, 'ETHUSDT', 'ETHUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(18, 'LTCUSDT', 'LTCUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(19, 'SOLUSDT', 'SOLUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(20, 'WLDUSDT', 'WLDUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(21, 'COMPUSDT', 'COMPUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(22, 'BCHUSDT', 'BCHUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(23, 'LDOUSDT', 'LDOUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(24, 'MKRUSDT', 'MKRUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(25, 'UNIUSDT', 'UNIUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(26, 'CFXUSDT', 'CFXUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(27, 'MATICUSDT', 'MATICUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(28, 'DOGEUSDT', 'DOGEUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(29, 'BNBUSDT', 'BNBUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(30, 'CRVUSDT', 'CRVUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(31, 'PEPEUSDT', 'PEPEUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(32, 'SUIUSDT', 'SUIUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(33, 'AVAXUSDT', 'AVAXUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(34, 'SHIBUSDT', 'SHIBUSDT', 'coin', 'binance');
INSERT INTO asset(id, symbol, name, type, market) VALUES(35, 'FTMUSDT', 'FTMUSDT', 'coin', 'binance');

COMMIT;