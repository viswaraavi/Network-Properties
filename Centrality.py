import os
import sys
os.environ['SPARK_HOME'] = "/home/viswa/Downloads/spark-1.6.2-bin-hadoop2.6"
sys.path.append("/home/viswa/Downloads/spark-1.6.2-bin-hadoop2.6/python")
sys.path.append("/home/viswa/Downloads/spark-1.6.2-bin-hadoop2.6/python/lib/py4j-0.9-src.zip")
try:
    from pyspark import SparkContext
    from pyspark import SparkConf
    from pyspark.sql import SQLContext
    from graphframes import *
except ImportError as e:
    print ("error importing spark modules", e)
    sys.exit(1)


def create_graphframe(filename):
    conf = SparkConf().setAppName("Network")
    sc = SparkContext(conf=conf)
    graph=[0,0]
    graphrdd=sc.textFile(filename)
    vertexrdd=graphrdd.map(lambda x:int(x.split(" ")[0])).distinct()
    vertexrdd=vertexrdd.map(lambda x:tuple([x]))
    edgerdd=graphrdd.map(lambda x:tuple([int(i) for i in x.split(" ")]))
    graph[0]=vertexrdd.collect()
    graph[1]=edgerdd.collect()
    sqlcontext=SQLContext(sc)
    v=sqlcontext.createDataFrame(graph[0],["id"])
    e=sqlcontext.createDataFrame(graph[1],["src","dst"])
    g=GraphFrame(v,e)
    return g

frame=create_graphframe("amazon.graph.large")

def closeness(frame):
    return frame.shortestPaths(landmarks=frame.vertices.select("id").map(lambda r:r[0]).collect())


print closeness(frame).show()