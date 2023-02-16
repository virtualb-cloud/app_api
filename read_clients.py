from sqlalchemy import create_engine

class Read:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
    
    def socio_demographics(self, ids:list):

        query = f'''
        SELECT person_id, age_, gender_, location_, education_, profession_

        FROM {self.schema_name}.hub_customer
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE person_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE person_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_people = {}
        for person in data:

            id = person[0]

            new_people[id] = {
                "age" : person[1],
                "gender" : person[2],
                "location" : person[3],
                "education" : person[4],
                "profession" : person[5]
                }

        return new_people

    def needs(self, ids:list):
        
        query = f'''
        SELECT person_id,
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
            WHERE person_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE person_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_people = {}
        for person in data:
            
            id = person[0]

            new_people[id] = {
                'health_insurance_need' : person[1], 
                'home_insurance_need' : person[2], 
                'longterm_care_insurance_need' : person[3], 
                'payment_financing_need' : person[4], 
                'loan_financing_need' : person[5], 
                'mortgage_financing_need' : person[6], 
                'capital_accumulation_investment_need' : person[7], 
                'capital_protection_investment_need' : person[8],
                'retirement_investment_need' : person[9], 
                'income_investment_need' : person[10], 
                'heritage_investment_need' : person[11], 
                'liquidity_investment_need' : person[12]
            }
            
        return new_people

    def status(self, ids:list):
        
        query = f'''
        SELECT person_id, 
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
            WHERE person_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE person_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_people = {}
        for person in data:
            
            id = person[0]

            new_people[id] = {
                "real_assets_index" : person[1], 
                "financial_assets_index" : person[2],
                "net_liabilities_index" : person[3], 
                "net_wealth_index" : person[4],
                "net_income_index" : person[5], 
                "net_savings_index" : person[6],
                "net_expences_index" : person[7]
                }
                
            
        return new_people

    def attitudes(self, ids:list):
        
        query = f'''
        SELECT person_id,
        bank_activity_index, digital_activity_index,
        cultural_activity_index, charity_activity_index

        FROM {self.schema_name}.cust_attitudes
        '''

        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE person_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE person_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_people = {}
        for person in data:
            
            id = person[0]
                
            new_people[id] = {
                "bank_activity_index" : person[1], 
                "digital_activity_index" : person[2],
                "cultural_activity_index" : person[3], 
                "charity_activity_index" : person[4]
                }
            
        return new_people
   
    def cultures(self, ids:list):
        
        query = f'''
        SELECT person_id,
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
            WHERE person_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE person_id in {tuple(ids)}
            '''
        data = self.engine.connect().execute(statement=query)

        new_people = {}
        for person in data:
            
            id = person[0]

            new_people[id] = {
                "financial_horizon_index" : person[1], 
                "financial_litteracy_index" : person[2],
                "financial_experience_index" : person[3], 
                "objective_risk_propensity_index" : person[4],
                "subjective_risk_propensity_index" : person[5], 
                "esg_propensity_index" : person[6],
                "life_quality_index" : person[7],
                "sophisticated_instrument" : person[8], 
                "marginality_index" : person[9]
                }
            
        return new_people

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
            people_sociodemo = self.socio_demographics(ids=ids)
            final_keys = people_sociodemo.keys()

            flags["cultures"] = True
            people_cultures = self.cultures(ids=ids)

            flags["status"] = True
            people_status = self.status(ids=ids)

            flags["needs"] = True
            people_needs = self.needs(ids=ids)

            flags["attitudes"] = True
            people_attitudes = self.attitudes(ids=ids)

        if "sociodemographics" in categories:
            flags["sociodemographics"] = True
            people_sociodemo = self.socio_demographics(ids=ids)
            final_keys = people_sociodemo.keys()
            
        if "cultures" in categories:
            flags["cultures"] = True
            people_cultures = self.cultures(ids=ids)
            final_keys = people_cultures.keys()
            
        if "status" in categories:
            flags["status"] = True
            people_status = self.status(ids=ids)
            final_keys = people_status.keys()
        
        if "needs" in categories:
            flags["needs"] = True
            people_needs = self.needs(ids=ids)
            final_keys = people_needs.keys()

        if "attitudes" in categories:
            flags["attitudes"] = True
            people_attitudes = self.attitudes(ids=ids)
            final_keys = people_attitudes.keys()

        people = []

        for id in final_keys:
            
            person = {
                "id" : id
            } 

            if flags["sociodemographics"]: person["sociodemographics"] = people_sociodemo[id]
            if flags["cultures"]: person["cultures"] = people_cultures[id]
            if flags["status"]: person["status"] = people_status[id]
            if flags["needs"]: person["needs"] = people_needs[id]
            if flags["attitudes"]: person["attitudes"] = people_attitudes[id]
            
            people.append(person)

        return people