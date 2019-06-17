/**
 mysql
 CREATE TABLE `NewTable` (
 `id`  int(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
 `pid`  int(10) NOT NULL DEFAULT 0 COMMENT '父id' ,
 `uid`  int(11) NOT NULL COMMENT '添加人id' ,
 `pathid`  varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '父子id串，如0-1-2' ,
 `name`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '请求名称' ,
 `type`  char(1) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1' COMMENT '1菜单; 2接口请求' ,
 `url`  varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '请求地址' ,
 `addTime`  datetime NOT NULL COMMENT '添加时间' ,
 `upTime`  datetime NOT NULL COMMENT '更新时间' ,
 `note`  varchar(512) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '菜单或请求的说明' ,
 `sx`  int(10) NOT NULL DEFAULT 999 COMMENT '菜单的显示顺序' ,
 `guest`  char(1) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0' COMMENT '游客可查看：\'1\'可以， \'0\'不可以' ,
 PRIMARY KEY (`id`)
 )
 ENGINE=MyISAM
 DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
 COMMENT='菜单或请求'
 AUTO_INCREMENT=34
 CHECKSUM=0
 ROW_FORMAT=DYNAMIC
 DELAY_KEY_WRITE=0
 ;
 */

//_ = {
//  name: 'a_req',
//  type: 'mysql',
//  engine: 'MyISAM',
//  charset: 'utf8',
//  collate: 'utf8_general_ci',
//  comment: '菜单或请求',
//  fields: {
//    id: {type: 'int', len:10,sign: 'unsigned', isnull: 0, auto_increment: 1, comment: '自增主键'},
//    pid: {type: 'int', len:10,sign: 'unsigned', isnull: 0, default: 0, comment: '父id'},
//    uid: {type: 'int', len:11,sign: 'unsigned', isnull: 0, comment: '添加人id'},
//    pathid: {type: 'varchar', len:128, isnull: 0, default: 0, comment: '添加人id'},
//  }
//}