from typing import List, Tuple, Dict, Union, Optional


def func2(query_key: Dict[str, str]) -> bool:
    lis: List[str] = [
        " or ",
        "or ",
        " or",
        "and ",
        " and",
        " and ",
        "#",
        "--",
        " --",
        "-- ",
        " -- ",
    ]

    for i in lis:
        if i in query_key:
            return False
    return True


# res: map = map(func2, [v for k, v in a.items()])
# print(all(list(res)))


class VerifyQueryParameters(object):
    """
    :param query_parameters:key--table字段, value--查询条件
    :param subject_sql: select 主体语句
    :param sort_sql: 排序 分组 sql语句
    :param is_exist_where: query_sql 是否含有where关键字
    :param query_time: 查询时间
    :return:
    """

    def __init__(
        self,
        query_field: Dict[str, str],
        query_parameters: Dict[str, str],
        subject_sql: str,
        sort_sql:Optional[str] = None,
        is_exist_where:Optional[bool] = False,
        query_time:Optional[Dict[str, str]] = None,
    ):
        self.query_field = query_field
        self.query_parameters = query_parameters
        self.lis: List[str] = [
            " or ",
            "or ",
            " or",
            "and ",
            " and",
            " and ",
            "#",
            "--",
            " --",
            "-- ",
            " -- ",
            "||",
            "from "
        ]

        self.subject_sql = subject_sql
        self.query_time = query_time
        self.sort_sql = sort_sql
        self.is_exist_where = is_exist_where
        self.query_time = query_time

    def item_keywords(self, query_key) -> bool:
        for i in self.lis:
            if i in query_key:
                return False
        return True

    @property
    def filter_keywords(self) -> bool:
        res = map(
            self.item_keywords, [v for k, v in self.query_parameters.items()]
        )
        return all(list(res))

    def stitching_sql(self) -> str:

        flag = True
        sql = self.subject_sql.rstrip()
        for i in self.query_field:
            if self.query_field[i]:

                if self.is_exist_where:
                    start_con = " and `{0}`{1}%({2})s".format(i, self.query_field[i], i)
                    sql += start_con
                    continue
                if flag:
                    start_con = " where `{0}`{1}%({2})s".format(i,self.query_field[i], i)
                    sql += start_con
                    flag = False
                else:
                    start_con = " and `{0}`{1}%({2})s".format(i,self.query_field[i], i)
                    sql += start_con
        if self.query_time:

            time_keys = list(self.query_time.keys())
            if self.query_time[time_keys[0]]:
                if "where" not in sql:
                    time_sql = " where `{0}`>=%({1})s".format(
                        time_keys[0], time_keys[0]
                    )
                    sql += time_sql
                else:
                    time_sql = " and `{0}`>=%({1})s".format(time_keys[0], time_keys[0])
                    sql += time_sql

            if self.query_time[time_keys[1]]:
                if "where" not in sql:
                    time_sql = " where `{0}`<=%({1})s".format(
                        time_keys[1], time_keys[1]
                    )
                    sql += time_sql
                else:

                    time_sql = " and `{0}`<=%({1})s".format(time_keys[1], time_keys[1])
                    sql += time_sql
        if self.sort_sql:
            sort_sql = " " + self.sort_sql
            sql += sort_sql
        return sql



group_id = "0"
user_name = "sc"
user_state = "-1"
group_id = "" if group_id == "-1" else group_id
user_state = "" if user_state == "-1" else user_state

query_field: Dict[str, str] = {"user_name":"and"}
# query_field["b.name"] = "like"

query_parameters = {
    "name": f"{user_name}%",

}
SEARCH_USER_LOGIN_LOGS = {
    "subject_sql": 'select `id`, `user_name`,`ip`,DATE_FORMAT(`create_time`, "%%Y/%%c/%%e %%T") as `create_time` from `login_log`',
    "sort_sql": " order by create_time desc limit %(start)s, %(step)s;",
}

SEARCH_USER_LOGIN_LOGS_COUNT = "select count(1) as `count` from `login_log`"

op_log_count_obj = VerifyQueryParameters(
    {"user_name": "and"},
    {"user_name": user_name},
    SEARCH_USER_LOGIN_LOGS_COUNT,
)

get_login_log_count_sql = op_log_count_obj.stitching_sql()
get_op_logs_obj = VerifyQueryParameters(
    {"user_name": "and"},
    {"user_name": user_name},
    SEARCH_USER_LOGIN_LOGS["subject_sql"],
    SEARCH_USER_LOGIN_LOGS["sort_sql"],
)
get_login_logs_sql = get_op_logs_obj.stitching_sql()

print(get_login_logs_sql)

