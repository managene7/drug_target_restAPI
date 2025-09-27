import models
from database import engine
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

df_target_to_drugs_AE=pd.read_csv("./data_processed/Target_to_drugs_AE.csv")
df_target_to_drugs_AE['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

df_filtered_molecules=pd.read_csv("./data_processed/Filtered_molecules.csv")
df_filtered_molecules['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

db_engine=create_engine("sqlite:///./Drug_Target_AE.db")

df_target_to_drugs_AE.to_sql("Target", con=db_engine, if_exists='replace')
df_filtered_molecules.to_sql("Drug", con=db_engine, if_exists='replace')

print("\n\n*** The SQL database has built successfully ***\n\n")

