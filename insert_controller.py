from sqlalchemy import create_engine

class Insert_controller:

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
    
        response = self.engine.connect().execute(query)
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
        
        elif product["id"] in self.product_ids:
            flag = False
            errors += f"product_id '{product['id']}' exists in db, use update instead. " 

        # controll "description"
        elif not "description" in product.keys(): 
            flag = False
            errors += "try sending description dictionary for each record. " 

        return flag, errors

    def first_optional_keys_controller(self, product:dict):

        flags = {
            "assets" : False,
            "cultures" : False,
            "needs" : False
            } 

        if "cultures" in product.keys(): flags["cultures"] = True
        if "assets" in product.keys(): flags["assets"] = True
        if "needs" in product.keys(): flags["needs"] = True

        return flags
        
    def description_keys_controller(self, product:dict):
        
        # mandatory variables
        mandatory_keys = [
            "name", "isin_code", "bloomberg_id", "currency"
        ]

        # flag & errors
        flag = True
        errors = ""

        # flag True means to have necessary input data
        flag = True

        # check if necessary keys exist
        for key in mandatory_keys :
            if not key in product["description"].keys(): 
                flag = False
                errors += f"try sending '{key}' as a description dictionary key. "

        return flag, errors

    def cultures_controller(self, product:dict):
        
        # optional variables
        optional_keys = [
            "financial_horizon_index", "finacial_littercay_index", 
            "financial_experience_index", "risk_propensity_index", 
            "esg_propensity_index", "sophisticated_instrument", 
            "marginality_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        if product["cultures"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as cultures dictionary keys. "

        for key in product["cultures"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as cultures dictionary keys. "

            elif not type(product["cultures"][key]) in [int, float]:
                flag = False
                errors += "try sending a value in [0, 1] range as cultures dictionary values. "

            elif (product["cultures"][key] < 0) | (product["cultures"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as cultures dictionary values. "

        return flag, errors

    def assets_controller(self, product:dict):
        
        # optional variables
        optional_keys = [
            "equity", "balanced", "bond",
            "real_estate", "commodities", "money_market",
            "liquidity"
        ]

        # flag & errors
        flag = True
        errors = ""

        if product["assets"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as assets dictionary keys. "

        sum = 0
        for key in product["assets"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as assets dictionary keys. "

            elif not type(product["assets"][key]) in [int, float]:
                flag = False
                errors += "try sending a value in [0, 1] range as assets dictionary values. "

            elif (product["assets"][key] < 0) | (product["assets"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as assets dictionary values. "

            else:
                sum += product["assets"][key]

        # last check
        if sum != 1:
            flag = False
            errors += f"assets should sum up to one. "

        return flag, errors
            
    def needs_controller(self, product:dict):
        
        # optional variables
        optional_keys = [
            "capital_accumulation_investment_need", "capital_protection_investment_need", 
            "liquidity_investment_need", "income_investment_need",
            "retirement_investment_need", "heritage_investment_need",
            "health_incurance_need", "home_insurance_need",
            "longterm_care_insurance_need", "payment_financing_need",
            "loan_financing_need", "mortgage_financing_need"
        ]

        # flag & errors
        flag = True
        errors = ""

        if product["needs"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as needs dictionary keys. "

        sum = 0
        for key in product["needs"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as needs dictionary keys. "

            elif not type(product["needs"][key]) in [int, float]:
                flag = False
                errors += "try sending a value in [0, 1] range as needs dictionary values. "


            elif (product["needs"][key] < 0) | (product["needs"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as needs dictionary values. "

            else:
                sum += product["needs"][key]

        # last check
        if sum != 1:
            flag = False
            errors += f"needs should sum up to one. "

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

            # control description keys and values
            flag, errors = self.description_keys_controller(product=product)
            if not flag: 
                errors += errs 
                errors +=f"error seen at id = '{product_id}'. "
                return flag, errors

            # optional keys
            flags = self.first_optional_keys_controller(product=product)
            
            # control cultures if exists
            if flags["cultures"]:
                flag, errors = self.cultures_controller(product=product)
                if not flag: 
                    errors += errs
                    errors += f"error seen at id = '{product_id}'. "
                    return flag, errors

            # control assets if exists
            if flags["assets"]:
                flag, errors = self.assets_controller(product=product)
                if not flag: 
                    errors += errs
                    errors += f"error seen at id = '{product_id}'. "
                    return flag, errors
            
            # control needs if exists
            if flags["needs"]:
                flag, errors = self.needs_controller(product=product)
                if not flag: 
                    errors += errs
                    errors += f"error seen at id = '{product_id}'. "
                    return flag, errors

        return flag, errors