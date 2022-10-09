/*
 Navicat Premium Data Transfer

 Source Server         : em
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 09/10/2022 11:19:01
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS "account";
CREATE TABLE "account" (
    id INTEGER PRIMARY KEY AUTOINCREMENT
  , userid TEXT
  , duration INTEGER
  , password TEXT
);

-- ----------------------------
-- Auto increment value for account
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 2 WHERE name = 'account';

PRAGMA foreign_keys = true;
