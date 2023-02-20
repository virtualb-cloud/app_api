from sqlalchemy import create_engine

class Read:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
    
    def description(self, ids:list):

        query = f'''
        SELECT portfolio_id, advisor_id, customer_id

        FROM {self.schema_name}.hub_portfolio
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE portfolio_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE portfolio_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_portfolios = {}
        for portfolio in data:

            id = portfolio[0]

            new_portfolios[id] = {
                "advisor_id" : portfolio[1],
                "customer_id" : portfolio[2]
                }

        return new_portfolios

    def run(self, body:dict):

        ids = body["ids"]

        categories = body["categories"]

        flags = {
            "description" : False
            }

        if categories == []:
            
            flags["description"] = True
            portfolios_desc = self.description(ids=ids)
            final_keys = portfolios_desc.keys()

        if "description" in categories:
            flags["description"] = True
            portfolios_desc = self.description(ids=ids)
            final_keys = portfolios_desc.keys()
        
        portfolios = []

        for id in final_keys:
            
            portfolio = {
                "id" : id
            } 

            if flags["description"]: portfolio["description"] = portfolios_desc[id]

            portfolios.append(portfolio)

        return portfolios