from sqlalchemy import create_engine

class Insert_controller:

    def __init__(self) -> None:

        # object to control the sample
        # before adding to enrichment db

        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        
        # customer id

        query = f'''
        SELECT customer_id
        FROM {self.schema_name}.hub_customer
        '''
    
        response = self.engine.connect().execute(query)
        customer_ids = response.fetchall()

        self.customer_ids = []
        if customer_ids == None: self.customer_ids = []
        else:
            for item in customer_ids:
                self.customer_ids.append(item[0])

    
    def first_necessary_keys_controller(self, customer:dict):

        # flag & errors
        flag = True
        errors = ""

        # controll "id"

        if not "id" in customer.keys(): 
            errors += "try sending an id for each record. " 
            flag = False
        
        elif customer["id"] in self.customer_ids:
            flag = False
            errors += f"customer_id '{customer['id']}' exists in db, use update instead. " 

        return flag, errors

    def first_optional_keys_controller(self, customer:dict):

        flags = {
            "sociodemographics" : False,
            "status" : False,
            "cultures" : False,
            "attitudes" : False,
            "needs" : False
            } 

        if "sociodemographics" in customer.keys(): flags["sociodemographics"] = True
        if "cultures" in customer.keys(): flags["cultures"] = True
        if "status" in customer.keys(): flags["status"] = True
        if "attitudes" in customer.keys(): flags["attitudes"] = True
        if "needs" in customer.keys(): flags["needs"] = True

        return flags
        
    def sociodemographics_keys_controller(self, customer:dict):
        
        # mandatory variables
        optional_keys = [
            "age", "gender", "location", "profession", "education"
        ]

        # flag & errors
        flag = True
        errors = ""

        # flag True means to have necessary input data
        flag = True

        # check if necessary keys exist
        for key in customer["sociodemographics"].keys() :

            if not key in optional_keys:
                flag = False
                errors += f"try sending only '{optional_keys}' as cultures dictionary keys. "

        return flag, errors

    def sociodemographics_values_controller(self, customer:dict):
        
        # functional limits to each variable
        age_limits = [0, 120]

        gender_limits = ["m", "f", "o"]

        location_limits = [
            'piemonte', "valle daosta", 'lombardia', 'trentino alto adige', 'veneto', 'friuli venezia giulia',
            'liguria', 'emilia romagna', 'toscana', 'umbria', 'marche', 'lazio', 'abruzzo', 'molise', 'campania',
            'puglia', 'basilicata', 'calabria', 'sicilia', 'sardegna' 
        ]

        profession_limits = [
            "lavoratore dipendente", "lavoratore indipendente", "pensionato",
            "non occupato"
        ]

        education_limits = [
            "scuola primaria", "scuola secondaria di I grado", "scuola secondaria di II grado",
            "istruzione superiore università", "master di II livello e PHD"
        ]

        # flag & errors
        flag = True
        errors = ""

        # check if necessary variables exist

        if "age" in customer["sociodemographics"].keys():
            if not type(customer["sociodemographics"]["age"]) in [int, float]:
                flag = False
                errors += f"try sending sociodemographics 'age' variable in this limits: '{age_limits}'. "
        
            elif (customer["sociodemographics"]["age"] > 120) | (customer["sociodemographics"]["age"] < 0): 
                flag = False
                errors += f"try sending sociodemographics 'age' variable in this limits: '{age_limits}'. "
        
        if "gender" in customer["sociodemographics"].keys():
            if not customer["sociodemographics"]["gender"] in gender_limits: 
                flag = False
                errors += f"try sending sociodemographics 'gender' variable in this limits: '{gender_limits}'. "

        if "location" in customer["sociodemographics"].keys():
            if not customer["sociodemographics"]["location"] in location_limits: 
                flag = False
                errors += f"try sending sociodemographics 'location' variable in this limits: '{location_limits}'. "

        if "profession" in customer["sociodemographics"].keys():
            if not customer["sociodemographics"]["profession"] in profession_limits: 
                flag = False
                errors += f"try sending sociodemographics 'profession' variable in this limits: '{profession_limits}'. "

        if "education" in customer["sociodemographics"].keys():
            if not customer["sociodemographics"]["education"] in education_limits: 
                flag = False
                errors += f"try sending sociodemographics 'education' variable in this limits: '{education_limits}'. "

        return flag, errors

    def cultures_controller(self, customer:dict):
        
        # optional variables
        optional_keys = [
            "financial_horizon_index", "financial_litteracy_index", 
            "financial_experience_index", "objective_risk_propensity_index", 
            "subjective_risk_propensity_index", "esg_propensity_index",
            "life_quality_index", "sophisticated_instrument", "marginality_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        if customer["cultures"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as cultures dictionary keys. "

        for key in customer["cultures"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as cultures dictionary keys. "

            elif (customer["cultures"][key] < 0) | (customer["cultures"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as cultures dictionary values. "

        return flag, errors

    def status_controller(self, customer:dict):
        
        # optional variables
        optional_keys = [
            "net_income_index", "net_expences_index", "net_savings_index",
            "real_assets_index", "financial_assets_index", "net_liabilities_index",
            "net_wealth_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        if customer["status"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as status dictionary keys. "

        for key in customer["status"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as status dictionary keys. "

            elif (customer["status"][key] < 0) | (customer["status"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as status dictionary values. "

        return flag, errors
            
    def attitudes_controller(self, customer:dict):
        
        # optional variables
        optional_keys = [
            "bank_activity_index", "digital_activity_index", 
            "cultural_activity_index", "charity_activity_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        if customer["attitudes"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as attitudes dictionary keys. "

        for key in customer["attitudes"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as attitudes dictionary keys. "

            elif (customer["attitudes"][key] < 0) | (customer["attitudes"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as attitudes dictionary values. "

        return flag, errors

    def needs_controller(self, customer:dict):
        
        # optional variables
        optional_keys = [
            "capital_accumulation_investment_need", "capital_protection_investment_need", 
            "liquidity_investment_need", "income_investment_need",
            "retirement_investment_need", "heritage_investment_need",
            "health_incurance_need", "home_insurance_need",
            "longterm_care_insurance_need", "payment_financing_need",
            "loan_financing_need", "mortgage_financing_need"
        ]

        # flag & errors
        flag = True
        errors = ""

        if customer["needs"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as needs dictionary keys. "

        for key in customer["needs"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as needs dictionary keys. "

            elif (customer["needs"][key] < 0) | (customer["needs"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as needs dictionary values. "

        return flag, errors

    def run(self, customers:list):

        # flag & errors
        flag = True
        errors = ""

        if type(customers) != list:
            flag = False
            errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
            return flag, errors
        
        for customer in customers:
            
            if type(customer) != dict:
                flag = False
                errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
                return flag, errors
            
            all_keys = ["id", "sociodemographics", "attitudes", "cultures", "status", "needs"]
            for key in customer.keys():
                if not key in all_keys:
                    flag = False
                    errors += f"try sending only '{all_keys}' as record dictionary keys. "
                    return flag, errors
                
            # necessary keys
            flag, errs = self.first_necessary_keys_controller(customer=customer)
            if not flag: 
                errors += errs
                return flag, errors
            else:
                customer_id = customer["id"]

            # optional keys
            flags = self.first_optional_keys_controller(customer=customer)
            
            # control sociodemographics keys and values
            if flags["sociodemographics"]:
                flag, errors = self.sociodemographics_keys_controller(customer=customer)
                if not flag: 
                    errors += errs 
                    errors +=f"error seen at id = '{customer_id}'. "
                    return flag, errors

                flag, errors = self.sociodemographics_values_controller(customer=customer)
                if not flag: 
                    errors += errs
                    errors += f"error seen at id = '{customer_id}'. "
                    return flag, errors

            # control cultures if exists
            if flags["cultures"]:
                flag, errors = self.cultures_controller(customer=customer)
                if not flag: 
                    errors += errs
                    errors += f"error seen at id = '{customer_id}'. "
                    return flag, errors

            # control status if exists
            if flags["status"]:
                flag, errors = self.status_controller(customer=customer)
                if not flag: 
                    errors += errs
                    errors += f"error seen at id = '{customer_id}'. "
                    return flag, errors
            
            # control attitudes if exists
            if flags["attitudes"]:
                flag, errors = self.attitudes_controller(customer=customer)
                if not flag: 
                    errors += errs
                    errors += f"error seen at id = '{customer_id}'. "
                    return flag, errors

            # control needs if exists
            if flags["needs"]:
                flag, errors = self.needs_controller(customer=customer)
                if not flag: 
                    errors += errs
                    errors += f"error seen at id = '{customer_id}'. "
                    return flag, errors

        return flag, errors