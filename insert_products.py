from sqlalchemy import create_engine

class Insert:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def insert_products_description(self, products:list):
        
        # prepare fixed query
        query = f'''
            INSERT INTO {self.schema_name}.hub_product(
                product_id, name_, isin_code, bloomberg_id, currency
            )
            VALUES '''
            
        keys_list = [
            "name", "isin_code", "bloomberg_id", "currency"
            ]
        # add the data to query
        for product in products:

            product_id = product["id"]
            
            record = product["description"]

            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            add_statement = f'''('{product_id}', '{record["name"]}', '{record["isin_code"]}',
            '{record["bloomberg_id"]}', '{record["currency"]}'),'''
            query = query + add_statement

        # to exclude the last ","
        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            conn.execute(statement=query)

        return True

    def insert_products_cultures(self, products:list):

        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.prod_cultures(
            product_id, financial_horizon_index, financial_litteracy_index,
            financial_experience_index, risk_propensity_index,
            esg_propensity_index, sophisticated_instrument, 
            marginality_index
        )
        VALUES '''
        
        keys_list = [
            "financial_horizon_index", "financial_litteracy_index",
            "financial_experience_index", "risk_propensity_index",
            "esg_propensity_index", "sophisticated_instrument", "marginality_index"]

        for product in products:

            product_id = product["id"]

            # check
            if not "cultures" in product.keys(): product["cultures"] = {}

            record = product["cultures"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query   
            add_statement = f'''('{product_id}', {record["financial_horizon_index"]},
                {record["financial_litteracy_index"]}, {record["financial_experience_index"]},
                {record["risk_propensity_index"]}, 
                {record["esg_propensity_index"]}, 
                {record["sophisticated_instrument"]}, {record["marginality_index"]}
            ),'''

            query = query + add_statement
        
        # to exclude the last ","
        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            result = conn.execute(statement=query)

        return True

    def insert_products_assets(self, products:list):

        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.prod_assets(
            product_id, equity_index, balanced_index,
            bond_index, real_estate_index,
            commodity_index, money_market_index,
            liquidity_index
        )
        VALUES '''

        keys_list = [
            "equity_index", "balanced_index",
            "bond_index", "real_estate_index",
            "commodity_index", "money_market_index",
            "liquidity_index"
        ]

        for product in products:

            product_id = product["id"]

            # check
            if not "assets" in product.keys(): product["assets"] = {}

            record = product["assets"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query  
            add_statement = f'''('{product_id}', {record["equity_index"]},
                {record["balanced_index"]}, {record["bond_index"]},
                {record["real_estate_index"]}, {record["commodity_index"]}, 
                {record["money_market_index"]}, {record["liquidity_index"]}
            ),'''

            query = query + add_statement
        
        # to exclude the last ","
        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            result = conn.execute(statement=query)

        return True

    def insert_products_needs(self, products:list):
        
        # fixed query
        query = f'''
        INSERT INTO {self.schema_name}.prod_needs(
            product_id, health_insurance_need, home_insurance_need, longterm_care_insurance_need, 
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

        for product in products:

            product_id = product["id"]

            # check
            if not "needs" in product.keys(): product["needs"] = {}

            record = product["needs"]
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): record[key] = "NULL"

            # add the data to query 
            add_statement = f'''('{product_id}', {record["health_insurance_need"]},
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
            conn.execute(statement=query)
        
        return True

    def run(self, products:list):

        self.insert_products_description(products=products)
        print("description pushed")

        self.insert_products_cultures(products=products)
        print("cultures pushed")

        self.insert_products_assets(products=products)
        print("assets pushed")

        self.insert_products_needs(products=products)
        print("needs pushed")

        return True
