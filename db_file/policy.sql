--
-- SQLiteStudio v3.4.2 生成的文件，周一 10月 9 17:03:01 2023
--
-- 所用的文本编码：System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：policy
CREATE TABLE IF NOT EXISTS "policy" (
    id INTEGER PRIMARY KEY
  , account_id INTEGER
  , enabled INT DEFAULT(0)
  , asset_id INTEGER
  , type TEXT
  , cash TEXT
  , cash_into TEXT DEFAULT(0.00)
  , cash_inuse TEXT DEFAULT(0.00)
  , condition TEXT
  , asset_count TEXT DEFAULT(0)
  , timestamp TEXT
  , execution_time TEXT
);
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (1, 1, 1, 15, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (2, 1, 1, 16, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (3, 1, 1, 17, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (4, 1, 1, 18, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (5, 1, 1, 19, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (6, 1, 1, 20, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (7, 1, 1, 21, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (8, 1, 1, 22, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164813', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (9, 1, 1, 23, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164818', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (10, 1, 1, 24, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164823', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (11, 1, 1, 25, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (12, 1, 1, 26, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164833', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (13, 1, 1, 27, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008170036', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (14, 1, 1, 28, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164325', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (15, 1, 1, 29, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008165308', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (16, 1, 1, 30, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20230928144235', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (17, 1, 1, 31, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008170239', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (18, 1, 1, 32, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20230928144235', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (19, 1, 1, 33, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008173402', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (20, 1, 1, 34, 'autobuy', '100.0', '0.0', '0.0', '{"period":"1w","type":"cash","count":10.0}', '0.0', '20231008164911', '{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (21, 2, 1, 9, 'autobuy', '10000.0', '0.0', '0.0', '{"period":"1d","type":"cash","count":100.0}', '0.0', '20231009132400', '{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (22, 2, 1, 10, 'autobuy', '10000.0', '0.0', '0.0', '{"period":"1d","type":"cash","count":100.0}', '0.0', '20231009132400', '{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (23, 2, 1, 11, 'autobuy', '10000.0', '0.0', '0.0', '{"period":"1d","type":"cash","count":100.0}', '0.0', '20231009132500', '{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');
INSERT INTO policy (id, account_id, enabled, asset_id, type, cash, cash_into, cash_inuse, condition, asset_count, timestamp, execution_time) VALUES (24, 2, 1, 12, 'autobuy', '10000.0', '0.0', '0.0', '{"period":"1d","type":"cash","count":100.0}', '0.0', '20230928144235', '{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
