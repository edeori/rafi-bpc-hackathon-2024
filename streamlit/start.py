# Databricks notebook source
!pip install streamlit
dbutils.library.restartPython()

# COMMAND ----------

import os
base_url='https://' + spark.conf.get("spark.databricks.workspaceUrl")
workspace_id=spark.conf.get("spark.databricks.clusterUsageTags.orgId")
cluster_id=spark.conf.get("spark.databricks.clusterUsageTags.clusterId")
dashboard_port='8501'
pathname_prefix='/driver-proxy/o/' + workspace_id + '/' + cluster_id + '/' + dashboard_port
 
apitoken = dbutils.notebook().entry_point.getDbutils().notebook().getContext().apiToken().get()
dashboard_url=base_url + pathname_prefix + '/app' # ?token=' + apitoken[0:10] + " " + apitoken[10:]
 
#Small Output
print("Once the dashbord is running, it can be accessed at this link:\n\n" + dashboard_url)
 
#Large Output
displayHTML(f'<a href="{dashboard_url}" target="_blank"><h2><b>APP URL</b></h2></a>')

print(base_url)
 
!streamlit run --server.baseUrlPath=/app /Workspace/Users/vendel.mellau@rbinternational.com/streamlit/sandbox.py --server.enableCORS=false --server.enableXsrfProtection=false
