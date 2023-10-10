BEGIN;

CREATE TABLE asset (
    id INTEGER PRIMARY KEY AUTOINCREMENT
  , symbol TEXT NOT NULL
  , name TEXT
  , type TEXT NOT NULL
  , market TEXT
);

INSERT INTO asset(symbol, name, type, market) VALUES('0', '国债', 'bond', 'N/A');
INSERT INTO asset(symbol, name, type, market) VALUES('001632', '天弘中证食品饮料ETF联接C', 'fund', '37');
INSERT INTO asset(symbol, name, type, market) VALUES('003096', '中欧医疗健康混合C', 'fund', '142');
INSERT INTO asset(symbol, name, type, market) VALUES('004643', '南方房地产ETF联接C', 'fund', '100');
INSERT INTO asset(symbol, name, type, market) VALUES('004753', '广发中证传媒ETF联接C', 'fund', '34');
INSERT INTO asset(symbol, name, type, market) VALUES('320007', '诺安成长混合', 'fund', '141');
INSERT INTO asset(symbol, name, type, market) VALUES('004744', '易方达创业板ETF联接C', 'fund', '128');
INSERT INTO asset(symbol, name, type, market) VALUES('011609', '易方达科创板50ETF联接C', 'fund', '128');
INSERT INTO asset(symbol, name, type, market) VALUES('013810', '广发科创50ETF发起式联接A', 'fund', '34');
INSERT INTO asset(symbol, name, type, market) VALUES('110020', '易沪深300ETF联接A', 'fund', '128');
INSERT INTO asset(symbol, name, type, market) VALUES('007379', '易方达上证50ETF联接A', 'fund', '128');
INSERT INTO asset(symbol, name, type, market) VALUES('000307', '易方达黄金ETF联接A', 'fund', '128');
INSERT INTO asset(symbol, name, type, market) VALUES('601166', '兴业银行', 'stock', 'sh');
INSERT INTO asset(symbol, name, type, market) VALUES('000338', '潍柴动力', 'stock', 'sz');
INSERT INTO asset(symbol, name, type, market) VALUES('SOLUSDT', 'SOLUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('BTCUSDT', 'BTCUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('ETHUSDT', 'ETHUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('LTCUSDT', 'LTCUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('SOLUSDT', 'SOLUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('WLDUSDT', 'WLDUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('COMPUSDT', 'COMPUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('BCHUSDT', 'BCHUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('LDOUSDT', 'LDOUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('MKRUSDT', 'MKRUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('UNIUSDT', 'UNIUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('CFXUSDT', 'CFXUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('MATICUSDT', 'MATICUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('DOGEUSDT', 'DOGEUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('BNBUSDT', 'BNBUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('CRVUSDT', 'CRVUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('PEPEUSDT', 'PEPEUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('SUIUSDT', 'SUIUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('AVAXUSDT', 'AVAXUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('SHIBUSDT', 'SHIBUSDT', 'coin', 'binance');
INSERT INTO asset(symbol, name, type, market) VALUES('FTMUSDT', 'FTMUSDT', 'coin', 'binance');

COMMIT;