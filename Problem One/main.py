import pandas as pd
from io import StringIO
import requests
import lxml


url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Fetch the HTML content with headers
response = requests.get(url, headers=headers)
response.raise_for_status()

tables = pd.read_html(StringIO(response.text))
df = tables[0]
df.to_csv('data.csv')
df.reset_index

df = df[['Symbol', 'Security', 'Date added']]

df['Date added'] = pd.to_datetime(df['Date added'], errors="coerce")
df['Year added'] = df['Date added'].dt.year

additions_by_year = (
    df['Year added'].value_counts().sort_index()
)

additions_since_2020 = additions_by_year[additions_by_year.index >= 2020]

