from transformers import pipeline

class Text2SQLModel:
    def __init__(self):
        self.pipe = pipeline("text2sql-generation", model="text2sql-ai/text2sql-large-dbmdz")

    def generate_sql(self, prompt, schema):
        context = " ".join(schema)
        return self.pipe(f"{prompt} \n {context}")[0]["generated_text"]
