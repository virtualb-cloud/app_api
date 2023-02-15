from sqlalchemy import create_engine, text

class Insert_controller:

    def __init__(self) -> None:

        # object to control the sample
        # before adding to enrichment db

        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-maipapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        
        # person id

        query = f'''
        SELECT person_id
        FROM {self.schema_name}.sociodemographics
        '''
    
        response = self.engine.connect().execute(statement=text(query))
        self.person_ids = response.fetchall()

        if self.person_id == None: self.person_ids = []
        pass
    
    def first_necessary_keys_controller(self, person:dict):

        # flag & errors
        flag = True
        errors = ""

        # controll "id"

        if not "id" in person.keys(): 
            errors += "try sending an id for each record" 
            flag = False
        
        elif person["id"] in self.person_ids:
            flag = False
            errors += f"person_id {person['id']} exists in db, use update instead." 

        # controll "sociodemographics"
        elif not "sociodemographics" in person.keys(): 
            flag = False
            errors += "try sending sociodemographics dictionary for each record" 

        return flag, errors

    def first_optional_keys_controller(self, person:dict):

        flags = {
            "status" : False,
            "cultures" : False,
            "attitudes" : False,
            "needs" : False
            } 

        if "cultures" in person.keys(): flags["cultures"] = True
        if "status" in person.keys(): flags["status"] = True
        if "attitudes" in person.keys(): flags["attitudes"] = True
        if "needs" in person.keys(): flags["needs"] = True

        return flags
        
    def sociodemographics_keys_controller(self, person:dict):
        
        # mandatory variables
        mandatory_keys = [
            "age", "gender", "location", "profession", "education"
        ]

        # flag & errors
        flag = True
        errors = ""

        # flag True means to have necessary input data
        flag = True

        # check if necessary keys exist
        for key in mandatory_keys :
            if not key in person["sociodemographics"].keys(): 
                flag = False
                errors += f"try sending {key} as a sociodemographics dictionary key"

        return flag, errors

    def sociodemographics_values_controller(self, person:dict):
        
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
        if (person["sociodemographics"]["age"] > 120) | (person["sociodemographics"]["age"] < 0): 
            flag = False
            errors += f"try sending sociodemographics age variable in this limits: {age_limits}"
        
        elif not person["sociodemographics"]["gender"] in gender_limits: 
            flag = False
            errors += f"try sending sociodemographics gender variable in this limits: {gender_limits}"

        elif not person["sociodemographics"]["location"] in location_limits: 
            flag = False
            errors += f"try sending sociodemographics location variable in this limits: {location_limits}"

        elif not person["sociodemographics"]["profession"] in profession_limits: 
            flag = False
            errors += f"try sending sociodemographics profession variable in this limits: {profession_limits}"

        elif not person["sociodemographics"]["education"] in education_limits: 
            flag = False
            errors += f"try sending sociodemographics education variable in this limits: {education_limits}"

        return flag, errors

    def cultures_controller(self, person:dict):
        
        # optional variables
        optional_keys = [
            "financial_horizon_index", "finacial_littercay_index", 
            "financial_experience_index", "objective_risk_propensity_index", 
            "subjective_risk_propensity_index", "esg_propensity_index",
            "life_quality_index", "sophisticated_instrument", "marginality_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        if person["cultures"] == {}:
            flag = False
            errors += f"try sending at least one of {optional_keys} as cultures dictionary keys"

        for key in person["cultures"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending {optional_keys} as cultures dictionary keys"

            elif (person["cultures"][key] < 0) | (person["cultures"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as cultures dictionary values"

        return flag, errors

    def status_controller(self, person:dict):
        
        # optional variables
        optional_keys = [
            "net_income_index", "net_expences_index", "net_savings_index",
            "real_assets_index", "financial_assets_index", "net_liabilities_index",
            "net_wealth_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        if person["status"] == {}:
            flag = False
            errors += f"try sending at least one of {optional_keys} as status dictionary keys"

        for key in person["status"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending {optional_keys} as status dictionary keys"

            elif (person["status"][key] < 0) | (person["status"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as status dictionary values"

        return flag, errors
            
    def attitudes_controller(self, person:dict):
        
        # optional variables
        optional_keys = [
            "bank_activity_index", "digital_activity_index", 
            "cultural_activity_index", "charity_activity_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        if person["attitudes"] == {}:
            flag = False
            errors += f"try sending at least one of {optional_keys} as attitudes dictionary keys"

        for key in person["attitudes"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending {optional_keys} as attitudes dictionary keys"

            elif (person["attitudes"][key] < 0) | (person["attitudes"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as attitudes dictionary values"

        return flag, errors

    def needs_controller(self, person:dict):
        
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

        if person["needs"] == {}:
            flag = False
            errors += f"try sending at least one of {optional_keys} as needs dictionary keys"

        for key in person["needs"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending {optional_keys} as needs dictionary keys"

            elif (person["needs"][key] < 0) | (person["needs"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as needs dictionary values"

        return flag, errors

    def run(self, people:list):

        # flag & errors
        flag = True
        errors = ""

        if type(people) != list:
            flag = False
            errors += "try sending a body [{rescord1}, ..., {rescordn}]"
            return flag, errors
        
        for person in people:
            
            if type(person) != dict:
                flag = False
                errors += "try sending a body [{rescord1}, ..., {rescordn}]"
                return flag, errors
            
            all_keys = ["id", "sociodemographics", "attitudes", "cultures", "status"]
            for key in person.keys():
                if not key in all_keys:
                    flag = False
                    errors += f"try sending only {all_keys} as record dictionary keys"
                    return flag, errors
                
            # necessary keys
            flag, errs = self.first_necessary_keys_controller(person=person)
            if not flag: 
                errors += errs
                return flag, errors
            else:
                person_id = person["id"]

            # control sociodemographics keys and values
            flag, errors = self.sociodemographics_keys_controller(person=person)
            if not flag: 
                errors += errs 
                errors += + f"error seen at id = {person_id}"
                return flag, errors

            flag, errors = self.sociodemographics_values_controller(person=person)
            if not flag: 
                errors += errs
                errors += + f"error seen at id = {person_id}"
                return flag, errors
            
            # optional keys
            flags = self.first_optional_keys_controller(person=person)
            
            # control cultures if exists
            if flags["cultures"]:
                flag, errors = self.cultures_controller(person=person)
                if not flag: 
                    errors += errs
                    errors += + f"error seen at id = {person_id}"
                    return flag, errors

            # control status if exists
            if flags["status"]:
                flag, errors = self.status_controller(person=person)
                if not flag: 
                    errors += errs
                    errors += + f"error seen at id = {person_id}"
                    return flag, errors
            
            # control attitudes if exists
            if flags["attitudes"]:
                flag, errors = self.attitudes_controller(person=person)
                if not flag: 
                    errors += errs
                    errors += + f"error seen at id = {person_id}"
                    return flag, errors

            # control needs if exists
            if flags["needs"]:
                flag, errors = self.needs_controller(person=person)
                if not flag: 
                    errors += errs
                    errors += + f"error seen at id = {person_id}"
                    return flag, errors

        return flag, errors