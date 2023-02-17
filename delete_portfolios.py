from sqlalchemy import create_engine

class Delete:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")

    def run(self, body:dict):

        ids = body["ids"]

        if len(ids) == 1:

            query = f'''
            DELETE FROM {self.schema_name}.hub_portfolio
            WHERE portfolio_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:

            query = f'''
            DELETE FROM {self.schema_name}.hub_portfolio
            WHERE portfolio_id in {tuple(ids)}
            '''

        self.engine.connect().execute(statement=query)
  
        return True
