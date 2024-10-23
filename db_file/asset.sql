PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE asset (
    id INTEGER PRIMARY KEY AUTOINCREMENT
  , symbol TEXT NOT NULL
  , name TEXT
  , type TEXT NOT NULL
  , market TEXT
);
INSERT INTO asset VALUES(1,'0','国债','bond','N/A');
--INSERT INTO asset VALUES(2,'001632','天弘中证食品饮料ETF联接C','fund','37');
--INSERT INTO asset VALUES(3,'003096','中欧医疗健康混合C','fund','142');
--INSERT INTO asset VALUES(4,'004643','南方房地产ETF联接C','fund','100');
--INSERT INTO asset VALUES(5,'004753','广发中证传媒ETF联接C','fund','34');
--INSERT INTO asset VALUES(6,'320007','诺安成长混合','fund','141');
--INSERT INTO asset VALUES(7,'004744','易方达创业板ETF联接C','fund','128');
--INSERT INTO asset VALUES(8,'011609','易方达科创板50ETF联接C','fund','128');
INSERT INTO asset VALUES(2,'013810','广发科创50ETF发起式联接A','fund','34');
INSERT INTO asset VALUES(3,'110020','易沪深300ETF联接A','fund','128');
INSERT INTO asset VALUES(4,'007379','易方达上证50ETF联接A','fund','128');
INSERT INTO asset VALUES(5,'000307','易方达黄金ETF联接A','fund','128');
INSERT INTO asset VALUES(6,'009051','易方达中证红利ETF联接A','fund','128');
INSERT INTO asset VALUES(7,'601166','兴业银行','stock','sh');
INSERT INTO asset VALUES(8,'000338','潍柴动力','stock','sz');
INSERT INTO asset VALUES(9,'SOLUSDT','SOLUSDT','coin','binance');
INSERT INTO asset VALUES(10,'BTCUSDT','BTCUSDT','coin','binance');
INSERT INTO asset VALUES(11,'ETHUSDT','ETHUSDT','coin','binance');
INSERT INTO asset VALUES(12,'LTCUSDT','LTCUSDT','coin','binance');
--INSERT INTO asset VALUES(19,'WLDUSDT','WLDUSDT','coin','binance');
--INSERT INTO asset VALUES(20,'COMPUSDT','COMPUSDT','coin','binance');
--INSERT INTO asset VALUES(21,'BCHUSDT','BCHUSDT','coin','binance');
--INSERT INTO asset VALUES(22,'LDOUSDT','LDOUSDT','coin','binance');
--INSERT INTO asset VALUES(23,'MKRUSDT','MKRUSDT','coin','binance');
--INSERT INTO asset VALUES(24,'UNIUSDT','UNIUSDT','coin','binance');
--INSERT INTO asset VALUES(25,'CFXUSDT','CFXUSDT','coin','binance');
--INSERT INTO asset VALUES(26,'MATICUSDT','MATICUSDT','coin','binance');
--INSERT INTO asset VALUES(27,'DOGEUSDT','DOGEUSDT','coin','binance');
--INSERT INTO asset VALUES(28,'BNBUSDT','BNBUSDT','coin','binance');
--INSERT INTO asset VALUES(29,'CRVUSDT','CRVUSDT','coin','binance');
--INSERT INTO asset VALUES(30,'PEPEUSDT','PEPEUSDT','coin','binance');
--INSERT INTO asset VALUES(31,'SUIUSDT','SUIUSDT','coin','binance');
--INSERT INTO asset VALUES(32,'AVAXUSDT','AVAXUSDT','coin','binance');
--INSERT INTO asset VALUES(33,'SHIBUSDT','SHIBUSDT','coin','binance');
--INSERT INTO asset VALUES(34,'FTMUSDT','FTMUSDT','coin','binance');
--INSERT INTO asset VALUES(35,'ORDIUSDT','ORDIUSDT','coin','binance');
--INSERT INTO asset VALUES(36,'BLURUSDT','BLURUSDT','coin','binance');
--INSERT INTO asset VALUES(37,'BONKUSDT','BONKUSDT','coin','binance');
--INSERT INTO asset VALUES(38,'OPUSDT','OPUSDT','coin','binance');
--INSERT INTO asset VALUES(39,'ARBUSDT','ARBUSDT','coin','binance');
--INSERT INTO asset VALUES(40,'AAVEUSDT','AAVEUSDT','coin','binance');
--INSERT INTO asset VALUES(41,'GMXUSDT','GMXUSDT','coin','binance');
--INSERT INTO asset VALUES(42,'RDNTUSDT','RDNTUSDT','coin','binance');
--INSERT INTO asset VALUES(43,'MAGICUSDT','MAGICUSDT','coin','binance');
--INSERT INTO asset VALUES(44,'SNXUSDT','SNXUSDT','coin','binance');
--INSERT INTO asset VALUES(45,'LRCUSDT','LRCUSDT','coin','binance');
--INSERT INTO asset VALUES(46,'IMXUSDT','IMXUSDT','coin','binance');
COMMIT;
