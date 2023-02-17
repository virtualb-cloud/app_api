from sqlalchemy import create_engine

class Update_controller:

    def __init__(self) -> None:

        # object to control the sample
        # before adding to enrichment db

        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        
        # product id
        query = f'''
        SELECT product_id
        FROM {self.schema_name}.hub_product
        '''
    
        response = self.engine.connect().execute(statement=query)
        product_ids = response.fetchall()

        self.product_ids = []
        if product_ids == None: self.product_ids = []
        else:
            for item in product_ids:
                self.product_ids.append(item[0])
    
    def first_necessary_keys_controller(self, product:dict):

        # flag & errors
        flag = True
        errors = ""

        # controll "id"

        if not "id" in product.keys(): 
            errors += "try sending an id for each record. " 
            flag = False
        
        elif not product["id"] in self.product_ids:
            flag = False
            errors += f"product_id '{product['id']}' does not exist in db. " 

        return flag, errors

    def first_optional_keys_controller(self, product:dict):

        flags = {
            "description" : False
            } 

        if "description" in product.keys(): flags["description"] = True

        return flags
        
    def description_keys_controller(self, product:dict):
        
        # mandatory variables
        optional_keys = [
            "classification_index", "qualification_index", "diversification_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        if product["description"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as description dictionary keys. "

        for key in product["description"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending only '{optional_keys}' as description dictionary keys. "

            elif not type(product["description"][key]) in [str]:
                flag = False
                errors += "try sending a string as description dictionary values. "

        return flag, errors

    def run(self, products:list):

        # flag & errors
        flag = True
        errors = ""

        if type(products) != list:
            flag = False
            errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
            return flag, errors
        
        for product in products:
            
            if type(product) != dict:
                flag = False
                errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
                return flag, errors
            
            all_keys = ["id", "description", "cultures", "assets", "needs"]
            for key in product.keys():
                if not key in all_keys:
                    flag = False
                    errors += f"try sending only '{all_keys}' as record dictionary keys. "
                    return flag, errors
                
            # necessary keys
            flag, errs = self.first_necessary_keys_controller(product=product)
            if not flag: 
                errors += errs
                return flag, errors
            else:
                product_id = product["id"]

            # optional keys
            flags = self.first_optional_keys_controller(product=product)
            
            sign = 0
            for k, v in flags.items():
                if v == True: sign = 1
            
            if sign == 0:
                flag = False
                errors = f"try sending at least one of '{all_keys[1:]}'. "
                errors +=  f"error seen at id = '{product_id}'. "
                return flag, errors

            # control description if exists
            if flags["description"]:

                # control description keys
                flag, errors = self.description_keys_controller(product=product)
                if not flag: 
                    errors += errs 
                    errors +=  f"error seen at id = '{product_id}'. "
                    return flag, errors

        return flag, errors