from sqlalchemy import create_engine

class Update:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def update_product_description(self, product:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.hub_product
        SET 
        '''
        set_query = ""

        record = product["description"]

        # control keys
        keys_list = [
            "name", "isin_code", "bloomberg_id", "currency"
        ]

        for key in keys_list:

            if key in record.keys(): 
                if key == "name":
                    set_query += f'''{key}_ = '{record[key]}','''
                else: 
                    set_query += f'''{key} = '{record[key]}','''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE product_id = '{record['product_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def update_product_cultures(self, product:dict):

        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.prod_cultures
        SET 
        '''
        set_query = ""

        record = product["cultures"]

        # control keys
        keys_list = [
            "financial_horizon_index", "financial_litteracy_index",
            "financial_experience_index", "risk_propensity_index",
            "esg_propensity_index", "sophisticated_instrument", 
            "marginality_index"
            ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''{key} = {record[key]},'''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE product_id = '{record['product_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def update_product_assets(self, product:dict):

        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.prod_assets
        SET 
        '''
        set_query = ""

        record = product["assets"]

        keys_list = [
            "equity", "balanced", "bond",
            "real_estate", "commodities", "money_market",
            "liquidity"
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f''' {key} = {record[key]},'''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE product_id = '{record['product_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def update_product_needs(self, product:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.prod_needs
        SET 
        '''
        set_query = ""

        record = product["needs"]

        keys_list = [
            'health_insurance_need', 'home_insurance_need', 'longterm_care_insurance_need', 
            'payment_financing_need', 'loan_financing_need', 'mortgage_financing_need', 
            'capital_accumulation_investment_need', 'capital_protection_investment_need',
            'retirement_investment_need', 'income_investment_need', 
            'heritage_investment_need', 'liquidity_investment_need'
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''{key} = {record[key]},'''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE product_id = '{record['product_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def run(self, products:list):

        for product in products:
            
            product_id = product["id"]

            if "description" in product.keys(): 
                product["description"]["product_id"] = product_id
                self.update_product_description(product=product)
                print("description pushed")

            if "cultures" in product.keys(): 
                product["cultures"]["product_id"] = product_id
                self.update_product_cultures(product=product)
                print("cultures pushed")
                
            if "assets" in product.keys(): 
                product["assets"]["product_id"] = product_id
                self.update_product_assets(product=product)
                print("assets pushed")

            if "needs" in product.keys(): 
                product["needs"]["product_id"] = product_id
                self.update_product_needs(product=product)
                print("needs pushed")
                
        return True
