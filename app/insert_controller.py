from sqlalchemy import create_engine

class Insert_controller:

    def __init__(self) -> None:

        # object to control the sample
        # before adding to enrichment db

        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        
        # position id
        query = f'''
        SELECT position_id
        FROM {self.schema_name}.link_position
        '''
    
        response = self.engine.connect().execute(query)
        position_ids = response.fetchall()

        self.position_ids = []
        if position_ids == None: self.position_ids = []
        else:
            for item in position_ids:
                self.position_ids.append(item[0])

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

        # product id
        query = f'''
        SELECT product_id
        FROM {self.schema_name}.hub_product
        '''
    
        response = self.engine.connect().execute(query)
        product_ids = response.fetchall()

        self.product_ids = []
        if product_ids == None: self.product_ids = []
        else:
            for item in product_ids:
                self.product_ids.append(item[0])

    def first_necessary_keys_controller(self, position:dict):

        # flag & errors
        flag = True
        errors = ""

        mandatory_keys = [
            "id"
        ]
        # controll 
        for key in mandatory_keys:

            if not key in position.keys(): 
                errors += f"try sending a '{key}' for each record. " 
                flag = False
            
        if position["id"] in self.position_ids:
            flag = False
            errors += f"position_id '{position['id']}' exists in db, use update instead. " 


        return flag, errors

    def first_optional_keys_controller(self, position:dict):

        flags = {
            "description" : False
            } 

        if "description" in position.keys(): flags["description"] = True

        return flags
        
    def description_keys_controller(self, position:dict):
        
        # mandatory variables
        optional_keys = [
            "portfolio_id", "product_id"
        ]

        # flag & errors
        flag = True
        errors = ""

        for key in position["description"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as description dictionary keys. "

            elif not type(position["description"][key]) in [str]:
                flag = False
                errors += "try sending a string value as description dictionary values. "
            
            if key == "portfolio_id":
                if not position["description"][key] in self.portfolio_ids:
                    flag = False
                    errors += f"portfolio_id '{position['description'][key]}' does not exist in db. " 
            
            if key == "product_id":
                if not position["description"][key] in self.product_ids:
                    flag = False
                    errors += f"product_id '{position['description'][key]}' does not exist in db. " 

        return flag, errors

    def run(self, positions:list):

        # flag & errors
        flag = True
        errors = ""

        if type(positions) != list:
            flag = False
            errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
            return flag, errors
        
        for position in positions:
            
            if type(position) != dict:
                flag = False
                errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
                return flag, errors
            
            all_keys = ["id", "description"]
            for key in position.keys():
                if not key in all_keys:
                    flag = False
                    errors += f"try sending only '{all_keys}' as record dictionary keys. "
                    return flag, errors
                
            # necessary keys
            flag, errs = self.first_necessary_keys_controller(position=position)
            if not flag: 
                errors += errs
                return flag, errors

            flags = self.first_optional_keys_controller(position=position)
            
            if flags["description"]:
                flag, errs = self.description_keys_controller(position=position)
                if not flag: 
                    errors += errs
                    return flag, errors

        return flag, errors