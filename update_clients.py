from sqlalchemy import create_engine, text

class Insert:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-maipapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def update_person_sociodemographics(self, person:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.sociodemographics
        SET 
        '''
        set_query = ""

        record = person["sociodemographics"]

        # control keys
        keys_list = [
            "age", "gender", "location", "education", "profession"
            ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''({key}_ = {record[key]}),'''

        # to exclude the last ","
        query = query[:-1]
        query = fixed_query + set_query + f" WHERE person_id = {record['person_id']}" 

        # execute the query
        self.engine.connect().execute(statement=text(query))

        return True

    def update_person_cultures(self, person:dict):

        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.cultures
        SET 
        '''
        set_query = ""

        record = person["cultures"]

        # control keys
        keys_list = [
            "financial_horizon_index", "financial_litteracy_index",
            "financial_experience_index", "objective_risk_propensity_index",
            "subjective_risk_propensity_index", "esg_propensity_index",
            "life_quality_index", "sophisticated_instrument", "marginality_index"
            ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''({key} = {record[key]}),'''

        # to exclude the last ","
        query = query[:-1]
        query = fixed_query + set_query + f" WHERE person_id = {record['person_id']}" 

        # execute the query
        self.engine.connect().execute(statement=text(query))

        return True

    def update_person_status(self, person:dict):

        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.status
        SET 
        '''
        set_query = ""

        record = person["status"]

        keys_list = [
            "real_assets_index", "financial_assets_index",
            "net_liabilities_index", "net_wealth_index",
            "net_income_index", "net_savings_index",
            "net_expences_index"
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''({key} = {record[key]}),'''

        # to exclude the last ","
        query = query[:-1]
        query = fixed_query + set_query + f" WHERE person_id = {record['person_id']}" 

        # execute the query
        self.engine.connect().execute(statement=text(query))

        return True

    def update_person_attitudes(self, person:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.attitudes
        SET 
        '''
        set_query = ""

        record = person["attitudes"]

        keys_list = [
            "bank_activity_index", "digital_activity_index",
            "cultural_activity_index", "charity_activity_index"
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''({key} = {record[key]}),'''


        # to exclude the last ","
        query = query[:-1]
        query = fixed_query + set_query + f" WHERE person_id = {record['person_id']}" 

        # execute the query
        self.engine.connect().execute(statement=text(query))

        return True

    def update_person_needs(self, person:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.needs
        SET 
        '''
        set_query = ""

        record = person["needs"]

        keys_list = [
            'health_insurance_need', 'home_insurance_need', 'longterm_care_insurance_need', 
            'payment_financing_need', 'loan_financing_need', 'mortgage_financing_need', 
            'capital_accumulation_investment_need', 'capital_protection_investment_need',
            'retirement_investment_need', 'income_investment_need', 
            'heritage_investment_need', 'liquidity_investment_need'
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''({key} = {record[key]}),'''

        # to exclude the last ","
        query = query[:-1]
        query = fixed_query + set_query + f" WHERE person_id = {record['person_id']}" 

        # execute the query
        self.engine.connect().execute(statement=text(query))

        return True

    def run(self, people:list):

        for person in people:
            
            person_id = person["id"]

            if "sociodemographics" in person.keys(): 
                person["sociodemographics"]["person_id"] = person_id
                self.update_person_sociodemographics(person=person)
                print("sociodemographics pushed")

            if "cultures" in person.keys(): 
                person["cultures"]["person_id"] = person_id
                self.update_person_cultures(person=person)
                print("cultures pushed")
                
            if "status" in person.keys(): 
                person["status"]["person_id"] = person_id
                self.update_person_status(person=person)
                print("status pushed")

            if "attitudes" in person.keys(): 
                person["attitudes"]["person_id"] = person_id
                self.update_person_attitudes(person=person)
                print("attitudes pushed")

            if "needs" in person.keys(): 
                person["needs"]["person_id"] = person_id
                self.update_person_needs(person=person)
                print("needs pushed")
                
        return True
