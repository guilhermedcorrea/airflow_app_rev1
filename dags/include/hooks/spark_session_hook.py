# import the hook to inherit from
from airflow.hooks.base import BaseHook


class Sparkhook(BaseHook):
  

    conn_name_attr = "connpyspark"
    default_conn_name = "spark_hook"
    conn_type = "general"
    hook_name = "SPARKHOOKO"

    def __init__(
        self, my_conn_id: str = default_conn_name, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.my_conn_id = my_conn_id
        self.get_conn()

    def get_conn(self):
       
        conn_id = getattr(self, self.conn_name_attr)
        conn = self.get_connection(conn_id)

        return conn

