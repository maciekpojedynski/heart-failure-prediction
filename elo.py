import re
import pandas as pd

# Ścieżka do pliku (wersja archiwum)
FILE_PATH = 'raw_transactions.txt'
ARCHIVE_PATH = 'archive/processed_transactions_20250101.csv'

# Krok 1: Wczytanie pliku i złączenie w jeden długi string
with open(FILE_PATH, 'r') as f:
    raw_text = f.read()

# Krok 2: Użycie Regex do ekstrakcji i restrukturyzacji (KLUCZOWY ETAP)
# Wzorzec szuka początku wiersza (daty/ID) i chwyta wszystko 
# do następnego wiersza (Amount). Używamy non-greedy match (.*?).
pattern = re.compile(
    r'(?P<Date>\d{2}-\d{2}-\d{4}): TRANSACTION STARTED - UserID: (?P<UserID>\d+)\n'
    r'Amount: \$(?P<Amount>[\d\.,]+) \| Type: (?P<Type>\w+)'
)

# Znajdź wszystkie pasujące grupy
records = []
for match in pattern.finditer(raw_text):
    records.append(match.groupdict())

# Krok 3: Utworzenie DataFrame i Zapis (ETL)
df_transactions = pd.DataFrame(records)

# Wymuszenie typów przed zapisem
df_transactions['Amount'] = pd.to_numeric(df_transactions['Amount'].str.replace(',', ''), errors='coerce')
df_transactions['UserID'] = df_transactions['UserID'].astype(int)

# Zapis do archiwum/docelowego CSV
df_transactions.to_csv(ARCHIVE_PATH, index=False)

print(f"Projekt 1: Pomyślnie przetworzono {len(df_transactions)} zdarzeń i zapisano do archiwum.")
