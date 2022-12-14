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
  , price TEXT
  , asset_count TEXT DEFAULT(0)
  , date TEXT
  , para TEXT
);

PRAGMA foreign_keys = true;
