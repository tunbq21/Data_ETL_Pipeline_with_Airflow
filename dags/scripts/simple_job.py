from pyspark.sql import SparkSession

# Tạo SparkSession
spark = SparkSession.builder.appName("SimpleSparkJob").getOrCreate()

# Đọc file CSV mẫu
data = spark.read.csv("/opt/airflow/dags/scripts/data.csv", header=True)

# Đếm số dòng
count = data.count()
print(f"📊 Số dòng trong file CSV là: {count}")

spark.stop()
