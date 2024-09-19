# Databricks notebook source
# MAGIC %sql
# MAGIC SELECT * FROM read_files(
# MAGIC   'file:/Workspace/Users/marton.ferenczi@raiffeisen.hu/rafi-bpc-hackathon-2024/customer.csv',
# MAGIC   format => 'csv',
# MAGIC   header => true,
# MAGIC   mode => 'FAILFAST')
# MAGIC

# COMMAND ----------

pwd
