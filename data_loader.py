"""Data loading and preprocessing module."""
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data():
    """Load and preprocess all data sources."""
    xlsx = os.path.join(BASE_DIR, "Data Dashboard Visdat.xlsx")
    eur_csv = os.path.join(BASE_DIR, "FX_IDC_EURIDR, 1D.csv")

    # Load sheets
    df_ihsg = pd.read_excel(xlsx, sheet_name="IDX SECTOR")
    df_fx = pd.read_excel(xlsx, sheet_name="NILAI TUKAR")

    # Load EUR correction
    df_eur = pd.read_csv(eur_csv)
    df_eur['time'] = pd.to_datetime(df_eur['time'])

    # Fix EUR column
    df_fx['Tanggal'] = pd.to_datetime(df_fx['Tanggal'])
    eur_map = df_eur.set_index('time')['close']
    df_fx = df_fx.set_index('Tanggal')
    df_fx['EURIDR'] = eur_map.reindex(df_fx.index)
    df_fx['EURIDR'] = df_fx['EURIDR'].ffill().bfill()
    df_fx = df_fx.reset_index()

    # Clean IHSG
    df_ihsg['time'] = pd.to_datetime(df_ihsg['time'])
    if 'idxtechno.1' in df_ihsg.columns:
        df_ihsg = df_ihsg.drop(columns=['idxtechno.1'])

    # Currency display names
    currency_names = {
        'USDIDR': 'USD/IDR', 'EURIDR': 'EUR/IDR', 'GBPIDR': 'GBP/IDR',
        'JPYIDR': 'JPY/IDR', 'AUDIDR': 'AUD/IDR', 'CADIDR': 'CAD/IDR',
        'CHFIDR': 'CHF/IDR', 'CNHIDR': 'CNH/IDR', 'HKDIDR': 'HKD/IDR',
        'NZDIDR': 'NZD/IDR'
    }

    # Sector display names
    sector_names = {
        'composite': 'Composite (IHSG)', 'idxbasic': 'Basic Materials',
        'idxnoncyc': 'Non-Cyclical', 'idxhealth': 'Healthcare',
        'idxpropert': 'Property', 'idxtechno': 'Technology',
        'idxtrans': 'Transportation', 'idxindust': 'Industrial',
        'idxfinance': 'Finance', 'idxenergy': 'Energy',
        'idxinfra': 'Infrastructure', 'idxcyclic': 'Cyclical'
    }

    currency_cols = list(currency_names.keys())
    sector_cols = list(sector_names.keys())

    return df_fx, df_ihsg, currency_names, sector_names, currency_cols, sector_cols
