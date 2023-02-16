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

        new_people = {}
        for product in data:

            id = product[0]

            new_people[id] = {
                "name" : product[1],
                "isin_code" : product[2],
                "bloomberg_id" : product[3],
                "currency" : product[4]
                }

        return new_people

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

        new_people = {}
        for product in data:
            
            id = product[0]

            new_people[id] = {
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
            
        return new_people

    def assets(self, ids:list):
        
        query = f'''
        SELECT product_id, 
        equity, balanced,
        bond, real_estate,
        commodities, money_market,
        liquidity

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

        new_people = {}
        for product in data:
            
            id = product[0]

            new_people[id] = {
                "equity" : product[1], 
                "balanced" : product[2],
                "bond" : product[3], 
                "real_estate" : product[4],
                "commodities" : product[5], 
                "money_market" : product[6],
                "liquidity" : product[7]
                }
                
            
        return new_people

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

        new_people = {}
        for product in data:
            
            id = product[0]

            new_people[id] = {
                "financial_horizon_index" : product[1], 
                "financial_litteracy_index" : product[2],
                "financial_experience_index" : product[3], 
                "risk_propensity_index" : product[4],
                "esg_propensity_index" : product[5],
                "sophisticated_instrument" : product[6], 
                "marginality_index" : product[7]
                }
            
        return new_people

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
            people_sociodemo = self.description(ids=ids)

            flags["cultures"] = True
            people_cultures = self.cultures(ids=ids)

            flags["assets"] = True
            people_assets = self.assets(ids=ids)

            flags["needs"] = True
            people_needs = self.needs(ids=ids)

        if "description" in categories:
            flags["description"] = True
            people_sociodemo = self.description(ids=ids)
        
        if "cultures" in categories:
            flags["cultures"] = True
            people_cultures = self.cultures(ids=ids)

        if "assets" in categories:
            flags["assets"] = True
            people_assets = self.assets(ids=ids)
        
        if "needs" in categories:
            flags["needs"] = True
            people_needs = self.needs(ids=ids)

        people = []

        for id in people_sociodemo.keys():
            
            product = {
                "id" : id
            } 

            if flags["description"]: product["description"] = people_sociodemo[id]
            if flags["cultures"]: product["cultures"] = people_cultures[id]
            if flags["assets"]: product["assets"] = people_assets[id]
            if flags["needs"]: product["needs"] = people_needs[id]
            
            people.append(product)

        return people