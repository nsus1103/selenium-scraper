import pandas as pd
import os
from sqlalchemy import create_engine

def parse_html_to_db(filestore):
    files = os.listdir(filestore)
    df = pd.DataFrame()

    for file in files:
        filepath = filestore + f'\\{file}'
        temp_df = pd.read_html(filepath)
        df.append(temp_df[0])

        # write df to sql database
        engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
        df.to_sql('table_name', engine)

        # # write df to csv
        # df.to_csv(f'{file}.csv')

        return