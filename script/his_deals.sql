/*
 Navicat Premium Data Transfer

 Source Server         : em
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 09/10/2022 11:18:37
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for his_deals
-- ----------------------------
DROP TABLE IF EXISTS "his_deals";
CREATE TABLE "his_deals" (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
  , account_id INTEGER
  , policy_id INTEGER
  , step INTEGER
  , asset_id TEXT
  , contract_id TEXT
  , direction TEXT
  , cash TEXT
  , vol TEXT
  , date TEXT
);

-- ----------------------------
-- Auto increment value for his_deals
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 140 WHERE name = 'his_deals';

PRAGMA foreign_keys = true;
