# import the operator to inherit from
from airflow.models.baseoperator import BaseOperator


# define the class inheriting from an existing operator class
class SparkOperator(BaseOperator):


    def __init__(self, my_parameter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_parameter = my_parameter

    def execute(self, context):
        self.log.info(self.my_parameter)
        return "hi :)"
