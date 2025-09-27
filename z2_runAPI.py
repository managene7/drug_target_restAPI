from fastapi import FastAPI
# from typing import Optional
# from database import SessionLocal
from models import Target, Drug
# from sqlalchemy import select
import sqlite3
import uvicorn


app = FastAPI()



@app.get("/targets/{target}")
def get_best_drugs_by_target(target: str) -> dict:
    """
    To search the drug-target number and adverse effect database
    """
    conn=sqlite3.connect('Drug_Target_AE.db')
    cursor=conn.cursor()
    cursor.execute(f"SELECT target, value from Target WHERE target=='{target}'")
    search_result=cursor.fetchall()
    return {"target": search_result[0][0], "value": search_result[0][1]}



@app.get("/drugs/{drug_concatenated}")
def get_drug_info(drug_concatenated: str) -> dict:
    """
    To search the full drug informatino database
    """

    # Convert concated drug names int list format (The drug names are concatenated with "__").
    drug_list=drug_concatenated.split('__')

    conn=sqlite3.connect('Drug_Target_AE.db')

    # Extract drug information
    cursor=conn.cursor()

    placeholders = ",".join("?" for _ in drug_list)
    query=f"SELECT * FROM Drug WHERE drug IN ({placeholders})"

    cursor.execute(query, drug_list)
    search_result=cursor.fetchall()

    # Extract header information
    cursor.execute("SELECT drug, content from Drug WHERE drug=='header'")
    header_info=cursor.fetchall()
    
    return {"content": search_result, 'header':header_info[0][1]}


if __name__ == "__main__":
    uvicorn.run(
        "z2_runAPI:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
