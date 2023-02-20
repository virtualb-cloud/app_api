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
        FROM {self.schema_name}.link_portfolio
        '''
    
        response = self.engine.connect().execute(query)
        portfolio_ids = response.fetchall()

        self.portfolio_ids = []
        if portfolio_ids == None: self.portfolio_ids = []
        else:
            for item in portfolio_ids:
                self.portfolio_ids.append(item[0])

        # customer id

        query = f'''
        SELECT customer_id
        FROM {self.schema_name}.hub_customer
        '''
    
        response = self.engine.connect().execute(query)
        customer_ids = response.fetchall()

        self.customer_ids = []
        if customer_ids == None: self.customer_ids = []
        else:
            for item in customer_ids:
                self.customer_ids.append(item[0])

        # portfolio id

        query = f'''
        SELECT portfolio_id
        FROM {self.schema_name}.link_portfolio
        '''
    
        response = self.engine.connect().execute(query)
        portfolio_ids = response.fetchall()

        self.portfolio_ids = []
        if portfolio_ids == None: self.portfolio_ids = []
        else:
            for item in portfolio_ids:
                self.portfolio_ids.append(item[0])


    def first_necessary_keys_controller(self, portfolio:dict):

        # flag & errors
        flag = True
        errors = ""

        mandatory_keys = [
            "id"
        ]
        # controll 
        for key in mandatory_keys:

            if not key in portfolio.keys(): 
                errors += f"try sending a '{key}' for each record. " 
                flag = False
            
        if portfolio["id"] in self.portfolio_ids:
            flag = False
            errors += f"portfolio_id '{portfolio['id']}' exists in db, use update instead. " 


        return flag, errors

    def first_optional_keys_controller(self, portfolio:dict):

        flags = {
            "description" : False
            } 

        if "description" in portfolio.keys(): flags["description"] = True

        return flags
        
    def description_keys_controller(self, portfolio:dict):
        
        # mandatory variables
        optional_keys = [
            "customer_id", "advisor_id"
        ]

        # flag & errors
        flag = True
        errors = ""

        for key in portfolio["description"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as description dictionary keys. "

            elif not type(portfolio["description"][key]) in [str]:
                flag = False
                errors += "try sending a string value as description dictionary values. "
            
            if key == "customer_id":
                if not portfolio["description"][key] in self.customer_ids:
                    flag = False
                    errors += f"customer_id '{portfolio['description'][key]}' does not exist in db. " 
            
            if key == "portfolio_id":
                if not portfolio["description"][key] in self.portfolio_ids:
                    flag = False
                    errors += f"portfolio_id '{portfolio['description'][key]}' does not exist in db. " 

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
            
            all_keys = ["id", "description"]
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

            flags = self.first_optional_keys_controller(portfolio=portfolio)
            
            if flags["description"]:
                flag, errs = self.description_keys_controller(portfolio=portfolio)
                if not flag: 
                    errors += errs
                    return flag, errors

        return flag, errors