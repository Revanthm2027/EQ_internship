import sqlite3
import pandas as pd
import plotly.express as px
import base64
from io import BytesIO

def execute_query(sql, db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def get_db_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = []
    for t in tables:
        table = t[0]
        cursor.execute(f"PRAGMA table_info({table})")
        cols = cursor.fetchall()
        col_names = ", ".join([c[1] for c in cols])
        schema.append(f"Table {table} with columns: {col_names}")
    conn.close()
    return schema

def generate_charts(df):
    if df.shape[1] >= 2:
        fig = px.bar(df, x=df.columns[0], y=df.columns[1])
        buf = BytesIO()
        fig.write_image(buf, format="png")
        img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return img_str
    return None
