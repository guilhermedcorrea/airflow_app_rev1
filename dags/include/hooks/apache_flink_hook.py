
from airflow.hooks.base import BaseHook

class ApacheFlinkOperator(BaseHook):
 
    conn_name_attr = "finkhoo"

    default_conn_name = "Apache_Flink"

    conn_type = "general"
  
    hook_name = "FLINKHOOK"

 
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

   