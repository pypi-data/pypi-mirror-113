from jh_utils.pandas import sql

def send_data(engine_origin, engine_destiny, destiny_schema, if_exists = 'replace', index=False):
    def output_func(query, table_name):
        df = sql.get_data(query, engine_origin)
        df.to_sql(name=table_name, con=engine_destiny, if_exists = if_exists, schema = destiny_schema, index=False)
    return output_func