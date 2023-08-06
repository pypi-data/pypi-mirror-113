from jh_utils.pandas import sql

def send_data(engine_origin, engine_destiny, destiny_schema, if_exists = 'replace', index=False):
    def output_func(query, table_name):
        df = sql.get_data(query, engine_origin)
        sql.write_table(df, table_name, destiny_schema, engine_destiny, if_exists = 'replace', chunksize = 10_000, index= False, close_connection = False)
    return output_func