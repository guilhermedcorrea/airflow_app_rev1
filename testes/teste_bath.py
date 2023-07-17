import sys
from pyspark import SparkContext

output = sys.argv[1]
sc = SparkContext(appName="PySpark Test")
try:
  sc.parallelize(range(100), 10).map(lambda x: (x, x * 2)).saveAsTextFile(output)
finally:
  sc.stop()