from sqlalchemy import create_engine

class Insert_controller:

    def __init__(self) -> None:

        # object to control the sample
        # before adding to enrichment db

        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        
        # advisor id

        query = f'''
        SELECT advisor_id
        FROM {self.schema_name}.hub_advisor
        '''
    
        response = self.engine.connect().execute(query)
        advisor_ids = response.fetchall()

        self.advisor_ids = []
        if advisor_ids == None: self.advisor_ids = []
        else:
            for item in advisor_ids:
                self.advisor_ids.append(item[0])

    
    def first_necessary_keys_controller(self, advisor:dict):

        # flag & errors
        flag = True
        errors = ""

        # controll "id"

        if not "id" in advisor.keys(): 
            errors += "try sending an id for each record. " 
            flag = False
        
        elif advisor["id"] in self.advisor_ids:
            flag = False
            errors += f"advisor_id '{advisor['id']}' exists in db, use update instead. " 

        return flag, errors
    
    def first_optional_keys_controller(self, advisor:dict):

        flags = {
            "description" : False
            } 

        if "description" in advisor.keys(): flags["description"] = True

        return flags
        
    def description_keys_controller(self, advisor:dict):
        
        # mandatory variables
        optional_keys = [
            "classification_index", "qualification_index", "diversification_index"
        ]

        # flag & errors
        flag = True
        errors = ""

        for key in advisor["description"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending '{optional_keys}' as description dictionary keys. "

            elif not type(advisor["description"][key]) in [int, float]:
                flag = False
                errors += "try sending a value in [0, 1] range as description dictionary values. "

            elif (advisor["description"][key] < 0) | (advisor["description"][key] > 1): 
                flag = False
                errors += f"try sending a value in [0, 1] range as description dictionary values. "

        return flag, errors

    def run(self, advisors:list):

        # flag & errors
        flag = True
        errors = ""

        if type(advisors) != list:
            flag = False
            errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
            return flag, errors
        
        for advisor in advisors:
            
            if type(advisor) != dict:
                flag = False
                errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
                return flag, errors
            
            all_keys = ["id", "description"]
            for key in advisor.keys():
                if not key in all_keys:
                    flag = False
                    errors += f"try sending only '{all_keys}' as record dictionary keys. "
                    return flag, errors
                
            # necessary keys
            flag, errs = self.first_necessary_keys_controller(advisor=advisor)
            if not flag: 
                errors += errs
                return flag, errors
            else:
                advisor_id = advisor["id"]

            # optional keys
            flags = self.first_optional_keys_controller(advisor=advisor)
            
            if flags["description"]:
                flag, errors = self.description_keys_controller(advisor=advisor)
                if not flag: 
                    errors += errs 
                    errors +=f"error seen at id = '{advisor_id}'. "
                    return flag, errors


        return flag, errors