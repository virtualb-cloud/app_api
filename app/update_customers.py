from sqlalchemy import create_engine

class Update:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def update_customer_sociodemographics(self, customer:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.hub_customer
        SET 
        '''
        set_query = ""

        record = customer["sociodemographics"]

        # control keys
        keys_list = [
            "age", "gender", "location", "education", "profession"
            ]

        for key in keys_list:

            if key in record.keys(): 
                if key == "age":
                    set_query += f'''{key}_ = {record[key]},'''
                else: 
                    set_query += f'''{key}_ = '{record[key]}','''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE customer_id = '{record['customer_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def update_customer_cultures(self, customer:dict):

        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.cust_cultures
        SET 
        '''
        set_query = ""

        record = customer["cultures"]

        # control keys
        keys_list = [
            "financial_horizon_index", "financial_litteracy_index",
            "financial_experience_index", "objective_risk_propensity_index",
            "subjective_risk_propensity_index", "esg_propensity_index",
            "life_quality_index", "sophisticated_instrument", "marginality_index"
            ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''{key} = {record[key]},'''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE customer_id = '{record['customer_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def update_customer_status(self, customer:dict):

        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.cust_status
        SET 
        '''
        set_query = ""

        record = customer["status"]

        keys_list = [
            "real_assets_index", "financial_assets_index",
            "net_liabilities_index", "net_wealth_index",
            "net_income_index", "net_savings_index",
            "net_expences_index"
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f''' {key} = {record[key]},'''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE customer_id = '{record['customer_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def update_customer_attitudes(self, customer:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.cust_attitudes
        SET 
        '''
        set_query = ""

        record = customer["attitudes"]

        keys_list = [
            "bank_activity_index", "digital_activity_index",
            "cultural_activity_index", "charity_activity_index"
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''{key} = {record[key]},'''


        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE customer_id = '{record['customer_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def update_customer_needs(self, customer:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.cust_needs
        SET 
        '''
        set_query = ""

        record = customer["needs"]

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
        query = fixed_query + set_query + f" WHERE customer_id = '{record['customer_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def run(self, customers:list):

        for customer in customers:
            
            customer_id = customer["id"]

            if "sociodemographics" in customer.keys(): 
                customer["sociodemographics"]["customer_id"] = customer_id
                self.update_customer_sociodemographics(customer=customer)
                print("sociodemographics pushed")

            if "cultures" in customer.keys(): 
                customer["cultures"]["customer_id"] = customer_id
                self.update_customer_cultures(customer=customer)
                print("cultures pushed")
                
            if "status" in customer.keys(): 
                customer["status"]["customer_id"] = customer_id
                self.update_customer_status(customer=customer)
                print("status pushed")

            if "attitudes" in customer.keys(): 
                customer["attitudes"]["customer_id"] = customer_id
                self.update_customer_attitudes(customer=customer)
                print("attitudes pushed")

            if "needs" in customer.keys(): 
                customer["needs"]["customer_id"] = customer_id
                self.update_customer_needs(customer=customer)
                print("needs pushed")
                
        return True
