from sqlalchemy import create_engine

class Read:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
    
    def socio_demographics(self, ids:list):

        query = f'''
        SELECT customer_id, age_, gender_, location_, education_, profession_

        FROM {self.schema_name}.hub_customer
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE customer_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE customer_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_customers = {}
        for customer in data:

            id = customer[0]

            new_customers[id] = {
                "age" : customer[1],
                "gender" : customer[2],
                "location" : customer[3],
                "education" : customer[4],
                "profession" : customer[5]
                }

        return new_customers

    def needs(self, ids:list):
        
        query = f'''
        SELECT customer_id,
        health_insurance_need, home_insurance_need, longterm_care_insurance_need, 
        payment_financing_need, loan_financing_need, mortgage_financing_need, 
        capital_accumulation_investment_need, capital_protection_investment_need,
        retirement_investment_need, income_investment_need, 
        heritage_investment_need, liquidity_investment_need

        FROM {self.schema_name}.cust_needs
        '''

        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE customer_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE customer_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_customers = {}
        for customer in data:
            
            id = customer[0]

            new_customers[id] = {
                'health_insurance_need' : customer[1], 
                'home_insurance_need' : customer[2], 
                'longterm_care_insurance_need' : customer[3], 
                'payment_financing_need' : customer[4], 
                'loan_financing_need' : customer[5], 
                'mortgage_financing_need' : customer[6], 
                'capital_accumulation_investment_need' : customer[7], 
                'capital_protection_investment_need' : customer[8],
                'retirement_investment_need' : customer[9], 
                'income_investment_need' : customer[10], 
                'heritage_investment_need' : customer[11], 
                'liquidity_investment_need' : customer[12]
            }
            
        return new_customers

    def status(self, ids:list):
        
        query = f'''
        SELECT customer_id, 
        real_assets_index, financial_assets_index,
        net_liabilities_index, net_wealth_index,
        net_income_index, net_savings_index,
        net_expences_index

        FROM {self.schema_name}.cust_status
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE customer_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE customer_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_customers = {}
        for customer in data:
            
            id = customer[0]

            new_customers[id] = {
                "real_assets_index" : customer[1], 
                "financial_assets_index" : customer[2],
                "net_liabilities_index" : customer[3], 
                "net_wealth_index" : customer[4],
                "net_income_index" : customer[5], 
                "net_savings_index" : customer[6],
                "net_expences_index" : customer[7]
                }
                
            
        return new_customers

    def attitudes(self, ids:list):
        
        query = f'''
        SELECT customer_id,
        bank_activity_index, digital_activity_index,
        cultural_activity_index, charity_activity_index

        FROM {self.schema_name}.cust_attitudes
        '''

        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE customer_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE customer_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_customers = {}
        for customer in data:
            
            id = customer[0]
                
            new_customers[id] = {
                "bank_activity_index" : customer[1], 
                "digital_activity_index" : customer[2],
                "cultural_activity_index" : customer[3], 
                "charity_activity_index" : customer[4]
                }
            
        return new_customers
   
    def cultures(self, ids:list):
        
        query = f'''
        SELECT customer_id,
        financial_horizon_index, financial_litteracy_index, 
        financial_experience_index, objective_risk_propensity_index, 
        subjective_risk_propensity_index, esg_propensity_index,
        life_quality_index, sophisticated_instrument, marginality_index

        FROM {self.schema_name}.cust_cultures
        '''

        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE customer_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE customer_id in {tuple(ids)}
            '''
        data = self.engine.connect().execute(statement=query)

        new_customers = {}
        for customer in data:
            
            id = customer[0]

            new_customers[id] = {
                "financial_horizon_index" : customer[1], 
                "financial_litteracy_index" : customer[2],
                "financial_experience_index" : customer[3], 
                "objective_risk_propensity_index" : customer[4],
                "subjective_risk_propensity_index" : customer[5], 
                "esg_propensity_index" : customer[6],
                "life_quality_index" : customer[7],
                "sophisticated_instrument" : customer[8], 
                "marginality_index" : customer[9]
                }
            
        return new_customers

    def run(self, body:dict):

        ids = body["ids"]

        categories = body["categories"]

        flags = {
            "sociodemographics" : False,
            "status" : False,
            "cultures" : False,
            "attitudes" : False,
            "needs" : False
            }

        if categories == []:
            
            flags["sociodemographics"] = True
            customers_sociodemo = self.socio_demographics(ids=ids)
            final_keys = customers_sociodemo.keys()

            flags["cultures"] = True
            customers_cultures = self.cultures(ids=ids)

            flags["status"] = True
            customers_status = self.status(ids=ids)

            flags["needs"] = True
            customers_needs = self.needs(ids=ids)

            flags["attitudes"] = True
            customers_attitudes = self.attitudes(ids=ids)

        if "sociodemographics" in categories:
            flags["sociodemographics"] = True
            customers_sociodemo = self.socio_demographics(ids=ids)
            final_keys = customers_sociodemo.keys()
            
        if "cultures" in categories:
            flags["cultures"] = True
            customers_cultures = self.cultures(ids=ids)
            final_keys = customers_cultures.keys()
            
        if "status" in categories:
            flags["status"] = True
            customers_status = self.status(ids=ids)
            final_keys = customers_status.keys()
        
        if "needs" in categories:
            flags["needs"] = True
            customers_needs = self.needs(ids=ids)
            final_keys = customers_needs.keys()

        if "attitudes" in categories:
            flags["attitudes"] = True
            customers_attitudes = self.attitudes(ids=ids)
            final_keys = customers_attitudes.keys()

        customers = []

        for id in final_keys:
            
            customer = {
                "id" : id
            } 

            if flags["sociodemographics"]: customer["sociodemographics"] = customers_sociodemo[id]
            if flags["cultures"]: customer["cultures"] = customers_cultures[id]
            if flags["status"]: customer["status"] = customers_status[id]
            if flags["needs"]: customer["needs"] = customers_needs[id]
            if flags["attitudes"]: customer["attitudes"] = customers_attitudes[id]
            
            customers.append(customer)

        return customers