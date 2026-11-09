import pandas as pd

class AccountingEngine:
    def __init__(self, conn):
        self.conn = conn
        
    def get_sales_df(self):
        return pd.read_sql("SELECT * FROM daily_sales", self.conn)
        
    def get_financial_summary(self, start_date=None, end_date=None):
        df = self.get_sales_df()
        df['date'] = pd.to_datetime(df['date'])
        
        if start_date and end_date:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
        total_revenue = (df['units'] * df['unit_price']).sum()
        total_cogs = (df['units'] * df['cost_price']).sum()
        gross_profit = total_revenue - total_cogs
        
        # Estimación de OPEX genérico (30% de la utilidad bruta para simulación PYME)
        operating_expenses = gross_profit * 0.4
        ebit = gross_profit - operating_expenses
        
        # Gastos financieros e impuestos simulados
        interest_expense = ebit * 0.15 if ebit > 0 else 0.0
        ebt = ebit - interest_expense
        tax = ebt * 0.30 if ebt > 0 else 0.0
        net_income = ebt - tax
        
        # Indicadores de Apalancamiento
        # GAO = Margen de Contribución / EBIT (Asumimos costos fijos estimados en OPEX)
        fixed_costs = operating_expenses * 0.7
        contribution_margin = total_revenue - (total_cogs + (operating_expenses * 0.3))
        gao = contribution_margin / ebit if ebit != 0 else 0.0
        
        # GAF = EBIT / (EBIT - Intereses)
        gaf = ebit / (ebit - interest_expense) if (ebit - interest_expense) != 0 else 1.0
        gat = gao * gaf
        
        # Indicadores de Rentabilidad
        total_assets = 150000.0 # Base patrimonial simulada para PYME
        total_equity = 90000.0
        roa = (net_income / total_assets) * 100
        roe = (net_income / total_equity) * 100
        net_margin = (net_income / total_revenue) * 100 if total_revenue > 0 else 0.0
        
        return {
            "Total Revenue": total_revenue,
            "COGS": total_cogs,
            "Gross Profit": gross_profit,
            "Operating Expenses": operating_expenses,
            "EBIT": ebit,
            "Interest Expense": interest_expense,
            "Net Income": net_income,
            "GAO (Operating Leverage)": round(gao, 2),
            "GAF (Financial Leverage)": round(gaf, 2),
            "GAT (Total Leverage)": round(gat, 2),
            "ROA (%)": round(roa, 2),
            "ROE (%)": round(roe, 2),
            "Net Margin (%)": round(net_margin, 2)
        }