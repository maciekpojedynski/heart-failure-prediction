import tabula
import pandas as pd

PDF_FILE = 'monthly_budget_report.pdf'

# Krok 1: Ekstrakcja danych z tabeli w PDF
# Ta komenda wczyta tabele z podanego pliku
try:
    df_list = tabula.read_pdf(PDF_FILE, pages='all', multiple_tables=True, output_format='dataframe')
    
    # Załóżmy, że interesuje nas pierwsza tabela
    df_raw = df_list[0] 

except Exception as e:
    print(f"Błąd ekstrakcji PDF: {e}")
    # W praktyce: Zgłoszenie błędu i zatrzymanie potoku

# Krok 2: Czyszczenie i transformacja (przykład: agregacja)
# Załóżmy, że kolumna 'Expense_Amount' jest stringiem i wymaga czyszczenia
if 'Expense_Amount' in df_raw.columns:
    
    # 1. Czyszczenie stringów (usuwanie $, konwersja na float)
    df_raw['Expense_Amount'] = (
        df_raw['Expense_Amount']
        .astype(str)
        .str.replace(r'[$,]', '', regex=True)
        .astype(float)
    )
    
    # 2. Agregacja i raport
    total_expense = df_raw['Expense_Amount'].sum()
    
    print(f"Projekt 2: Całkowity zagregowany budżet z PDF: ${total_expense:,.2f}")
    
# Krok 3: Opcjonalny zapis finalnego raportu
# df_final_report.to_excel('Final_Aggregated_Report.xlsx')
