"""
SQL仓库
"""

"""
alter table {table} add pid int default 0 not null after rid;
update {table} r inner join task t on t.tid = r.tid set r.pid = t.pid;
create index pid_index on {table} (pid);
"""
SELECT_PASSWORD = (
    "SELECT substring(password, 21, 32) as `key`,`gid`, `old_time`  "
    "FROM `user` WHERE `uid` = %(uid)s;"
)

GET_PASSWORD = "SELECT `uid`, `name`, `password` FROM `user` WHERE `uid` = %(uid)s;"

UPDATE_TOTP_KEY = "UPDATE `user` SET `otpkey` = %(otpkey)s  WHERE `uid` = %(uid)s"

LOGIN = (
    "SELECT a.uid, a.`name`, a.password, a.email, a.gid, b.`name` as `gname`, "
    "a.state  as `state` , a.lip as `lip`, a.otpkey as `otpkey` "
    "FROM `user` AS a INNER JOIN `group` AS b ON a.gid=b.gid "
    "WHERE a.name = %(user_name)s LIMIT 1;"
)

USER_IS_GROUP = "SELECT 1 FROM user WHERE `uid` = %(uid)s and `gid` = %(gid)s;"

UPDATE_TOKEN_MIN = "UPDATE `user` SET old_time = %(stamp)s WHERE uid = %(user_id)s;"

UPDATE_LOGIN_IP = "UPDATE `user` SET lip = %(lip)s WHERE uid = %(user_id)s;"

INSERT_PROJECT = (
    "INSERT INTO `project` (`target`, `name`, `uid`,`gid`) "
    "VALUES (%(target)s, %(name)s, %(uid)s, %(gid)s);"
)

GET_PROJECT_STATE = (
    "SELECT state from `project` "
    "where pid = %(pid)s AND (`uid` = %(uid)s or 0 = %(gid)s);"
)

UPDATE_PROJECT_STATE = "UPDATE `project` set state = %(state)s where pid = %(pid)s;"

GET_PROJECT_LIST_USER = (
    "SELECT `p`.`pid`, `target`, p.`name`, p.`uid`, u.`name` `uname`, "
    'p.`gid`, DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") as `starting`, '
    "IFNULL(pu.`time` > pc.`time`, 0) as `update`, p.state `pstate` "
    "FROM project as `p`  left join `user` as `u` on p.uid = u.uid "
    "left join `project_check` as `pc` on p.pid = pc.pid "
    "AND pc.uid = %(uid)s "
    "left join `project_update` as `pu` on p.pid = pu.pid "
    "WHERE p.`uid` = %(uid)s and p.state != 1 "
    "ORDER BY {order} {sort} LIMIT %(start)s, %(step)s"
)

GET_PROJECT_LIST_GROUP_STATE = (
    "SELECT 1 FROM project p left join project_update pu "
    "on pu.pid = p.pid WHERE p.gid = %(gid)s and "
    "pu.time > FROM_UNIXTIME(%(time)s) "
    "union select 1 from project where gid = %(gid)s "
    "and `starting` > FROM_UNIXTIME(%(time)s) limit 1;"
)

GET_PROJECT_LIST_ROOT_STATE = (
    "SELECT 1 FROM project p left join project_update pu "
    "on pu.pid = p.pid WHERE pu.time > FROM_UNIXTIME(%(time)s) "
    "union select 1 from project "
    "where `starting` > FROM_UNIXTIME(%(time)s) limit 1;"
)

GET_PROJECT_DELETE = (
    "SELECT `p`.`pid`, `target`, p.`name`, p.`uid`, u.`name` `uname`, "
    'p.`gid`, DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") '
    "as `starting`, p.state `pstate`,  "
    "(IFNULL(pu.`time`, 1) > IFNULL(pc.`time`, 0)) as `update` "
    "FROM project as `p`  left join `user` as `u` on p.uid = u.uid "
    "left join `project_check` as `pc` on p.pid = pc.pid "
    "AND pc.uid = %(uid)s "
    "left join `project_update` as `pu` on p.pid = pu.pid "
    "where p.state = 1 "
    "ORDER BY {order} {sort} LIMIT %(start)s, %(step)s"
)

GET_PROJECT_DELETE_COUNT = "SELECT count(1) as `count` FROM `project` WHERE state = 1;"

GET_PROJECT_LIST_GROUP_ADMIN = (
    "SELECT `p`.`pid`, `target`, p.`name`, p.`uid`, u.`name` `uname`, "
    'p.`gid`, DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") '
    "as `starting`,  p.`df`, p.state `pstate`,  "
    "(IFNULL(pu.`time`, 1) > IFNULL(pc.`time`, 0)) as `update` "
    "FROM project as `p`  left join `user` as `u` on p.uid = u.uid "
    "left join `project_check` as `pc` on p.pid = pc.pid "
    "AND pc.uid = %(uid)s "
    "left join `project_update` as `pu` on p.pid = pu.pid "
    "where p.state != 1 "
    "ORDER BY {order} {sort} LIMIT %(start)s, %(step)s"
)

GET_PROJECT_LIST_GROUP_LAB = (
    "SELECT `p`.`pid`, `target`, p.`name`, p.`uid`, u.`name` `uname`, p.`gid`, "
    'DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") as `starting`, p.state `pstate`, '
    "(IFNULL(pu.`time`, 1) > IFNULL(pc.`time`, 0)) as `update` "
    "FROM project as `p`  left join `user` as `u` on p.uid = u.uid "
    "left join `project_check` as `pc` on p.pid = pc.pid "
    "AND pc.uid = %(uid)s "
    "left join `project_update` as `pu` on p.pid = pu.pid "
    "WHERE (p.`gid` = 100 or p.`gid` = 1) and p.state != 1 "
    "ORDER BY {order} {sort} LIMIT %(start)s, %(step)s"
)

GET_PROJECT_LIST_GROUP_USER = (
    "SELECT `p`.`pid`, `target`, p.`name`, p.`uid`, u.`name` `uname`,p.`gid`,"
    'DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") `starting`, p.state `pstate`, '
    "(IFNULL(pu.`time`, 1) > IFNULL(pc.`time`, 0)) as `update` "
    "FROM project as `p`  left join `user` as `u` on p.uid = u.uid "
    "left join `project_check` as `pc` on p.pid = pc.pid "
    "AND pc.uid = %(uid)s "
    "left join `project_update` as `pu` on p.pid = pu.pid "
    "WHERE p.`gid` = %(gid)s and p.state != 1  "
    "ORDER BY {order} {sort} LIMIT %(start)s, %(step)s"
)

GET_PROJECT_LIST_GROUP_SEARCH = (
    "SELECT `p`.`pid`, `target`, p.`name`, p.`uid`, u.`name` `uname`, p.`gid`,"
    'DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") `starting`, p.state `pstate`,'
    "(IFNULL(pu.`time`, 1) > IFNULL(pc.`time`, 0)) as `update` "
    "FROM project as `p`  left join `user` as `u` on p.uid = u.uid "
    "left join `project_check` as `pc` on p.pid = pc.pid "
    "AND pc.uid = %(uid)s "
    "left join `project_update` as `pu` on p.pid = pu.pid "
    'WHERE (p.`gid` = %(gid)s or "0" = %(gid)s '
    'or (p.`gid` = 100 and %(gid)s = "1")) and '
    "p.target like %(search)s and p.state != 1 "
    "ORDER BY {order} {sort} LIMIT %(start)s, %(step)s"
)

GET_PROJECT_LIST_GROUP_SEARCH_PREFETCHING = (
    "SELECT `pid`, `target` "
    "FROM project as `p` "
    "WHERE p.state != 1 "
    'and (p.`gid` = %(gid)s or "0" = %(gid)s '
    'or (p.`gid` = 100 and %(gid)s = "1")) and '
    "p.target like %(search)s "
    "ORDER BY `pid` desc LIMIT 0, 50"
)

PROJECT_CACHE = (
    "select UNIX_TIMESTAMP(time) `time` from project_update where pid = %(pid)s;"
)

PROJECT_IS_UPDATE = (
    "select IF((select ifnull(count(1), 0) as `f` from project_check"
    " WHERE uid = %(uid)s and pid = %(pid)s),"
    "(SELECT IF(pu.`time` > pc.`time`, 2, 1) as `update` "
    "FROM `project_check` as `pc` "
    "right join `project_update` as `pu` on pc.pid = pu.pid "
    "WHERE pu.`pid` = %(pid)s and pc.`uid` = %(uid)s),"
    "(SELECT if(count(1), 3, 4) FROM `project_update`"
    "WHERE `pid` = %(pid)s)) as `update`;"
)

GET_PROJECT_ALL = (
    "SELECT `pid`, `target`, `name`, `uid`, `gid`, "
    'DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") as `starting` '
    "FROM `project` ORDER BY {order} {sort} LIMIT %(start)s, %(step)s;"
)

GET_PROJECT_USER_COUNT = (
    "SELECT count(1) as `count` FROM `project` WHERE `uid` = %(uid)s and state != 1"
)

GET_PROJECT_GROUP_COUNT = (
    "SELECT count(1) as `count` FROM `project` "
    "WHERE `gid` = %(gid)s and state != 1 "
    'or "0" = %(gid)s or (gid = 100 and %(gid)s = "1")'
)

GET_PROJECT_GROUP_SEARCH_COUNT = (
    "SELECT count(1) as `count` FROM `project` "
    'WHERE state != 1 and (`gid` = %(gid)s or "0" = %(gid)s or '
    '(gid = 100 and %(gid)s = "1")) and `target` like %(search)s'
)

UPDATE_GET_PROJECT_TIMESTAMPS = (
    "INSERT INTO `project_check` (`pid`, `uid`) "
    "VALUES (%(pid)s, %(uid)s) ON DUPLICATE KEY UPDATE `time` = now();"
)

DELETE_PROJECT = (
    "update `project` set state = 1 WHERE `pid` = %(pid)s "
    'AND (`uid` = %(uid)s or "0" = %(gid)s);'
)

GET_SELECTOR_IP = (
    "select inet6_ntoa(ip)ip from ({selector}) r "
    "group by ip having count(ip) = %(count)s "
    "order by cast(CONV(hex(ip), 16, 10) as unsigned) asc "
)

SELECTOR_APP_PID = (
    "select inet6_ntoa(ip)ip,layer,app,count(ip)total "
    "from result_cms "
    "where pid = %(pid)s group by ip,app,layer order by total desc;"
)

SELECTOR_SERVICE_PID = (
    "select inet6_ntoa(ip)ip,server_type `type`,port,server_product `product` "
    "from result_port where pid = %(pid)s "
)

SELECTOR_HOST_PID = (
    "select inet6_ntoa(ip)ip,whois,country,vendor "
    "from result_host_collect where pid = %(pid)s"
)

SELECTOR_SERVICE_WEBCLASS_PID = (
    "select inet6_ntoa(ip)ip,server_product,count(1)total "
    "from result_port where pid = %(pid)s and server_type in ('http', 'https') "
    "group by ip,server_product;"
)

SELECTOR_SERVICE_SUBCLASS_PID = (
    "select inet6_ntoa(ip)ip,server_product,count(1)total "
    "from result_port where pid = %(pid)s and server_type = %(type)s "
    "group by ip,server_product;"
)

SELECTOR_SERVICE_VERSION_PID = (
    "select inet6_ntoa(ip)ip,count(1)total,`server_version` version "
    "from result_port "
    "where pid = %(pid)s and server_product = %(product)s "
    "group by ip,server_version;"
)

SELECTOR_SYSTEM_PID = (
    "select inet6_ntoa(ip)ip,`system` "
    "from result_host_collect where pid = %(pid)s and vendor = %(vendor)s;"
)
SELECTOR_DOMAIN_COUNT = (
    "select count(distinct record) `domain` from result_subdomain where pid = %(pid)s;"
)

SELECTOR_ASSOCIATE_LOOP_PID = (
    "select inet6_ntoa(`ip`)`ip`, subclass, count(1)total from ( "
    'select `ip`, "si" `subclass` from result_sql_injection where pid = %(pid)s '
    "union all select `ip`, \"al\" from result_wapp_loophole where pid = %(pid)s and status != '不存在漏洞' "
    'union all select `ip`, "wp" from result_service_blasting where pid = %(pid)s '
    'union all select `ip`, "al" from result_code_leakage where pid = %(pid)s '
    'union all select `ip`, "wp" from result_web_blasting where pid = %(pid)s)`r`'
    "group by ip,subclass"
)

SELECTOR_BASE_SQL = {
    "not": "select '' `ip` where 1=2 ",
    "apps": "select ip from result_recognition where pid = %(pid)s ",
    "port": "select ip from result_port where pid = %(pid)s ",
    "host": "select ip from result_host_collect where pid = %(pid)s ",
    "si": "select ip from result_sql_injection where pid = %(pid)s ",
    "wp": "select ip from result_service_blasting where pid = %(pid)s group by ip union all select ip from result_web_blasting where pid = %(pid)s ",
    "al": "select ip from result_wapp_loophole where pid = %(pid)s and status != '不存在漏洞' group by ip union all select ip from result_code_leakage where pid = %(pid)s ",
}

SELECTOR_CONDITION_SQL = {
    "other": ("", "not"),
    "sl": ("", "not"),
    "si": ("", "si"),
    "wp": ("", "wp"),
    "al": ("", "al"),
    "version": ("and server_version = %(version)s", "port"),
    "vendor": ("and vendor = %(vendor)s", "host"),
    "apps": ("and app = %(apps)s", "apps"),
    "http": ("and (server_type='http' or server_type='https')", "port"),
    "service": ("and server_type = %(service)s", "port"),
    "system": ("and `system` = %(system)s", "host"),
    "port": ("and port = %(port)s", "port"),
    "product": ("and server_product = %(product)s", "port"),
    "webserver": ("and server_product = %(webserver)s", "port"),
    "whois": ("and trim(whois) = %(whois)s", "host"),
    "ipv6": ("and length(ip) > 4", "host"),
    "ipv4": ("and ip like concat(unhex(%(ip_segment)s), '%%')", "host"),
    "country": ("and country = %(country)s", "host"),
}

GET_HOST_INFO = (
    "select inet6_ntoa(ip)`ip`,r.rid,asname,country,`system`,vendor,`whois`, "
    "concat(if(LENGTH(prefix)=2, '主站', '二级域名'), if(data->'$.option.segment','C段',''))`htype` "
    "from result_host_collect r join task t on r.tid = t.tid "
    "join task_tree tt on tt.id = t.tree_id "
    "where r.pid = %(pid)s "
    "order by cast(CONV(hex(ip), 16, 10) as unsigned) asc;"
)

GET_PORT_INFO = (
    "select inet6_ntoa(ip)`ip`,port,server_type,server_product,server_version "
    "from result_port where pid = %(pid)s;"
)

GET_SUBDOMAIN_INFO = (
    "select `value` `ip`,record "
    "from result_subdomain where pid = %(pid)s group by `value`, record;"
)

GET_ASSOCIATE_LOOP_IP = (
    "select inet6_ntoa(`ip`)`ip`, `level`, subclass from ( "
    'select `ip`, "high" `level`, "si" `subclass` from result_sql_injection where pid = %(pid)s '
    "union all select `ip`, `level`, \"al\" from result_wapp_loophole where pid = %(pid)s and status != '不存在漏洞' "
    'union all select `ip`,  "info", "wp" from result_service_blasting where pid = %(pid)s '
    'union all select `ip`,  "info", "wp" from result_web_blasting where pid = %(pid)s) `r` '
)

GET_HOST_CHILD_TID = (
    "SELECT t.tid, t.ttype from task t cross join task t2 on t2.tid = %(tid)s "
    "where t.pid = t2.pid and t.prefix like concat(t2.prefix, '_%%');"
)

GET_SITE_COUNT = "select count(1) `count` from result_site_collect where pid = %(pid)s"

GET_SITE_LIST = (
    "select scheme,inet6_ntoa(rsc.ip)`ip`,rsc.port,site,title,code,ico,rp.server_product,vendor,response, "
    "concat(if(LENGTH(prefix)=2, '主站', '二级域名'), if(data->'$.option.segment','C段',''))`htype` "
    "from result_site_collect rsc "
    "join result_port rp on rp.pid = rsc.pid and rp.port=rsc.port and rp.ip=rsc.ip  "
    "join result_host_collect rh on rsc.pid = rh.pid and rsc.ip=rh.ip "
    "join task t on t.tid = rh.tid "
    "join task_tree tt on tt.id = t.tree_id "
    "where rsc.pid = %(pid)s "
    "ORDER BY {order} {sort} LIMIT %(start)s, %(step)s"
)

GET_SINGLE_HOST_INFO = (
    "select inet6_ntoa(ip)`ip`,`name`,`country`,`city`,`whois`,`as`,"
    "`asname`,`loc`,`system`,`type`,`vendor`,`cdnvendor`,`iscdn`,pid "
    "from result_host_collect where rid = %(rid)s"
)

GET_TASK_OLD_DATA = (
    "select pid,parameter,ttype,ttype_id,rid,hex(prefix)prefix,tree_id,rely "
    "from task t where tid = %(tid)s"
)

GET_TASK_SUB_CONDITION = (
    "select hex(prefix) prefix, lft, rgt, t.pid "
    "from task t join task_tree tt on tt.id = t.tree_id "
    "where t.tid = %(tid)s and t.df = 0;"
)

GET_TASK_SUB_TASK = (
    "select hex(ts.eid) eid "
    "from task t join task_status ts on t.tid = ts.tid "
    "cross join task t1 on t1.tid = %(tid)s "
    "where t.pid = t1.pid and t.tid >= %(tid)s and "
    "t.prefix like unhex(concat(hex(t1.prefix), '25'));"
)

UPDATE_TASK_SUB_STATE = (
    "update task t join task_status ts on t.tid = ts.tid "
    "cross join task t1 on t1.tid = %(tid)s "
    "set ts.state = %(state)s, t.df = 1 "
    "where t.pid = t1.pid and t.tid >= %(tid)s and "
    "t.prefix like unhex(concat(hex(t1.prefix), '25'));"
)

# GET_TASK_SUB_TASK = (
#     "select t.tid, ttype, rid, bin_to_uuid(eid) `eid`,state, tree_id "
#     "from task t join task_tree tt on tt.id = t.tree_id "
#     "join task_status ts on ts.tid = t.tid "
#     'where t.pid = %(pid)s and prefix like concat(unhex(%(prefix)s), "%%") '
#     "and t.`pid` = %(pid)s AND `lft` >= %(lft)s AND `rgt` <= %(rgt)s "
#     'and t.df = 0 and (t.`uid` = %(uid)s or "0" = %(gid)s) ;'
# )
#
# DELETE_TASK_SUB_TASK = (
#     "update task `t` join task_tree tt on tt.id = t.tree_id "
#     "join task_status ts on ts.tid = t.tid set t.df = 1 "
#     'where  t.pid = %(pid)s and prefix like concat(unhex(%(prefix)s), "%%") '
#     "and t.`pid` = %(pid)s AND `lft` >= %(lft)s AND `rgt` <= %(rgt)s "
#     'and (`uid` = %(uid)s or "0" = %(gid)s) ;'
# )
#
# UPDATE_TASK_SUB_STATE = (
#     "update task `t` join task_tree tt on tt.id = t.tree_id "
#     "join task_status ts on ts.tid = t.tid set ts.state = %(state)s "
#     'where  t.pid = %(pid)s and prefix like concat(unhex(%(prefix)s), "%%") '
#     "and t.`pid` = %(pid)s AND `lft` >= %(lft)s AND `rgt` <= %(rgt)s "
#     'and (`uid` = %(uid)s or "0" = %(gid)s) ;'
# )

INSTALL_INIT_TASK = (
    "INSERT INTO `task` (parameter, ttype, pid, uid, rid, tree_id, prefix, rely) "
    "values (%(parameter)s, %(ttype)s, %(pid)s, %(uid)s, %(rid)s, "
    "%(tree_id)s, unhex(%(prefix)s), %(rely)s);"
)

INSTALL_INIT_TASK_STATE = (
    "INSERT INTO `task_status` (`pid`, `tid`, `eid`) "
    "values (%(pid)s, %(tid)s, uuid_to_bin(%(eid)s));"
)

DELETE_CERT = "DELETE FROM `certificate` WHERE `id` = %(id)s AND `uid` = %(uid)s ;"

INSERT_CERT = (
    "INSERT INTO `certificate` (`uid`, `name`, `cert`, `key`, `password`) "
    "VALUES (%(uid)s, %(name)s, %(cert)s, %(key)s, %(password)s);"
)

GET_USE_CERTIFICATES = "SELECT `id`, `name` FROM `certificate` WHERE `uid` = %(uid)s;"
GET_USE_CERTIFICATE = (
    "SELECT `cert` FROM `certificate` WHERE `id` = %(id)s AND `uid` = %(uid)s ;"
)

GET_PROJECT_INFO_FROM_TID = (
    "SELECT p.pid FROM project p join task t on p.pid = t.pid "
    'where tid = %(tid)s and (state != 1 or %(gid)s = "0" ) '
    'and (gid = %(gid)s or "0" = %(gid)s '
    'or (gid = 100 and %(gid)s = "1"))'
)

GET_PROJECT_INFO_FROM_RID = (
    "SELECT p.pid FROM project p join {} r on p.pid = r.pid "
    'where rid = %(rid)s and (state != 1 or %(gid)s = "0" ) '
    'and (gid = %(gid)s or "0" = %(gid)s '
    'or (gid = 100 and %(gid)s = "1"))'
)

GET_PROJECT_INFO = (
    'SELECT `target`, `name`, DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") '
    "as `starting` FROM project "
    'where pid = %(pid)s and (state != 1 or %(gid)s = "0" ) '
    'and (gid = %(gid)s or "0" = %(gid)s '
    'or (gid = 100 and %(gid)s = "1"))'
)

GET_PROJECT_ALL_TASK = (
    'SELECT tid, IFNULL(parameter->"$.segment", False) as `segment`, '
    "ttype, rid FROM task where pid = %(pid)s and df = 0;"
)

GET_PROJECT_TYPE_TASK = (
    'SELECT tid, IFNULL(parameter->"$.segment", False) as `segment`, '
    "ttype, rid FROM task where pid = %(pid)s and ttype = %(ttype)s and df = 0;"
)

GET_PROJECT_GEXF_TASK = (
    "SELECT t.tid, ttype, t.rid, state, rely "
    "FROM task t join task_status ts on t.tid = ts.tid "
    "where t.pid = %(pid)s and df = 0"
)

GET_PROJECT_GEXF_WORDPRESS_LOOP = (
    "select rid,tid,concat(title, '(cve', cve, ')') `value` "
    "from result_wordpress_loop where pid = %(pid)s "
)

GET_PROJECT_GEXF_SUBDOMAIN = (
    "select rid,tid,concat(record, if(`type` != 'A', concat('|', `value`), '')) `value` "
    "from result_subdomain where pid = %(pid)s "
)

GET_PROJECT_GEXF_HOST_COLLECT = (
    "select rid,tid,concat(inet6_ntoa(ip), ' (',`vendor`, ')') `value` "
    "from result_host_collect where pid = %(pid)s "
)

GET_PROJECT_GEXF_PORT = (
    "select rid,tid,concat(port, ' (',`server_type`, ')') `value` "
    "from result_port where pid = %(pid)s "
)

GET_PROJECT_GEXF_SERVICE_BLASTING = (
    "select tid,rid,concat(service, '[',username, ':',password, ']') `value` "
    "from result_service_blasting where pid = %(pid)s ;"
)

GET_PROJECT_GEXF_SITE_COLLECT = (
    "select rid,tid,concat('[', code, '] ',site, ' (',`title`, ')') `value` "
    "from result_site_collect where pid = %(pid)s "
)

GET_PROJECT_GEXF_WAF_IDENTIFICATION = (
    "select rid,tid,waf `value` from result_waf_identification where pid = %(pid)s "
)

GET_PROJECT_GEXF_RECOGNITION = (
    "select rid,tid,trim(BOTH '/' FROM concat(app,'/',version)) `value` "
    "from result_recognition where pid = %(pid)s "
)

GET_PROJECT_GEXF_WAPP_LOOPHOLE = (
    "select rid,tid,concat(name, '->',status) `value` "
    "from result_wapp_loophole where pid = %(pid)s "
)

GET_PROJECT_GEXF_WEB_BLASTING = (
    "select rid,tid,concat(path, ' [',username, ':',password, ']') `value` "
    "from result_web_blasting where pid = %(pid)s "
)

GET_PROJECT_GEXF_EXHAUSTION_SPIDER = (
    "select rid,tid,concat('[', code, '] ',path) `value` "
    "from result_exhaustion_spider where pid = %(pid)s "
)

GET_PROJECT_GEXF_CHAIN_SPIDER = (
    "select rid,tid, concat('[', method, '] ',path) `value` "
    "from result_chain_spider where pid = %(pid)s "
)

GET_PROJECT_GEXF_SQL_INJECTION = (
    "select rid,tid,concat(attr, '->' , `user`) `value` "
    "from result_sql_injection where pid = %(pid)s "
)

GET_PROJECT_GEXF_DUMPS = (
    "select rid,tid,concat(user, '[', basedb, ']') `value` "
    "from result_dumps where pid = %(pid)s "
)

GET_PROJECT_EARTH_TID = (
    "select tid, hex(mrid) rid from task where pid = %(pid)s and "
    "ttype in ('subdomain', 'host_collect', 'port', 'site_collect');"
)

GET_PROJECT_EARTH_SUB = (
    "select rid id, record from result_subdomain r where pid = %(pid)s"
)

GET_PROJECT_EARTH_HOST = (
    "select t.rid, r.rid id, inet6_ntoa(ip) ip, r.system, cdnvendor "
    "from result_host_collect r left join task t on t.tid = r.tid "
    "where r.pid = %(pid)s"
)

GET_PROJECT_EARTH_PORT = (
    "select t.rid, r.rid id, port, "
    'if(server_product != "", server_product,server_type) server '
    "from result_port r left join task t on t.tid = r.tid "
    'where r.pid = %(pid)s and t.ttype = "port"'
)

GET_PROJECT_EARTH_SITE = (
    "select t.rid,site_url(scheme,site,port,'/')site, title "
    "from result_site_collect r left join task t on t.tid = r.tid "
    'where r.pid = %(pid)s and t.ttype= "site_collect" '
)

GET_PROJECT_ALL_TASK_TID = (
    'SELECT ttype, concat("(", group_concat(tid), ")") tids FROM task '
    "WHERE pid = %(pid)s and df = 0 group by ttype;"
)

GET_CONCAT_CMS_RESULT = (
    "SELECT max(rid) `rid`, tid, `site` `站点`, ip_url(scheme,ip,port,'/') `主机`, "
    " group_concat(concat(`app`, if(`version`, concat('/', version), ''))) `应用` "
    "FROM result_recognition left join library_cms_filter l on name = app  "
    "where tid in {tids} and (ifnull(level, 127) & 32) != 0 group by tid, site,`主机`;"
)

GET_PROJECT_TTYPE_RESULT = (
    "SELECT rid, tid, {key} FROM `result_{type}` "
    "WHERE rid > %(rid)s and tid in {tids}"
)

GET_IP_POSITION = (
    "select country, province, city, district, wgs_lon, wgs_lat from ipv4_position "
    "WHERE minip <= INET_ATON(%(ip)s) ORDER BY minip DESC LIMIT 1;"
)

RESULT_SUBDOMAIN = (
    'SELECT concat("subdomain-",rid) as `id`, record as `记录`, process '
    "as `解析过程`, `value` as `记录值` FROM result_subdomain "
    "where tid = %(tid)s;"
)

RESULT_HOST_COLLECT = (
    'SELECT concat("host_collect-",rid) as `id`, inet6_ntoa(`ip`) '
    "as `ip`, `country` as `国家`, `whois`, `asname` as `自治域`, `system` "
    "as `系统`, `type` as `系统类型`, `vendor` as `供应商` "
    "FROM result_host_collect  where tid = %(tid)s order by `ip` ;"
)

RESULT_PORT = (
    'SELECT concat("port-",rid) as `id`, inet6_ntoa(`ip`) as `ip`, `port` '
    "as `端口`, `server_type` as `服务类型`, `server_product` "
    "as `服务产品`, `server_version` as `服务版本`, `additional` as `其他信息` F"
    "ROM result_port where tid = %(tid)s;"
)

RESULT_SITE_COLLECT = (
    'SELECT concat("site_collect-",rid)`id`, inet6_ntoa(`ip`)`ip`,`scheme` `协议`,`port` `端口`, '
    "`site`, `title` `标题`, `ico` as `图标哈希`, `code` as `响应码` "
    "FROM result_site_collect where tid = %(tid)s;"
)

RESULT_WAF_IDENTIFICATION = (
    'SELECT concat("waf_identification-",rid) as `id`, inet6_ntoa(`ip`)`ip`,`scheme` `协议`,'
    "`port` `端口`, `site`, `waf` "
    "FROM result_waf_identification where tid = %(tid)s;"
)

RESULT_CHAIN_SPIDER = (
    'SELECT concat("chain_spider-",rid) `id`,site_url(scheme,site,port,path)`统一资源定位符`, '
    "`method` `请求方法`, `data` `负载`, `params` `参数` "
    "FROM result_chain_spider where tid = %(tid)s;"
)

RESULT_RECOGNITION = (
    'SELECT concat("recognition-",rid) `id`, inet6_ntoa(`ip`)`ip`,`scheme` `协议`,`port` `端口`, '
    '`site`, `app` `应用`, ifnull(`color`, "") `color`, ifnull(ctype,"") 类型 '
    "FROM result_recognition left join library_cms_filter on `name` = app "
    "where tid = %(tid)s and (ifnull(level, 127) & %(bit)s) != 0;"
)

RESULT_WAPP_LOOPHOLE = (
    'SELECT concat("wapp_loophole-",rid) `id`,`name` `漏洞名`, inet6_ntoa(`ip`)`ip`,`scheme` `协议`,'
    "`port` `端口`, `site` , `level` as `风险等级`, `type` as `漏洞类型`, `status` as `状态` "
    "FROM result_wapp_loophole where tid = %(tid)s and status != '不存在漏洞';"
)

RESULT_DUMPS = (
    'SELECT concat("dumps-",rid) as `id`, `netloc` as `站点`, `user` as `用户`, '
    "`basedb` as `当前库`, `db` as `导出库`, `dbs` as `所有库`, `table` as `当前表`, "
    "`tables` as `所有表`, `column` as `字段`, `data` as `展示数据` "
    "FROM result_dumps where tid = %(tid)s;"
)

RESULT_SERVICE_BLASTING = (
    'SELECT concat("service_blasting-",rid) as `id`, inet6_ntoa(`ip`) '
    "as `ip` , `port` as `端口`, `service` as `服务`, `username` "
    "as `用户名`, `password` as `密码` "
    "FROM result_service_blasting where tid = %(tid)s;"
)

RESULT_EXHAUSTION_SPIDER = (
    'SELECT concat("exhaustion_spider-",rid) `id`, inet6_ntoa(`ip`)`ip`,`scheme` `协议`,'
    "`port` `端口`, `site`, `path` `文件`, `code` `响应码`, `size` `大小` "
    "FROM result_exhaustion_spider where tid = %(tid)s "
    "order by `code`;"
)

RESULT_CODE_LEAKAGE = (
    'SELECT concat("code_leakage-",rid) as `id`, `number` `文件数`,`size` `文件大小`,`fileid` '
    "FROM result_code_leakage where tid = %(tid)s;"
)
GET_PROJECT_USERINFO = (
    "select itype,value,other from result_userinfo where pid = %(pid)s"
)

# GET_HOST_RESULT_DUMPS = "select * from result_dumps where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
# GET_HOST_RESULT_FILE_CONTAINS = "select * from result_file_contains where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
# GET_HOST_RESULT_INSTRUCTION_EXECUTION = "select * from result_instruction_execution where pid = %(pid)s and ip = inet6_aton(%(ip)s)"

GET_HOST_RESULT_WEB_SHELL = (
    "select concat('web_shell-', id) rid, uri, "
    'DATE_FORMAT(`time`, "%%Y/%%c/%%e %%T") as time '
    "from project_web_shell where pid = %(pid)s  and ip = inet6_aton(%(ip)s);"
)

GET_HOST_RESULT_USERINFO = "select concat('userinfo-', uiid) rid, itype, value, other from result_userinfo where pid = %(pid)s;"

GET_PORJECT_ALL_RESULT_TTYPE = "select distinct ttype from task where pid = %(pid)s and parameter->'$.target.ip' = %(ip)s"
GET_HOST_RESULT_HOST_COLLECT = (
    "select `rid`,name,city,country,whois,`as`,asname,loc,`system`,vendor,cdnvendor "
    "from result_host_collect where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
)
GET_HOST_RESULT_WORDPRESS_LOOP = (
    "select concat('wordpress_loop-', rid)`rid`,port,site,title,fixed_in,cve "
    "from result_wordpress_loop where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
)
GET_HOST_RESULT_CODE_LEAKAGE = (
    "select concat('code_leakage-', rid)`rid`,port,site,`number`,`size`,fileid "
    "from result_code_leakage where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
)
GET_HOST_RESULT_SUBDOMAIN = (
    "select distinct record from result_subdomain "
    "where pid = %(pid)s and value = %(ip)s"
)
GET_HOST_RESULT_EXHAUSTION_SPIDER = (
    "select concat('exhaustion_spider-', rid)`rid`,port,site,path,code,`size`,scheme,title "
    "from result_exhaustion_spider where pid = %(pid)s and ip = inet6_aton(%(ip)s) "
    "union all select concat('chain_spider-', any_value(rid))`rid`,any_value(port),any_value(site),"
    "path,'200' `core`,'0' `size`,any_value(scheme),'' `title` "
    "from result_chain_spider where pid = %(pid)s and ip = inet6_aton(%(ip)s) group by path;"
)
GET_HOST_RESULT_PORT = (
    "select concat('port-', rid)`rid`,port,server_type,server_product,server_version "
    "from result_port where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
)
GET_HOST_RESULT_RECOGNITION = (
    "select concat('recognition-', rid)`rid`,port,site,app,version,scheme,"
    "layer,classification "
    "from result_cms where pid = %(pid)s and ip = inet6_aton(%(ip)s);"
)
GET_HOST_RESULT_SERVICE_BLASTING = (
    "select concat('service_blasting-', rid)`rid`,port,service,username,password "
    "from result_service_blasting where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
)
GET_HOST_RESULT_SITE_COLLECT = (
    "select concat('site_collect-', rid)`rid`,port,site,title,code,ico,alias,response "
    "from result_site_collect where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
)
GET_HOST_RESULT_SQL_INJECTION = (
    "select concat('sql_injection-', rid)`rid`,method,port,scheme,site,path,"
    "params,data,sep,injection,attr,ikey,%(ip)s `ip`,`db`,`user` "
    "from result_sql_injection where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
)
GET_HOST_RESULT_WAF_IDENTIFICATION = (
    "select concat('waf_identification-', rid)`rid`,port,site,waf from result_waf_identification "
    "where pid = %(pid)s and ip = inet6_aton(%(ip)s) and waf != 'NOT'"
)
GET_HOST_RESULT_WAPP_LOOPHOLE = (
    "select concat('wapp_loophole-', rid)`rid`,port,scheme,site,`name`,level,`type` "
    "from result_wapp_loophole "
    "where pid = %(pid)s and ip = inet6_aton(%(ip)s) and status != '不存在漏洞' "
)
GET_HOST_RESULT_WEB_BLASTING = (
    "select concat('web_blasting-', rid)`rid`,port,scheme,site,path,username,password "
    "from result_web_blasting where pid = %(pid)s and ip = inet6_aton(%(ip)s)"
)
GET_TASK_PARENT_FROM_RID = (
    "select t.rid, r.tid, ttype, parameter->'$.target' `target` "
    "from task t join {} r on t.tid = r.tid where r.rid = %(rid)s;"
)

"""
CREATE FUNCTION site_url(scheme varchar(10), site varchar(255), port int, path text)
RETURNS text
RETURN(SELECT concat(scheme,"://",site,if((scheme='http'&&port=80)||(scheme='https'&&port=443),"",concat(":", port)),"/",TRIM(LEADING "/" FROM path)));

CREATE FUNCTION ip_url(scheme varchar(10), ip varbinary(16), port int, path text)
RETURNS text
RETURN(SELECT concat(scheme,"://",INET6_NTOA(ip),if((scheme='http'&&port=80)||(scheme='https'&&port=443),"",concat(":", port)),"/",TRIM(LEADING "/" FROM path)));
"""

RESULT_SQL_INJECTION = (
    'SELECT concat("sql_injection-",rid)`id`,  inet6_ntoa(`ip`)`ip`,`scheme` `协议`,`port` '
    "`端口`, `site` , `method` `请求方法`, `data` `负载`, `params` `参数`, `sep` `闭合符`, "
    "`injection` `注入结构`, `attr` `参数类型`,`ikey` `传参点` "
    "FROM result_sql_injection where tid = %(tid)s;"
)

RESULT_INSTRUCTION_EXECUTION = (
    'SELECT concat("instruction_execution-",rid) as `id`, '
    "`url` as `统一资源定位符`, `method` as `请求方法`, `data` as `负载`"
    ", `params` as `参数`, `platform` as `平台`, `payload` as `攻击负载`"
    ", `attr` as `参数类型`, `ikey` as `传参点`, `check` as `响应` "
    "FROM result_instruction_execution where tid = %(tid)s;"
)

RESULT_FILE_CONTAINS = (
    'SELECT concat("file_contains-",rid) as `id`, `url` as `统一资源定位符`,'
    " `method` as `请求方法`, `data` as `负载`, `params` as `参数`,"
    " `platform` as `平台`, `payload` as `攻击负载`, `attr` as `参数类型`,"
    " `ikey` as `传参点` "
    "FROM result_file_contains where tid = %(tid)s;"
)

RESULT_WEB_BLASTING = (
    'SELECT concat("web_blasting-",rid) as `id`, inet6_ntoa(`ip`)`ip`,`scheme` '
    "`协议`,`port` `端口`, `site` ,`title` `标题`, `username` `用户名`, `password` `密码` "
    "FROM result_web_blasting where tid = %(tid)s;"
)

RESULT_WORDPRESS_LOOP = (
    'SELECT concat("wordpress_loop-",rid) `id`, `title`, '
    "`fixed_in` `版本`, `cve`, `wpvulndb` `漏洞编号` "
    "FROM result_wordpress_loop where tid = %(tid)s;"
)

GET_SUBDOMAIN_LIST = (
    "select record, `value` `host` " "from result_subdomain where pid = %(pid)s;"
)

GET_HOST_LIST = (
    "select `tid`, inet6_ntoa(ip) ip,`country`,`city`,`whois`,"
    "`as`,`asname`,`loc`,`system`,`vendor`,iscdn,cdnvendor "
    "from result_host_collect where pid = %(pid)s;"
)

GET_PORT_LIST = (
    "select `tid`, inet6_ntoa(ip) `ip`, `port`, `server_type` "
    "from result_port where pid = %(pid)s;"
)

GET_APP_LIST = (
    "select `tid`, `site`, `app`, `version`, ifnull(`color`, '') color "
    "from result_recognition r "
    "left join library_cms_filter l on name = app  "
    "where pid = %(pid)s AND (ifnull(level, 127) & 64) != 0;"
)

GET_PROJECT_ALL_TASK_STATE = (
    "select b.pid `pid`, b.tid `tid`, b.nid `nid`, bin_to_uuid(b.eid) `eid`, "
    "b.state `state`, `ttype` "
    "from task as a left join task_status as b on a.tid = b.tid "
    "where b.pid = %(pid)s and a.df = 0"
)

GET_PROJECT_TASK_EID = (
    "select bin_to_uuid(eid) `eid`,state from task_status where tid = %(tid)s"
)

GET_PROJECT_ALL_EID = (
    "select bin_to_uuid(eid) `eid`,state from task_status where pid = %(pid)s"
)

GET_PROJECT_TASK_STATE_COUNT = (
    "SELECT pid, case "
    "  WHEN state in (-1, -3) THEN 'notstart' "
    "  WHEN state in (-2, -4, -6, -7) THEN 'end' "
    "  WHEN state in (-5) THEN 'del' "
    'ELSE "run" END `s`,  count(1) num FROM task_status '
    "where pid = %(pid)s GROUP BY s;"
)

GET_PROJECT_TASK_STATE_COUNTS = (
    "SELECT ts.pid, case "
    "  WHEN state in (-3) THEN 'notstart' "
    "  WHEN state in (-2, -4, -6, -7) THEN 'end' "
    "  WHEN state in (-5) THEN 'del' "
    'ELSE "run" END `s`, count(1) num '
    "FROM task_status ts "
    "WHERE ts.pid in ({pid})"
    "GROUP BY s, pid;"
)

GET_FUCK_PROJECT_TASK_STATE_COUNTS = (
    "SELECT ts.pid, case "
    "  WHEN state in (-1, -3) THEN 'notstart' "
    "  WHEN state in (-2, -4, -6, -7) THEN 'end' "
    "  WHEN state in (-5) THEN 'del' "
    'ELSE "run" END `s`, count(1) num '
    "FROM task_status ts "
    "inner join fuck_project f on f.pid = ts.pid "
    "where f.fid = %(fid)s "
    "GROUP BY s, pid order by pid desc;"
)

UPDATE_TASK_STATE = "update task_status set state = %(state)s where tid = %(tid)s"

UPDATE_PROJECT_ALL_TASK_STATE = (
    "update task_status set state = %(state)s where pid = %(pid)s and state != -2"
)

ASSOCIATE_INFO = (
    "select 'subdomain' ttype, count(1) count "
    "   from result_subdomain where pid = %(pid)s "
    "union all select 'host_collect' ttype, count(1) count "
    "   from result_host_collect where pid = %(pid)s "
    "union all select 'port' ttype, count(1) count "
    "   from result_port where pid = %(pid)s "
    "union all select 'site_collect' ttype, count(1) count "
    "   from result_site_collect where pid = %(pid)s "
)

GET_ASSOCIATE_LOOP_IP_TYPE = (
    'select "si" itype, "sql_injection" `name`, inet6_ntoa(ip) ip'
    "   from result_sql_injection r join task t on t.tid = r.tid where pid = %(pid)s "
    'union all select "wa" itype, "wapp_loophole" `name`, inet6_ntoa(ip) ip '
    "   from result_wapp_loophole r join task t on t.tid = r.tid where pid = %(pid)s and status != '不存在漏洞' "
    'union all select "sl" itype, "service_blasting" `name`, inet6_ntoa(ip) ip '
    "   from result_service_blasting r join task t on t.tid = r.tid where pid = %(pid)s "
    'union all select "wp" itype, "web_blasting" `name`, inet6_ntoa(ip) ip '
    "   from result_web_blasting r join task t on t.tid = r.tid where pid = %(pid)s "
)

GET_ASSOCIATE_LOOP = (
    "select %(pid)s `pid`, `level`, count(1) `total` from ( "
    'select "high" as level from result_sql_injection where pid = %(pid)s '
    'union all select "medium" level from result_file_contains where pid = %(pid)s '
    'union all select "medium" level from result_instruction_execution where pid = %(pid)s '
    "union all select `level` level from result_wapp_loophole where pid = %(pid)s and status != '不存在漏洞' "
    'union all select "info" level from result_service_blasting where pid = %(pid)s '
    'union all select "info" level from result_web_blasting where pid = %(pid)s '
    'union all select "info" level from result_code_leakage where pid = %(pid)s ) as `r` '
    "group by `level`;"
)

GET_ASSOCIATE_LOOPS = (
    "select `pid`, `level`, count(1) `total` from ( "
    'select `pid`, "high" level from result_sql_injection where pid in ({pid})  '
    'union all select `pid`, "medium" level from result_file_contains where pid in ({pid})  '
    'union all select `pid`, "medium" level from result_instruction_execution where pid in ({pid}) '
    "union all select `pid`, `level` from result_wapp_loophole where pid in ({pid}) and status != '不存在漏洞' "
    'union all select `pid`, "info" level from result_service_blasting where pid in ({pid})  '
    'union all select `pid`, "info" level from result_web_blasting where pid in ({pid}) '
    'union all select `pid`, "info" level from result_code_leakage where pid in ({pid})  ) as `r` '
    "group by `level`, `pid`;"
)

GET_FUCK_ASSOCIATE_LOOPS = (
    "select r.`pid`, `level`, count(1) `total` from ( "
    'select `pid`, "high" level from result_sql_injection '
    'union all select `pid`, "medium" level from result_file_contains '
    'union all select `pid`, "medium" level from '
    "result_instruction_execution "
    "union all select `pid`, `level` from result_wapp_loophole where status != '不存在漏洞'"
    'union all select `pid`, "info" level from result_service_blasting '
    'union all select `pid`, "info" level from result_web_blasting '
    'union all select `pid`, "info" level '
    "from result_code_leakage ) as `r` "
    "inner join fuck_project f on f.pid = r.pid "
    "where f.fid = %(fid)s group by `level`, `pid`;"
)

GET_VULNERABILITY_TOP = (
    'select concat("{name}-", r.rid) `id`, t.`starting`, t.tid, '
    "p.target, p.uid, p.pid "
    "from `task` as t "
    "right join `result_{name}` as r on t.tid = r.tid "
    "left join `project` as p on p.pid = t.pid and p.state != 1 "
    "where p.gid = %(gid)s or 0 = %(gid)s and "
    't.ttype = "{name}" and t.df = 0 '
    "order by t.`starting` desc limit 20"
)

GET_PROJECT_UPDATE_TIME = (
    "select UNIX_TIMESTAMP(`time`) as t " "from project_update where pid = %(pid)s;"
)

# -------------------------------- this user manager --------------------------------------

UPDATE_USER_EMAIL = "update `user` set `email` = %(email)s where `uid` = %(uid)s;"
EMAIL_EXIST = "select 1 from `user` where `email` = %(email)s limit 1;"

# -------------------------------- manager --------------------------------------

SEARCH_CMS_LIST = "select id, name from library_cms where name like %(search)s"

GET_CMS_NUM = "select count(1) as total from library_cms;"
UPDATE_CMS_RESULT = "update result_recognition set app = %(name)s where app_id = %(id)s"
DELETE_CMS = "delete from library_cms where id = %(id)s"

GET_CMS_ID = (
    "select name,description,website,matches,`condition`,implies,excludes,layer,classification "
    "from library_cms where id = %(id)s"
)
GET_CMS_LIST = "select * from library_cms limit %(start)s, %(step)s;"

GET_CMS_LIST_SEARCH = (
    "select * from library_cms where name like %(search)s limit %(start)s, %(step)s;"
)

UPDATE_CMS = "update library_cms set {} where id = %(id)s"

INSERT_CMS = (
    "insert into library_cms "
    "(name, `description`, `website`, `matches`, `condition`, "
    " `implies`,`excludes`, `layer`, `classification`) "
    "VALUES (%(name)s, %(description)s, %(website)s, %(matches)s, %(condition)s, "
    " %(implies)s, %(excludes)s, %(layer)s, %(classification)s)"
)

GET_ALL_GROUP = "select `gid`, `name` from `group` order by gid asc;"

GET_GROUPS = (
    "select `gid`, `name`, `admin`, "
    'DATE_FORMAT(`create_time`, "%%Y/%%c/%%e %%T") as `create_time` '
    "from `group` order by gid asc limit %(start)s, %(step)s;"
)

GET_GROUP_COUNT = "select count(1) as `count` from `group`"


SEARCH_GROUPS = {
    "subject_sql": 'select `gid`, `name`, `admin`, DATE_FORMAT(`create_time`, "%%Y/%%c/%%e %%T") as `create_time` from `group`',
    "sort_sql": " order by gid asc limit %(start)s, %(step)s;",
}

SEARCH_GROUP_COUNT = {"subject_sql": "select count(1) as `count` from `group`"}


INSERT_GROUP = "insert into `group` (`name`, `admin`) value (%(name)s, %(admin)s);"

GROUP_EXIST = "select 1 from `group` where gid = %(gid)s;"

GROUP_NAME_EXIST = "select 1 from `group` where name = %(name)s;"

UPDATE_GROUP_NAME = "update `group` set `name` = %(name)s;"

DELETE_GROUP = "delete from `group` where `gid` = %(gid)s and `admin` = %(uid)s;"

GET_USERS = (
    "select `uid`, `name`, `email`, `gid`, `state`,  "
    'DATE_FORMAT(`create_time`, "%%Y/%%c/%%e %%T") as `create_time`, `old_time`, '
    "`lip`, not ISNULL(`otpkey`) as `otp` from `user` "
    "order by uid asc limit %(start)s, %(step)s;"
)

SEARCH_USERS = {
    "subject_sql": 'select `uid`, `name`, `email`, `gid`, `state`, DATE_FORMAT(`create_time`, "%%Y/%%c/%%e %%T") as `create_time`, `old_time`,`lip`, not ISNULL(`otpkey`) as `otp` from `user` ',
    "sort_sql": " order by uid asc limit %(start)s, %(step)s;",
}

GET_USER_COUNT = "select count(1) as `count` from `user`"

SEARCH_USER_COUNT = {"subject_sql": "select count(1) as `count` from `user`"}


INSERT_USER = (
    "insert into `user` (`name`, `password`, `email`, `gid`, `state`) "
    "value (%(name)s, %(pswd)s, %(email)s, %(gid)s, 1);"
)

USER_EXIST = "select 1 from `user` where  `name` = %(name)s or `email` = %(email)s;"

UPDATE_USER_GID = "update `user` set `gid` = %(gid)s where `uid` = %(uid)s;"
UPDATE_USER_DOTP = 'update `user` set `otpkey` = "" where `uid` = %(uid)s;'
UPDATE_USER_STATE = "update `user` set `state` = not `state` where `uid` = %(uid)s;"
UPDATE_USER_PASSWORD = (
    "update `user` set `password` = %(password)s where `uid` = %(uid)s;"
)

DELETE_USER = "delete from `user` where `uid` = %(uid)s and `gid` != 0;"

GET_LIBRARY_APPLICATION_IDENTIFY = (
    "select `id`,`application`,`path`,`parameter`,"
    "`headers`, `body`,`special`, `hash` "
    "from `library_application_identify` "
    "order by id asc limit %(start)s, %(step)s;"
)

GET_LIBRARY_SERVICE_BLASTING = (
    "select `id`, `server`, need_user, usernames, "
    "to_base64(script) `script` "
    "from `library_service_blasting` "
    "order by id asc limit %(start)s, %(step)s;"
)

GET_LIBRARY_WAPP_BLASTING = (
    "select `id`, `app_id`, `app`, usernames, passwords, "
    "to_base64(script) `script`, dependent "
    "from `library_wapp_blasting` "
    "order by id asc limit %(start)s, %(step)s;"
)

GET_LIBRARY_URL_POLLUTION = (
    "select `id`, `name`, `type`, `level`, `position`, `clear`, "
    "`payload`, `criteria` "
    "from `library_url_pollution` "
    "order by id asc limit %(start)s, %(step)s;"
)

GET_LIBRARY_WAPP_POC = (
    "select `id`, `name`, to_base64(`poc`) `poc`, `app`, `type`, `level`, `dependent` "
    "from `library_wapp_poc` order by id asc limit %(start)s, %(step)s;"
)

GET_LIBRARY_DUMPS_LIST = (
    "select `id`, `gid`, `type`, `value` "
    "from `library_dumps_list` order by id asc limit %(start)s, %(step)s;"
)

GET_LIBRARY_NUM = "select count(1) as `count` from `{}`"

UPDATE_LIBRARY_APPLICATION_IDENTIFY = (
    "update `library_application_identify` "
    "set `application` = %(application)s,`path` = %(path)s,`"
    "parameter` = %(parameter)s,`headers` = %(headers)s,`"
    "body` = %(body)s,`special` = %(special)s,"
    "`hash` = %(hash)s where `id` = %(id)s"
)

UPDATE_LIBRARY_SERVICE_BLASTING = (
    "update `library_service_blasting` "
    "set `server` = %(server)s, `need_user` = %(need_user)s, "
    "`usernames` = %(usernames)s, `script` = from_base64(%(script)s) "
    "where `id` = %(id)s"
)

UPDATE_LIBRARY_WAPP_BLASTING = (
    "update `library_wapp_blasting` "
    "set `app_id` = %(app_id)s, `app` = %(app)s, "
    "`usernames` = %(usernames)s, `passwords` = %(passwords)s,"
    "`script` = from_base64(%(script)s), `dependent` = %(dependent)s "
    "where `id` = %(id)s"
)

UPDATE_LIBRARY_URL_POLLUTION = (
    "update `library_url_pollution` "
    "set `name` = %(name)s,`type` = %(type)s,`level` = %(level)s,"
    "`position` = %(position)s,`clear` = %(clear)s,"
    "`payload` = %(payload)s,`criteria` = %(criteria)s "
    "where `id` = %(id)s"
)

UPDATE_LIBRARY_WAPP_POC = (
    "update `library_wapp_poc` "
    "set `poc` = from_base64(%(poc)s),`app` = %(app)s,`type` = %(type)s,"
    "`level` = %(level)s, `name` = %(name)s, `dependent` = %(dependent)s where `id` = %(id)s"
)

UPDATE_LIBRARY_DUMPS_LIST = (
    "update `library_dumps_list` "
    "set `gid` = %(gid)s,`type` = %(type)s,`value` = %(value)s "
    "where `id` = %(id)s"
)

INSERT_LIBRARY_APPLICATION_IDENTIFY = (
    "insert into `library_application_identify` (`application`,"
    "`path`,`parameter`,`headers`,`body`,`special`,`hash`) "
    "value (%(application)s,%(path)s,%(parameter)s,"
    "%(headers)s,%(body)s,%(special)s,%(hash)s);"
)

INSERT_LIBRARY_SERVICE_BLASTING = (
    "insert into `library_service_blasting` (`server`,"
    " `need_user`, `usernames`, `script`) "
    "value (%(server)s, %(need_user)s, "
    "%(usernames)s, from_base64(%(script)s));"
)

INSERT_LIBRARY_WAPP_BLASTING = (
    "insert into `library_wapp_blasting` (`app_id`,"
    " `app`, `usernames`, `passwords`, `script`, `dependent`) "
    "value (%(app_id)s, %(app)s, "
    "%(usernames)s, %(passwords)s, from_base64(%(script)s), %(dependent)s );"
)

INSERT_LIBRARY_URL_POLLUTION = (
    "insert into `library_url_pollution` "
    "(`name`,`type`,`level`,`position`,`clear`,`payload`,`criteria`) "
    "value (%(name)s,%(type)s,%(level)s,%(position)s,%(clear)s,"
    "%(payload)s,%(criteria)s);"
)

INSERT_LIBRARY_WAPP_POC = (
    "insert into `library_wapp_poc` (`name`,`poc`,`app`,`type`,`level`, `dependent`) "
    "value (%(name)s,from_base64(%(poc)s),%(app)s,%(type)s,%(level)s,%(dependent)s);"
)

INSERT_LIBRARY_DUMPS_LIST = (
    "insert into `library_dumps_list` (`gid`,`type`,`value`) "
    "value (%(gid)s,%(type)s,%(value)s);"
)

DELETE_LIBRARY_LID = "delete from `{}` where `id` = %(id)s"

GET_NODE_STATE = (
    "select cpu,diskBytesRead,diskBytesWrite,diskusage,inodesusage,memoryusage,"
    "netBytesRecv,netBytesSent,taskName,`time` "
    "from `node_state` where nid = %(nid)s and `time` > UNIX_TIMESTAMP()-14400 "
    "order by nsid desc limit 240"
)

INSERT_NODE = (
    "insert into `node` (node_name,node_ip,node_gid,node_mode,`queue`,`remarks`) "
    "value (%(node_name)s,%(node_ip)s,%(node_gid)s,%(node_mode)s,%(queue)s,%(remarks)s);"
)

GET_NODE_COUNTRY = (
    "select areacode from ipv4_position "
    "WHERE minip <= INET_ATON(%(ip)s) ORDER BY minip DESC LIMIT 1;"
)

GET_GROUP_NODE = (
    "select node_name, node_ip, node_mode, creation, remarks "
    "from node where node_gid = %(gid)s;"
)

GET_TASK_STATE = "select tid, state from task_status where eid = uuid_to_bin(%(eid)s);"

GET_ALL_NODE = "select node_name, node_ip, node_mode, creation, remarks from node;"

GET_NODE_QUEUE = "select node_name,queue,node_mode from node;"

GET_NODE_COUNT = "select count(1) `count` from node; "

GET_NODE_MANAGER = (
    "select nid, node_name, node_ip, node_mode, "
    'queue, DATE_FORMAT(`creation`,"%%Y/%%c/%%e %%T") creation, remarks '
    "from node limit %(start)s, %(step)s;"
)

GET_NODE_SEARCH_MANAGER = {
    "not_a_state": "select nid, node_name, node_ip, node_mode, queue, "
    'DATE_FORMAT(`creation`,"%%Y/%%c/%%e %%T") creation, remarks '
    "from node where {key} like %(search)s limit %(start)s, %(step)s;",
    "yes_state": "select nid, node_name, node_ip, node_mode, queue, "
    'DATE_FORMAT(`creation`,"%%Y/%%c/%%e %%T") creation, remarks '
    "from node where {key} like %(search)s and `node_state`=%(node_state)s limit %(start)s, %(step)s;",
}

GET_NODE_MANAGER_NAME = "select node_name, queue from node where nid = %(nid)s;"

UPDATE_NODE_QUEUE = "update node set queue = %(queue)s where nid = %(nid)s;"

GET_LIBRARY_CMS_FILTER_NUM = "select count(1) `count` from library_cms_filter; "

GET_LIBRARY_CMS_FILTER = (
    "select `id`, `name`, `color`, `level` "
    "from  library_cms_filter "
    "order by `id` desc limit %(start)s, %(step)s;"
)

INSERT_LIBRARY_CMS_FILTER = (
    "insert into library_cms_filter (`name`, `color`, `level`) "
    "values (%(name)s, %(color)s, %(level)s) "
    "ON DUPLICATE KEY UPDATE color=%(color)s, level=%(level)s"
)

UPDATE_LIBRARY_CMS_FILTER = (
    "UPDATE library_cms_filter set color=%(color)s, level=%(level)s where id = %(id)s"
)

DELETE_LIBRARY_CMS_FILTER = "DELETE FROM library_cms_filter where id = %(id)s"

GET_API_PERIOD = (
    "select `uid`, `token_key`, `creation`, `vperiod` "
    "from `api_token` where `token_id` = %(token_id)s;"
)

CREATE_USER_TOKEN = (
    "INSERT INTO api_token (uid, `token_key`) value (%(uid)s, %(token)s) "
    "ON DUPLICATE KEY UPDATE `token_key` = %(token)s"
)

INSERT_FUCK = (
    "insert into `fuck` (`fuck_id`, `fuck_name`) values (%(fuck_id)s, %(fuck_name)s);"
)
INSERT_FUCK_TO_PROJECT = (
    "insert into `fuck_project` (`fid`, `pid`) values (%(fid)s, %(pid)s);"
)

GET_FUCK_LIST = (
    "select fid, fuck_id, fuck_name, "
    'DATE_FORMAT(`creation`, "%%Y/%%c/%%e %%T") as `creation` '
    "from `fuck` order by `fid` desc limit %(start)s, %(step)s;"
)

GET_FUCK_COUNT = "select count(1) as `count` from `fuck`;"

GET_PROJECT_IN_FUCK = (
    "SELECT `p`.`pid`, `target`, p.`name`, p.`uid`, u.`name` `uname`, p.`gid`, "
    'DATE_FORMAT(`starting`,"%%Y/%%c/%%e %%T") as `starting`, '
    "(IFNULL(pu.`time`, 1) > IFNULL(pc.`time`, 0)) as `update` "
    "FROM project as `p` "
    "inner join `fuck_project` as `f` on p.pid = f.pid "
    "left join `user` as `u` on p.uid = u.uid "
    "left join `project_check` as `pc` on p.pid = pc.pid AND pc.uid = %(uid)s "
    "left join `project_update` as `pu` on p.pid = pu.pid "
    "WHERE f.`fid` = %(fid)s "
    "ORDER BY {order} {sort} LIMIT %(start)s, %(step)s"
)

GET_PROJECT_IN_FUCK_COUNT = (
    "SELECT count(1) as `count` "
    "FROM `project` as `p` "
    "inner join `fuck_project` as `f` on p.pid = f.pid "
    "WHERE f.fid = %(fid)s;"
)

GET_DUMPS_DB = (
    "SELECT collection_name, "
    'DATE_FORMAT(`creation_time`,"%%Y/%%c/%%e %%T") as `creation_time`,data_count '
    "FROM `dumps_db` d JOIN `task` t on t.tid = d.tid "
    "JOIN `project` p on p.pid = t.pid "
    "WHERE t.tid = %(tid)s and (p.gid = %(gid)s or %(gid)s = 0)"
)

GET_TASK_RAW_INFO = (
    "select r.*, t.pid,t.tid,"
    "concat(hex(t.prefix),LPAD(count(1)-1,2,'0')) prefix "
    "from {0} r join task t on r.tid = t.tid "
    "cross join {0} r1 on r1.tid = t.tid and r1.rid <= %(rid)s where r.rid = %(rid)s;"
)

# -------------------------------- this user manager --------------------------------------

GET_XSSPAYLOAD = "select `payload` from `xss_payloads` where uid = %(uid)s"

INSERT_XSSPAYLOAD = (
    "insert into `xss_payloads` (`uid` ,`payload`) values (%(uid)s, %(payload)s);"
)

UPDATE_XSSPAYLOAD = (
    "update `xss_payloads` set `payload` = %(payload)s where uid = %(uid)s"
)

DELETE_XSSPAYLOAD = "delete from `xss_payloads` where uid = %(uid)s"

# -------------------------------- push --------------------------------------

GET_USER_NOTICE_PRESENCE = (
    "SELECT privateKey as t FROM user_notice " "WHERE uid = %(uid)s and ua = %(ua)s"
)

INSET_USER_NOTICE = (
    "INSERT INTO user_notice (uid, privateKey, subscription_info, ua) "
    "VALUES (%(uid)s, %(private)s, %(subscription_info)s, %(ua)s)"
)

UPDATE_USER_NOTICE = (
    "UPDATE user_notice set subscription_info = %(subscription_info)s "
    "WHERE uid = %(uid)s and ua = %(ua)s"
)

GET_USER_NOTICE_SUBSCRIPTION_INFO = (
    "SELECT privateKey, subscription_info FROM user_notice" "WHERE uid in ({})"
)

GET_ALLUSER_NOTICE_SUBSCRIPTION_INFO = (
    "SELECT privateKey, subscription_info FROM user_notice"
)

REQUEST_LOG = (
    "INSERT INTO `log` (`method` ,`url`,`remote_ip` ,`arguments`,`body`,`expend_time` ,`version`, `create_user`) values"
    "(%(method)s, %(url)s, %(remote_ip)s, %(arguments)s, %(body)s, %(expend_time)s, %(version)s, %(create_user)s);"
)

LOGIN_LOG = (
    "INSERT INTO `login_log` (`user_name` ,`ip`) values (%(user_name)s, %(ip)s);"
)

GET_OPERATION_LOGS = (
    "select a.`id`, a.`method`, a.`url`, a.`remote_ip`, b.`name`,"
    'DATE_FORMAT(a.`create_time`, "%%Y/%%c/%%e %%T") as `create_time` '
    "from `log` AS a INNER JOIN `user` AS b ON a.create_user=b.uid order by a.create_time desc limit %(start)s, %(step)s;"
)
SEARCH_OPERATION_LOGS = {
    "subject_sql": "select a.`id`, a.`method`, a.`url`, a.`remote_ip`, b.`name`,"
    'DATE_FORMAT(a.`create_time`, "%%Y/%%c/%%e %%T") as `create_time` '
    "from `log` AS a INNER JOIN `user` AS b ON a.create_user=b.uid where b.name like %(name)s",
    "sort_sql": "order by a.create_time desc limit %(start)s, %(step)s;",
}

GET_OPERATION_LOGS_COUNT = "select count(1) as `count` from `log`"

SEARCH_OPERATION_LOGS_COUNT = "select count(1) as `count` from `log` AS a INNER JOIN `user` AS b ON a.create_user=b.uid where b.name like %(name)s"

GET_USER_LOGIN_LOGS = (
    "select `id`, `user_name`,`ip`,"
    'DATE_FORMAT(`create_time`, "%%Y/%%c/%%e %%T") as `create_time` '
    "from `login_log` order by create_time desc limit %(start)s, %(step)s;"
)

SEARCH_USER_LOGIN_LOGS = {
    "subject_sql": 'select `id`, `user_name`,`ip`,DATE_FORMAT(`create_time`, "%%Y/%%c/%%e %%T") as `create_time` from `login_log`',
    "sort_sql": " order by create_time desc limit %(start)s, %(step)s;",
}

GET_USER_LOGIN_LOGS_COUNT = "select count(1) as `count` from `login_log`;"

SEARCH_USER_LOGIN_LOGS_COUNT = "select count(1) as `count` from `login_log`"

GET_DICTIONARY = "SELECT `did`, `dname`, `label`, `description`, `dictionary_count` as `dcount` FROM `dictionary` where dtype = %(dictionary_type)s order by did desc LIMIT %(start)s, %(step)s ;"

GET_DICTIONARY_COUNT = (
    "select count(1) as `count` from `dictionary` where dtype = %(dictionary_type)s;"
)

DICTIONARY_INSERT = "INSERT  INTO dictionary ( `dname`, `content`, `label`, `description`, `dtype`, `dictionary_count`) values (%(d_name)s, %(content)s, %(label)s, %(description)s, %(d_type)s, %(dictionary_count)s)"

UPDATE_DICTIONARY = {
    "get_dictionary": "SELECT `did`, `dname`, `content`, `label`, `description`, `dictionary_count` as `dcount` FROM `dictionary` where did = %(did)s and dtype=%(dictionary_type)s;",
    "update_dictionary": "UPDATE `dictionary` SET `content` = %(content)s, `dictionary_count`=%(dictionary_count)s  WHERE `did` = %(did)s and dtype = %(dtype)s",
}

DELETE_DICTIONARY = (
    "delete from `dictionary` where `did` = %(did)s and `dtype`=%(dictionary_type)s;"
)

SEARCH_DICTIONARY_COUNT = (
    "select count(1) as `count` from `dictionary` where dtype = %(dtype)s "
)

SEARCH_DICTIONARY = {
    "subject_sql": "SELECT `did`, `dname`, `label`, `description`, `dictionary_count` as `dcount` FROM `dictionary` where dtype = %(dtype)s",
    "sort_sql": " order by did desc LIMIT %(start)s, %(step)s ;",
}


INSERT_TACTICS = (
    "insert into `tactics` (`classification`, `name`, `content`, `description`) values (%(classification)s, %(name)s, %(content)s, %(description)s);"
)

GET_TACTICS = "SELECT `classification` as `tactics_classification`, `name` as `tactics_name`, `description`, `usage` as `tactics_usage` FROM `tactics` order by id desc LIMIT %(start)s, %(step)s ;"

GET_TACTICS_COUNT = (
    "select count(1) as `count` from `tactics`;"
)

VIEW_TACTICS = {
    "get_tactics_groups":  "select `gid` as `id`, `name` as `gname` from `group` order by gid asc;",
    "get_tactics_obj": "SELECT  `id` as `tid`, `classification` as `tactics_classification`, `name` as `tactics_name`, `description` as `describe` FROM `tactics` where `id`=%(id)s",
    "get_tactics_group_relation": "SELECT `group_id` as `gid` FROM `group_tactics_relationship` where `tactics_id`=%(id)s;"

}

UPDATE_TACTICS = {
    "update_tactics": "UPDATE `tactics` SET `classification` = %(classification)s, `name`=%(name)s,`description`=%(description)s  WHERE `id`=%(tid)s;",
    "delete_tactics_group_relation": "delete from `group_tactics_relationship` where `tactics_id`=%(tid)s",
    "insert_tactics_group_relation":"INSERT INTO `group_tactics_relationship` (`tactics_id`, `group_id`) VALUES (%s,%s);"
}
UPDATE_TACTICS_CONTENT = ("UPDATE `tactics` SET `content` = %(content)s WHERE `id`=%(id)s;")
