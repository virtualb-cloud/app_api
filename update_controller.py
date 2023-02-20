from sqlalchemy import create_engine

class Update_controller:

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
    
        response = self.engine.connect().execute(statement=query)
        portfolio_ids = response.fetchall()

        self.portfolio_ids = []
        if portfolio_ids == None: self.portfolio_ids = []
        else:
            for item in portfolio_ids:
                self.portfolio_ids.append(item[0])

        # advisor_id
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

        # controll "id"

        if not "id" in portfolio.keys(): 
            errors += "try sending an id for each record. " 
            flag = False
        
        elif not portfolio["id"] in self.portfolio_ids:
            flag = False
            errors += f"portfolio_id '{portfolio['id']}' does not exist in db. " 

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

        if portfolio["description"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as description dictionary keys. "

        for key in portfolio["description"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending only '{optional_keys}' as description dictionary keys. "

            elif not type(portfolio["description"][key]) in [str]:
                flag = False
                errors += "try sending a string as description dictionary values. "

            if key == "customer_id" :
                flag = False
                errors += "customer_id is not updatable, try creating a new portfolio. "

            if key == "advisor_id" :
                if not portfolio["description"][key] in self.advisor_ids:
                    flag = False
                    errors += f"advisor_id '{portfolio['description'][key]}' does not exist in db. "


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
            else:
                portfolio_id = portfolio["id"]

            # optional keys
            flags = self.first_optional_keys_controller(portfolio=portfolio)
            
            sign = 0
            for k, v in flags.items():
                if v == True: sign = 1
            
            if sign == 0:
                flag = False
                errors = f"try sending at least one of '{all_keys[1:]}'. "
                errors +=  f"error seen at id = '{portfolio_id}'. "
                return flag, errors

            # control description if exists
            if flags["description"]:

                # control description keys
                flag, errors = self.description_keys_controller(portfolio=portfolio)
                if not flag: 
                    errors += errs 
                    errors +=  f"error seen at id = '{portfolio_id}'. "
                    return flag, errors

        return flag, errors