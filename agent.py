import ollama
import pandas as pd

class AccountingAgent:
    def __init__(self, conn, model_name="qwen:7b"): # O el tag exacto que tengas instalado localmente (ej: qwen2.5:7b)
        self.conn = conn
        self.model_name = model_name
        
    def query(self, user_question):
        # Cargar contexto resumido de la base de datos para el agente
        df = pd.read_sql("SELECT * FROM daily_sales", self.conn)
        summary_text = f"""
        Total sales transactions recorded: {len(df)}
        Top categories: {df['category'].unique().tolist()}
        Total Revenue generated: ${(df['units'] * df['unit_price']).sum():,.2f}
        Top selling product by units: {df.groupby('product_name')['units'].sum().idxmax()}
        """
        
        prompt = f"""
        You are an expert AI Accounting & Corporate Finance Auditor for a SME.
        Analyze the following company data context and answer the user question professionally in English.
        
        Data Context:
        {summary_text}
        
        User Question: {user_question}
        """
        
        try:
            response = ollama.chat(model=self.model_name, messages=[
                {"role": "system", "content": "You are a professional corporate finance and accounting AI expert."},
                {"role": "user", "content": prompt}
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error communicating with local Ollama instance ({self.model_name}): {str(e)}. Make sure Ollama is running (`ollama serve`) and the model is pulled."