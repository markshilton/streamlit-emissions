import pandas as pd

def format_worksheet(xlsx, sheet):
        df = pd.read_excel(xlsx, sheet)
        
        column_names = [col.strip()
                          .lower()
                          .replace(' ', '_')
                          .replace('(', '')
                          .replace(')', '') for col in df.columns]
        
        df.columns = column_names
        
        df = df[[col for col in column_names if 'unnamed' not in col]]
        
        df['emission_group'] = sheet.lower().replace(' ', '_')

        return df

def format_dataframe(df):
    print('Formatting dataframe')
    df.date = pd.to_datetime(df.date)   
    df.month = df.date.dt.to_period('M').astype('str')
    df.scope = df.scope.astype('str')

    return df

if __name__ == '__main__':
    infile = pd.ExcelFile('Mordor LLC Emissions Calculations Report 08-12-2021.xlsx')
    outfile = 'data.csv'

    df = pd.DataFrame()
    sheets = infile.sheet_names

    for sheet in sheets:
        if sheet != 'Notes':
            print(f"Formatting worksheet: {sheet}")
            temp_df = format_worksheet(infile, sheet)        
            df = pd.concat([df, temp_df], ignore_index=True)


    df = format_dataframe(df)
    df.to_csv(outfile)
    print(f"Data processed and saved to {outfile}")