import asyncio


class Database:
    def __init__(self):
        self.connection = None

    @asyncio.coroutine
    def query(self, sql_query):
        """
        :param sql_query: Query to execute.
        :return:          Result of the query.
        """
        def query_thread(sql):
            cursor = self.connection.cursor()
            result = cursor.execute(sql)
            cursor.close()
            return result

        loop = asyncio.get_event_loop()
        rows = yield from loop.run_in_executor(query_thread, sql_query)
        return rows


mysql_database = Database()
