from typing import Dict


def stitching_sql(
    query_dict: Dict[str, str],
    subject_sql: str,
    sort_sql=None,
    is_exist_where: bool = False,
    query_time: Dict[str, str] = None,
):
    """

    :param query_dict:key--table字段, value--查询条件
    :param subject_sql: select 主体语句
    :param sort_sql: 排序 分组 sql语句
    :param is_exist_where: query_sql 是否含有where关键字
    :param query_time: 查询时间
    :return:
    """
    flag = True
    sql = subject_sql.rstrip()
    for i in query_dict:
        if query_dict[i]:

            if is_exist_where:
                start_con = " and `{0}`=%({1})s".format(i, i)
                sql += start_con
                continue
            if flag:
                start_con = " where `{0}`=%({1})s".format(i, i)
                sql += start_con
                flag = False
            else:
                start_con = " and `{0}`=%({1})s".format(i, i)
                sql += start_con
    if query_time:

        time_keys = list(query_time.keys())
        if query_time[time_keys[0]]:
            if "where" not in sql:
                time_sql = " where `{0}`>=%({1})s".format(time_keys[0], time_keys[0])
                sql += time_sql
            else:
                time_sql = " and `{0}`>=%({1})s".format(time_keys[0], time_keys[0])
                sql += time_sql

        if query_time[time_keys[1]]:
            if "where" not in sql:
                time_sql = " where `{0}`<=%({1})s".format(time_keys[1], time_keys[1])
                sql += time_sql
            else:

                time_sql = " and `{0}`<=%({1})s".format(time_keys[1], time_keys[1])
                sql += time_sql
    if sort_sql:
        sort_sql = " " + sort_sql
        sql += sort_sql
    return sql
