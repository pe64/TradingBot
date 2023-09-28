/*
 Navicat Premium Data Transfer

 Source Server         : em
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 09/10/2022 11:18:17
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for policy
-- ----------------------------
DROP TABLE IF EXISTS "policy";
CREATE TABLE "policy" (
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

INSERT INTO "table" VALUES(1,1,1,15,'autobuy','10.045','0','-0.0481999999999996','{"period":"1w","type":"asset","count":5.0}','21.0','20230921144235','{"start_time": {"week_day": "Thu","time": "14:30"},"end_time": {"week_day": "Thu","time": "15:59"}}');

PRAGMA foreign_keys = true;
