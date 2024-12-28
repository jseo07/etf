import plotly.express as px
import pandas as pd
import yfinance as yf
from tableauhyperapi import HyperProcess, Connection, TableDefinition, SqlType, Telemetry, CreateMode, Inserter
import tableauserverclient as tsc


##############################################
# API FUNCTIONALITY
##############################################
API_KEY = 'CPI98ICU61YJ90Z9'

site_id = "jang079-d24d6284f0"
username = "jang079@student.ubc.ca"
password = "Kids7741@"
server_url = "https://prod-ca-a.online.tableau.com" 
data_source_name = "data"
HYPER_FILE_PATH = "data.hyper"

#returns df
def request_data(symbol):
    dat = yf.Ticker(symbol)
    dat= dat.history(period="max", interval="1d")
    dat.reset_index(inplace=True)
    dat['Date'] = pd.to_datetime(dat['Date'])
    return dat

def search_auto(keyword):
    uncleaned = yf.Search(keyword, max_results=8, news_count=0).quotes
    return clean_search_data(uncleaned)

def clean_search_data(data):
    cleaned_data = [
    {"symbol": d.get("symbol"), "name": d.get("longname")} 
    for d in data
    ]
    return cleaned_data

def dataframe_to_hyper(df, table_name, hyper_name):
    if df.shape[0] == 0:
        print("df no rows")
        pass
    else:
        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(endpoint=hyper.endpoint, database=hyper_name, create_mode=CreateMode.NONE) as connection:

                extract_tables = connection.catalog.get_table_names(schema="Extract")
                public_tables = connection.catalog.get_table_names(schema="public")
                
                # Drop each table
                for table in extract_tables + public_tables:
                    drop_table_command = f"DROP TABLE IF EXISTS {table};"
                    connection.execute_command(drop_table_command)


                columns = []
                for col_name in df.columns:
                    if df[col_name].dtype == '0':
                        col_type = SqlType.text()
                    elif pd.api.types.is_datetime64_any_dtype(df[col_name]):
                        col_type = SqlType.timestamp()
                    else:
                        col_type = SqlType.double()
                    columns.append(TableDefinition.Column(name=col_name, type=col_type))
                table_definition = TableDefinition(table_name = table_name, columns=columns)
                connection.catalog.create_table(table_definition)

                print(f"Number of rows in DataFrame: {len(df)}")

                with Inserter(connection, table_definition) as inserter:
                    inserter.add_rows(rows=df.values)
                    inserter.execute()
        
        try:
            tableau_auth = tsc.TableauAuth(username, password, site_id=site_id)
            server = tsc.Server(server_url, use_server_version=True)

            with server.auth.sign_in(tableau_auth):
                all_datasources, pagination_item = server.datasources.get()
                datasource = next(
                    (ds for ds in all_datasources if ds.name == data_source_name), None
                )

                if datasource is None:
                    print(f"Data source '{data_source_name}' not found on the server.")
                    return
                print(f"Found data source: {datasource.name} (ID: {datasource.id})")

                new_ds_item = tsc.DatasourceItem(
                    project_id=datasource.project_id,
                    name=data_source_name
                )

                server.datasources.publish(
                    new_ds_item,
                    HYPER_FILE_PATH,
                    tsc.Server.PublishMode.Overwrite
                )

                print(f"Data source '{data_source_name}' successfully replaced.")
        except Exception as e:
            print(f"An error occurred: {e}")