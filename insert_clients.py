from sqlalchemy import create_engine

class Insert:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def insert_customers_sociodemographics(self, customers:list):
        
        # prepare fixed query
        query = f'''
            INSERT INTO {self.schema_name}.hub_customer(
                customer_id, age_, gender_, location_, education_, profession_
            )
            VALUES '''
        
        keys_list = [
            "age", "gender", "location", "profession", "education"
        ]
        # add the data to query
        for customer in customers:

            customer_id = customer["id"]

            # check
            if not "sociodemographics" in customer.keys(): customer["sociodemographics"] = {}
            
            record = customer["sociodemographics"]

            # control keys
            add_statement = f'''('{customer_id}','''
            for key in keys_list:
                
                if not key in record.keys(): 
                    record[key] = "NULL"
                    add_statement += f''' {record[key]},'''
                
                else:
                    if key == "age":
                        add_statement += f''' {record[key]},'''
                    else:
                        add_statement += f''' '{record[key]}','''
                    
            # to exclude the last ","
            query = query + add_statement[:-1] + "),"

        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            result = conn.execute(statement=query)

        return True

    def insert_customers_cultures(self, customers:list):

        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.cust_cultures(
            customer_id, financial_horizon_index, financial_litteracy_index,
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

        for customer in customers:

            customer_id = customer["id"]

            # check
            if not "cultures" in customer.keys(): customer["cultures"] = {}

            record = customer["cultures"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query   
            add_statement = f'''('{customer_id}', {record["financial_horizon_index"]},
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

    def insert_customers_status(self, customers:list):

        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.cust_status(
            customer_id, real_assets_index, financial_assets_index,
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

        for customer in customers:

            customer_id = customer["id"]

            # check
            if not "status" in customer.keys(): customer["status"] = {}

            record = customer["status"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query  
            add_statement = f'''('{customer_id}', {record["real_assets_index"]},
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

    def insert_customers_attitudes(self, customers:list):
        
        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.cust_attitudes(
            customer_id, bank_activity_index, digital_activity_index,
            cultural_activity_index, charity_activity_index
        )
        VALUES '''

        keys_list = [
            "bank_activity_index", "digital_activity_index",
            "cultural_activity_index", "charity_activity_index"
        ]

        for customer in customers:

            customer_id = customer["id"]

            # check
            if not "attitudes" in customer.keys(): customer["attitudes"] = {}

            record = customer["attitudes"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query  
            add_statement = f'''('{customer_id}',
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

    def insert_customers_needs(self, customers:list):
        
        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.cust_needs(
            customer_id, health_insurance_need, home_insurance_need, longterm_care_insurance_need, 
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

        for customer in customers:

            customer_id = customer["id"]

            # check
            if not "needs" in customer.keys(): customer["needs"] = {}

            record = customer["needs"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query 
            add_statement = f'''('{customer_id}', {record["health_insurance_need"]},
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

    def run(self, customers:list):

        self.insert_customers_sociodemographics(customers=customers)
        print("sociodemographics pushed")

        self.insert_customers_cultures(customers=customers)
        print("cultures pushed")

        self.insert_customers_status(customers=customers)
        print("status pushed")

        self.insert_customers_attitudes(customers=customers)
        print("attitudes pushed")

        self.insert_customers_needs(customers=customers)
        print("needs pushed")

        return True
