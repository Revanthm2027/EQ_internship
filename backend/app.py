from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from model.text2sql_model import Text2SQLModel
from utils import execute_query, get_db_schema, generate_charts

app = Flask(__name__)
CORS(app)

model = Text2SQLModel()
uploaded_df = None
db_path = None

@app.route("/upload", methods=["POST"])
def upload():
    global uploaded_df, db_path
    file = request.files["file"]
    if file.filename.endswith(".csv"):
        uploaded_df = pd.read_csv(file)
        db_path = "backend/temp.db"
        uploaded_df.to_sql("data", sqlite3.connect(db_path), index=False, if_exists="replace")
    return jsonify({"message": "File uploaded successfully", "columns": uploaded_df.columns.tolist()})

@app.route("/prompt", methods=["POST"])
def prompt():
    global uploaded_df, db_path
    user_prompt = request.json.get("prompt")
    schema = get_db_schema(db_path)
    generated_sql = model.generate_sql(user_prompt, schema)
    result_df = execute_query(generated_sql, db_path)
    chart = generate_charts(result_df)
    return jsonify({
        "sql": generated_sql,
        "table": result_df.to_dict(orient="records"),
        "columns": result_df.columns.tolist(),
        "chart": chart
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
