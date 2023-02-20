from sqlalchemy import create_engine

class Insert:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def insert_portfolios(self, portfolios:list):
        
        # prepare fixed query
        query = f'''
            INSERT INTO {self.schema_name}.hub_portfolio(
                portfolio_id, customer_id, advisor_id
            )
            VALUES '''
        
        keys_list = [
            "customer_id", "advisor_id"
        ]
        # add the data to query
        for portfolio in portfolios:
            
            portfolio_id = portfolio["id"]

            add_statement = f'''('{portfolio_id}','''

            # control keys
            for key in keys_list:
                add_statement += f''' '{portfolio[key]}','''

            # to exclude the last ","
            query = query + add_statement[:-1] + "),"

        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            conn.execute(statement=query)

        return True

    def run(self, portfolios:list):

        self.insert_portfolios(portfolios=portfolios)
        print("description pushed")

        return True
