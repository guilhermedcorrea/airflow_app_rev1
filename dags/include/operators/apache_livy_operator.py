
from airflow.models.baseoperator import BaseOperator


class LivyOperator(BaseOperator):

    def __init__(self, my_parameter, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.my_parameter = my_parameter

    def execute(self, context):
      
        self.log.info(self.my_parameter)
     
        return 
