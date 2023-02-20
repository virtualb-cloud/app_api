from sqlalchemy import create_engine

class Update:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def update_portfolio_description(self, portfolio:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.link_portfolio
        SET 
        '''
        set_query = ""

        record = portfolio["description"]

        # control keys
        keys_list = [
            "advisor_id"
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''{key} = '{record[key]}','''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE portfolio_id = '{record['portfolio_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def run(self, portfolios:list):

        for portfolio in portfolios:
            
            portfolio_id = portfolio["id"]

            if "description" in portfolio.keys(): 
                portfolio["description"]["portfolio_id"] = portfolio_id
                self.update_portfolio_description(portfolio=portfolio)
                print("description pushed")
                
        return True
