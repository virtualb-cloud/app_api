from sqlalchemy import create_engine

class Update_controller:

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
    
        response = self.engine.connect().execute(statement=query)
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
    
        response = self.engine.connect().execute(statement=query)
        portfolio_ids = response.fetchall()

        self.portfolio_ids = []
        if portfolio_ids == None: self.portfolio_ids = []
        else:
            for item in portfolio_ids:
                self.portfolio_ids.append(item[0])

        # product_id
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

        # controll "id"

        if not "id" in position.keys(): 
            errors += "try sending an id for each record. " 
            flag = False
        
        elif not position["id"] in self.position_ids:
            flag = False
            errors += f"position_id '{position['id']}' does not exist in db. " 

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

        if position["description"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as description dictionary keys. "

        for key in position["description"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending only '{optional_keys}' as description dictionary keys. "

            elif not type(position["description"][key]) in [str]:
                flag = False
                errors += "try sending a string as description dictionary values. "

            if key == "portfolio_id" :
                if not position["description"][key] in self.portfolio_ids:
                    flag = False
                    errors += f"portfolio_id '{position['description'][key]}' does not exist in db. "

            if key == "product_id" :
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
            else:
                position_id = position["id"]

            # optional keys
            flags = self.first_optional_keys_controller(position=position)
            
            sign = 0
            for k, v in flags.items():
                if v == True: sign = 1
            
            if sign == 0:
                flag = False
                errors = f"try sending at least one of '{all_keys[1:]}'. "
                errors +=  f"error seen at id = '{position_id}'. "
                return flag, errors

            # control description if exists
            if flags["description"]:

                # control description keys
                flag, errors = self.description_keys_controller(position=position)
                if not flag: 
                    errors += errs 
                    errors +=  f"error seen at id = '{position_id}'. "
                    return flag, errors

        return flag, errors