from sqlalchemy import create_engine

class Insert:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def insert_people_sociodemographics(self, people:list):
        
        # prepare fixed query
        query = f'''
            INSERT INTO {self.schema_name}.hub_customer(
                person_id, age_, gender_, location_, education_, profession_
            )
            VALUES '''
        
        # add the data to query
        for person in people:

            person_id = person["id"]
            
            record = person["sociodemographics"]

            add_statement = f'''('{person_id}', {record["age"]}, '{record["gender"]}',
            '{record["location"]}', '{record["education"]}', '{record["profession"]}'),'''
            query = query + add_statement

        # to exclude the last ","
        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            result = conn.execute(statement=query)

        return True

    def insert_people_cultures(self, people:list):

        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.cust_cultures(
            person_id, financial_horizon_index, financial_litteracy_index,
            financial_experience_index, objective_risk_propensity_index,
            subjective_risk_propensity_index, esg_propensity_index,
            life_quality_index, sophisticated_instrument, marginality_index
        )
        VALUES '''
        
        keys_list = [
            "financial_horizon_index", "financial_litteracy_index",
            "financial_experience_index", "objective_risk_propensity_index",
            "subjective_risk_propensity_index", "esg_propensity_index",
            "life_quality_index", "sophisticated_instrument", "marginality_index"]

        for person in people:

            person_id = person["id"]

            # check
            if not "cultures" in person.keys(): person["cultures"] = {}

            record = person["cultures"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query   
            add_statement = f'''('{person_id}', {record["financial_horizon_index"]},
                {record["financial_litteracy_index"]}, {record["financial_experience_index"]},
                {record["objective_risk_propensity_index"]}, {record["subjective_risk_propensity_index"]}, 
                {record["esg_propensity_index"]}, {record["life_quality_index"]},
                {record["sophisticated_instrument"]}, {record["marginality_index"]}
            ),'''

            query = query + add_statement
        
        # to exclude the last ","
        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            result = conn.execute(statement=query)

        return True

    def insert_people_status(self, people:list):

        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.cust_status(
            person_id, real_assets_index, financial_assets_index,
            net_liabilities_index, net_wealth_index,
            net_income_index, net_savings_index,
            net_expences_index
        )
        VALUES '''

        keys_list = [
            "real_assets_index", "financial_assets_index",
            "net_liabilities_index", "net_wealth_index",
            "net_income_index", "net_savings_index",
            "net_expences_index"
        ]

        for person in people:

            person_id = person["id"]

            # check
            if not "status" in person.keys(): person["status"] = {}

            record = person["status"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query  
            add_statement = f'''('{person_id}', {record["real_assets_index"]},
                {record["financial_assets_index"]}, {record["net_liabilities_index"]},
                {record["net_wealth_index"]}, {record["net_income_index"]}, 
                {record["net_savings_index"]}, {record["net_expences_index"]}
            ),'''

            query = query + add_statement
        
        # to exclude the last ","
        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            result = conn.execute(statement=query)

        return True

    def insert_people_attitudes(self, people:list):
        
        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.cust_attitudes(
            person_id, bank_activity_index, digital_activity_index,
            cultural_activity_index, charity_activity_index
        )
        VALUES '''

        keys_list = [
            "bank_activity_index", "digital_activity_index",
            "cultural_activity_index", "charity_activity_index"
        ]

        for person in people:

            person_id = person["id"]

            # check
            if not "attitudes" in person.keys(): person["attitudes"] = {}

            record = person["attitudes"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query  
            add_statement = f'''('{person_id}',
                {record["bank_activity_index"]}, {record["digital_activity_index"]},
                {record["cultural_activity_index"]}, {record["charity_activity_index"]}
            ),'''

            query = query + add_statement

        # to exclude the last ","
        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            conn.execute(statement=query)

        return True

    def insert_people_needs(self, people:list):
        
        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.cust_needs(
            person_id, health_insurance_need, home_insurance_need, longterm_care_insurance_need, 
            payment_financing_need, loan_financing_need, mortgage_financing_need, 
            capital_accumulation_investment_need, capital_protection_investment_need,
            retirement_investment_need, income_investment_need, 
            heritage_investment_need, liquidity_investment_need
        )
        VALUES '''

        keys_list = [
            'health_insurance_need', 'home_insurance_need', 'longterm_care_insurance_need', 
            'payment_financing_need', 'loan_financing_need', 'mortgage_financing_need', 
            'capital_accumulation_investment_need', 'capital_protection_investment_need',
            'retirement_investment_need', 'income_investment_need', 
            'heritage_investment_need', 'liquidity_investment_need'
        ]

        for person in people:

            person_id = person["id"]

            # check
            if not "needs" in person.keys(): person["needs"] = {}

            record = person["needs"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query 
            add_statement = f'''('{person_id}', {record["health_insurance_need"]},
                {record["home_insurance_need"]}, {record["longterm_care_insurance_need"]},
                {record["payment_financing_need"]}, {record["loan_financing_need"]}, 
                {record["mortgage_financing_need"]}, {record["capital_accumulation_investment_need"]},
                {record["capital_protection_investment_need"]},
                {record["retirement_investment_need"]}, {record["income_investment_need"]}, 
                {record["heritage_investment_need"]}, {record["liquidity_investment_need"]}
            ),'''
            query = query + add_statement

        # to exclude the last ","
        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            result = conn.execute(statement=query)
        
        return True

    def run(self, people:list):

        self.insert_people_sociodemographics(people=people)
        print("sociodemographics pushed")

        self.insert_people_cultures(people=people)
        print("cultures pushed")

        self.insert_people_status(people=people)
        print("status pushed")

        self.insert_people_attitudes(people=people)
        print("attitudes pushed")

        self.insert_people_needs(people=people)
        print("needs pushed")

        return True
