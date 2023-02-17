from sqlalchemy import create_engine

class Insert_controller:

    def __init__(self) -> None:

        # object to control the sample
        # before adding to enrichment db

        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        
        # portfolio id

        query = f'''
        SELECT portfolio_id
        FROM {self.schema_name}.hub_portfolio
        '''
    
        response = self.engine.connect().execute(query)
        portfolio_ids = response.fetchall()

        self.portfolio_ids = []
        if portfolio_ids == None: self.portfolio_ids = []
        else:
            for item in portfolio_ids:
                self.portfolio_ids.append(item[0])

        # client id

        query = f'''
        SELECT client_id
        FROM {self.schema_name}.hub_customer
        '''
    
        response = self.engine.connect().execute(query)
        client_ids = response.fetchall()

        self.client_ids = []
        if client_ids == None: self.client_ids = []
        else:
            for item in client_ids:
                self.client_ids.append(item[0])

        # advisor id

        query = f'''
        SELECT advisor_id
        FROM {self.schema_name}.hub_advisor
        '''
    
        response = self.engine.connect().execute(query)
        advisor_ids = response.fetchall()

        self.advisor_ids = []
        if advisor_ids == None: self.advisor_ids = []
        else:
            for item in advisor_ids:
                self.advisor_ids.append(item[0])

    
    def first_necessary_keys_controller(self, portfolio:dict):

        # flag & errors
        flag = True
        errors = ""

        mandatory_keys = [
            "id", "client_id", "advisor_id"
        ]
        # controll 
        for key in mandatory_keys:

            if not key in portfolio.keys(): 
                errors += f"try sending a '{key}' for each record. " 
                flag = False
            
        if portfolio["id"] in self.portfolio_ids:
            flag = False
            errors += f"portfolio_id '{portfolio['id']}' exists in db, use update instead. " 

        elif not portfolio["client_id"] in self.client_ids:
            flag = False
            errors += f"client_id '{portfolio['client_id']}' does not exist in db. " 

        elif not portfolio["advisor_id"] in self.advisor_ids:
            flag = False
            errors += f"advisor_id '{portfolio['advisor_id']}' does not exist in db. " 

        return flag, errors
    
    def run(self, portfolios:list):

        # flag & errors
        flag = True
        errors = ""

        if type(portfolios) != list:
            flag = False
            errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
            return flag, errors
        
        for portfolio in portfolios:
            
            if type(portfolio) != dict:
                flag = False
                errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
                return flag, errors
            
            all_keys = ["id", "client_id", "advisor_id"]
            for key in portfolio.keys():
                if not key in all_keys:
                    flag = False
                    errors += f"try sending only '{all_keys}' as record dictionary keys. "
                    return flag, errors
                
            # necessary keys
            flag, errs = self.first_necessary_keys_controller(portfolio=portfolio)
            if not flag: 
                errors += errs
                return flag, errors

        return flag, errors