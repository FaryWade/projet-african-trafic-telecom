import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col

# Initialisation de Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Lecture des données CSV depuis S3/raw/
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="telecom_bd",
    table_name="raw_raw"
)

# Conversion en DataFrame Spark pour nettoyage
df = datasource.toDF()

# Nettoyage : supprimer les lignes avec des valeurs nulles
df_clean = df.dropna()

# Normalisation : s'assurer des bons types
df_clean = df_clean \
    .withColumn("duree_secondes", col("duree_secondes").cast("integer")) \
    .withColumn("volume_mb", col("volume_mb").cast("double")) \
    .withColumn("montant_xof", col("montant_xof").cast("integer"))

# Écriture en Parquet avec compression Snappy dans S3/processed/
df_clean.write \
    .mode("overwrite") \
    .option("compression", "snappy") \
    .partitionBy("pays", "type_evenement") \
    .parquet("s3://african-trafic-telecom/processed/")

print(f"Nombre de lignes traitées : {df_clean.count()}")
print("Job ETL terminé avec succès !")

job.commit()
