/*
 Navicat Premium Data Transfer

 Source Server         : em
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 09/10/2022 11:19:11
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for collect
-- ----------------------------
DROP TABLE IF EXISTS "collect";
CREATE TABLE collect (
    id INTEGER PRIMARY KEY AUTOINCREMENT
  , code TEXT NOT NULL
  , name TEXT
  , price TEXT
  , type TEXT NOT NULL
  , market TEXT
);

-- ----------------------------
-- Records of collect
-- ----------------------------
BEGIN;
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (0, '0', '国债', NULL, 'b', 'N/A');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (1, '001632', '天弘中证食品饮料ETF联接C', NULL, 'f', '37');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (2, '003096', '中欧医疗健康混合C', NULL, 'f', '142');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (3, '004643', '南方房地产ETF联接C', NULL, 'f', '100');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (4, '004753', '广发中证传媒ETF联接C', NULL, 'f', '34');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (5, '320007', '诺安成长混合', NULL, 'f', '141');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (6, '004744', '易方达创业板ETF联接C', NULL, 'f', '128');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (7, '011609', '易方达科创板50ETF联接C', NULL, 'f', '128');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (8, '601166', '兴业银行', '17.00', 's', 'SH');
INSERT INTO "collect" ("id", "code", "name", "price", "type", "market") VALUES (9, '000338', '潍柴动力', NULL, 's', 'SH');
COMMIT;

-- ----------------------------
-- Auto increment value for collect
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 9 WHERE name = 'collect';

PRAGMA foreign_keys = true;
