PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
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
INSERT INTO policy VALUES(1,2,1,6,'autobuy','9700.0','0.0','5300.0','{"period":"1d","type":"cash","count":100.0}','8825.32839923066','20240220143100','{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');

--INSERT INTO policy VALUES(1,1,0,15,'autobuy','179.9597','0.0','20.0403','{"period":"1w","type":"cash","count":10.0}','0.63','20231126150125','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(2,1,1,16,'autobuy','130.3064358','0.0','69.6935642','{"period":"1w","type":"cash","count":10.0}','0.00178','20240225174246','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(3,1,1,17,'autobuy','140.030091','0.0','59.969909','{"period":"1w","type":"cash","count":10.0}','0.0289','20240128165818','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(4,1,1,18,'autobuy','129.96605','0.0','70.03395','{"period":"1w","type":"cash","count":10.0}','1.033','20240225174259','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(5,1,0,19,'autobuy','129.7755','0.0','70.2245','{"period":"1w","type":"cash","count":10.0}','29.8','20240204170114','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(6,1,0,20,'autobuy','130.01057','0.0','69.98943','{"period":"1w","type":"cash","count":10.0}','1.382','20240204143351','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(7,1,0,21,'autobuy','109.8757','0.0','90.1243','{"period":"1w","type":"cash","count":10.0}','0.384','20240225174316','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(8,1,1,22,'autobuy','119.99058','0.0','80.00942','{"period":"1w","type":"cash","count":10.0}','30.61','20240303174243','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(9,1,1,23,'autobuy','120.1977','0.0','79.8023','{"period":"1w","type":"cash","count":10.0}','0.0535','20240225174628','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(10,1,0,24,'autobuy','129.9425','0.0','70.0575','{"period":"1w","type":"cash","count":10.0}','13.32','20240128170200','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(11,1,0,25,'autobuy','169.9941','0.0','30.0059','{"period":"1w","type":"cash","count":10.0}','246.0','20231119143148','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(12,1,1,26,'autobuy','130.07209','0.0','69.92791','{"period":"1w","type":"cash","count":10.0}','93.4','20240204143128','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(13,1,1,27,'autobuy','120.01484','0.0','79.98516','{"period":"1w","type":"cash","count":10.0}','995.0','20240204171247','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(14,1,1,28,'autobuy','130.0801','0.0','69.9199','{"period":"1w","type":"cash","count":10.0}','0.274','20240204165909','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(15,1,1,29,'autobuy','119.96082','0.0','80.03918','{"period":"1w","type":"cash","count":10.0}','153.6','20240204170735','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(16,1,0,30,'autobuy','159.99999896','0.0','40.00000104','{"period":"1w","type":"cash","count":10.0}','41393693.0','20231126143326','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(17,1,0,31,'autobuy','170.04919','0.0','29.95081','{"period":"1w","type":"cash","count":10.0}','67.9','20231119143215','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(18,1,1,32,'autobuy','140.4238','0.0','59.5762','{"period":"1w","type":"cash","count":10.0}','2.66','20240225174718','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(19,1,0,33,'autobuy','119.99999862','0.0','80.00000138','{"period":"1w","type":"cash","count":10.0}','8965687.0','20240225174723','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(20,1,0,34,'autobuy','150.082','0.0','49.918','{"period":"1w","type":"cash","count":10.0}','162.0','20240107143351','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(22,2,0,10,'autobuy','9800.0','0.0','5200.0','{"period":"1d","type":"cash","count":100.0}','3914.75772145466','20240226143100','{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');
--INSERT INTO policy VALUES(23,2,0,11,'autobuy','9600.0','0.0','5400.0','{"period":"1d","type":"cash","count":100.0}','5345.86949535008','20240226143100','{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');
--INSERT INTO policy VALUES(24,2,0,12,'autobuy','9600.0','0.0','3400.0','{"period":"1d","type":"cash","count":100.0}','2109.14248474706','20240223145100','{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');
--INSERT INTO policy VALUES(25,3,0,9,'autobuy','4800.0','0.0','5200.0','{"period":"1d","type":"cash","count":100.0}','8644.92067778018','20240202143200','{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}');
--INSERT INTO policy VALUES(26,1,1,35,'autobuy','139.67392','0.0','60.32608','{"period":"1w","type":"cash","count":10.0}','1.02','20240225174435','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(27,1,1,36,'autobuy','120.0363','0.0','79.9637','{"period":"1w","type":"cash","count":10.0}','146.8','20240303174742','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(28,1,0,37,'autobuy','150.00000355','0.0','49.99999645','{"period":"1w","type":"cash","count":10.0}','4316063.0','20240225174447','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(29,1,1,38,'autobuy','170.02275','0.0','29.97725','{"period":"1w","type":"cash","count":10.0}','9.23','20240225174750','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(30,1,1,39,'autobuy','179.94856','0.0','20.05144','{"period":"1w","type":"cash","count":10.0}','11.2','20240204144048','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(31,1,1,40,'autobuy','170.00615','0.0','29.99385','{"period":"1w","type":"cash","count":10.0}','0.33','20240204170539','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(32,1,1,41,'autobuy','169.9793','0.0','30.0207','{"period":"1w","type":"cash","count":10.0}','0.675','20240204165730','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(33,1,1,42,'autobuy','169.803','0.0','30.197','{"period":"1w","type":"cash","count":10.0}','97.0','20240303151904','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(34,1,1,43,'autobuy','180.03866','0.0','19.96134','{"period":"1w","type":"cash","count":10.0}','16.1','20240225175131','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(35,1,1,44,'autobuy','169.8562','0.0','30.1438','{"period":"1w","type":"cash","count":10.0}','9.4','20240204170030','{"start_time": {"week_day": "Sun","time": "14:30"},"end_time": {"week_day": "Sun","time": "17:59"}}');
--INSERT INTO policy VALUES(36,1,1,45,'autobuy','179.9696','0.0','20.0304','{"period":"1w","type":"cash","count":10.0}','86.0','20240204143550','{"start_time": {"week_day": "Sun","time": 1|2|0|6|autobuy|9700.0|0.0|5300.0|{"period":"1d","type":"cash","count":100.0}|8825.32839923066|20240220143100|{"start_time": {"time": "14:30"},"end_time": {"time": "14:55"}}
COMMIT;