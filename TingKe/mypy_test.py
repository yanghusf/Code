class SearchUserManager(ManagerRestApi):
    """
    管理用户处理器
    """
    async def get(self, manager_id: str) -> None:
        """
        获取用户列表，动态资源
        :param manager_id:
        :return:
        """
        try:
            page = abs(int(self.get_argument("page", "1")))
            step = abs(int(self.get_argument("step", "20")))
            start = (page - 1) * step
        except (ValueError, KeyError):
            return await self.finish({"code": response_code.ParameterError})

        group_id = self.get_argument("gid", "")
        user_name = self.get_argument("user_name", "")
        user_state = self.get_argument("state", "")
        group_id = '' if group_id =='-1' else group_id
        user_state = '' if user_state =='-1' else user_state
        try:
            user_name = urllib.parse.unquote(user_name)
        except (ValueError, KeyError):
            return await self.finish({"code": response_code.ParameterError})

        query_field:Dict[str, str] = {}
        if user_name:
            query_field["name"] = "like"
        if group_id:
            query_field["gid"]="and"
        if user_state:
            query_field["state"] = "and"
        get_user_count_obj = VerifyQueryParameters(
            query_field,{"name":user_name, "gid":group_id,"state":user_state}, warehouse.SEARCH_USER_COUNT["subject_sql"]
        )
        if not get_user_count_obj.filter_keywords:
            return await self.finish({"code": response_code.ParameterError})
        get_user_count_sql = get_user_count_obj.stitching_sql()
        get_users_obj = VerifyQueryParameters(
            {"name": "like"},
            warehouse.SEARCH_USERS["subject_sql"],
            warehouse.SEARCH_USERS["sort_sql"],
        )
        get_users_sql = get_users_obj.stitching_sql()

        async with self.db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(get_user_count_sql)
                count = await cur.fetchone()
                await cur.execute(get_users_sql, {"start": start, "step": step})
                users = await cur.fetchall()
        return await self.finish({"code": 0, "users": users, **count})