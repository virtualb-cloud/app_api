from sqlalchemy import create_engine

class Read:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
    
    def description(self, ids:list):

        query = f'''
        SELECT product_id, name_, isin_code, bloomberg_id, currency

        FROM {self.schema_name}.hub_product
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE product_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE product_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_products = {}
        for product in data:

            id = product[0]

            new_products[id] = {
                "name" : product[1],
                "isin_code" : product[2],
                "bloomberg_id" : product[3],
                "currency" : product[4]
                }

        return new_products

    def needs(self, ids:list):
        
        query = f'''
        SELECT product_id,
        health_insurance_need, home_insurance_need, longterm_care_insurance_need, 
        payment_financing_need, loan_financing_need, mortgage_financing_need, 
        capital_accumulation_investment_need, capital_protection_investment_need,
        retirement_investment_need, income_investment_need, 
        heritage_investment_need, liquidity_investment_need

        FROM {self.schema_name}.prod_needs
        '''

        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE product_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE product_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_products = {}
        for product in data:
            
            id = product[0]

            new_products[id] = {
                'health_insurance_need' : product[1], 
                'home_insurance_need' : product[2], 
                'longterm_care_insurance_need' : product[3], 
                'payment_financing_need' : product[4], 
                'loan_financing_need' : product[5], 
                'mortgage_financing_need' : product[6], 
                'capital_accumulation_investment_need' : product[7], 
                'capital_protection_investment_need' : product[8],
                'retirement_investment_need' : product[9], 
                'income_investment_need' : product[10], 
                'heritage_investment_need' : product[11], 
                'liquidity_investment_need' : product[12]
            }
            
        return new_products

    def assets(self, ids:list):
        
        query = f'''
        SELECT product_id, 
        equity_index, balanced_index,
        bond_index, real_estate_index,
        commodity_index, money_market_index,
        liquidity_index

        FROM {self.schema_name}.prod_assets
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE product_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE product_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_products = {}
        for product in data:
            
            id = product[0]

            new_products[id] = {
                "equity_index" : product[1], 
                "balanced_index" : product[2],
                "bond_index" : product[3], 
                "real_estate_index" : product[4],
                "commodity_index" : product[5], 
                "money_market_index" : product[6],
                "liquidity_index" : product[7]
                }
                
            
        return new_products

    def cultures(self, ids:list):
        
        query = f'''
        SELECT product_id,
        financial_horizon_index, financial_litteracy_index, 
        financial_experience_index, risk_propensity_index, 
        esg_propensity_index,
        sophisticated_instrument, marginality_index

        FROM {self.schema_name}.prod_cultures
        '''

        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE product_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE product_id in {tuple(ids)}
            '''
        data = self.engine.connect().execute(statement=query)

        new_products = {}
        for product in data:
            
            id = product[0]

            new_products[id] = {
                "financial_horizon_index" : product[1], 
                "financial_litteracy_index" : product[2],
                "financial_experience_index" : product[3], 
                "risk_propensity_index" : product[4],
                "esg_propensity_index" : product[5],
                "sophisticated_instrument" : product[6], 
                "marginality_index" : product[7]
                }
            
        return new_products

    def run(self, body:dict):

        ids = body["ids"]

        categories = body["categories"]

        flags = {
            "description" : False,
            "assets" : False,
            "cultures" : False,
            "needs" : False
            }

        if categories == []:
            
            flags["description"] = True
            products_desc = self.description(ids=ids)
            final_keys = products_desc.keys()

            flags["cultures"] = True
            products_cultures = self.cultures(ids=ids)

            flags["assets"] = True
            products_assets = self.assets(ids=ids)

            flags["needs"] = True
            products_needs = self.needs(ids=ids)

        if "description" in categories:
            flags["description"] = True
            products_desc = self.description(ids=ids)
            final_keys = products_desc.keys()
        
        if "cultures" in categories:
            flags["cultures"] = True
            products_cultures = self.cultures(ids=ids)
            final_keys = products_cultures.keys()

        if "assets" in categories:
            flags["assets"] = True
            products_assets = self.assets(ids=ids)
            final_keys = products_assets.keys()
        
        if "needs" in categories:
            flags["needs"] = True
            products_needs = self.needs(ids=ids)
            final_keys = products_needs.keys()

        products = []

        for id in final_keys:
            
            product = {
                "id" : id
            } 

            if flags["description"]: product["description"] = products_desc[id]
            if flags["cultures"]: product["cultures"] = products_cultures[id]
            if flags["assets"]: product["assets"] = products_assets[id]
            if flags["needs"]: product["needs"] = products_needs[id]
            
            products.append(product)

        return products