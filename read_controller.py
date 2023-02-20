from sqlalchemy import create_engine

class Read_controller:

    def __init__(self) -> None:

        # object to control the sample
        # before adding to enrichment db

        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        
        # transaction id

        query = f'''
        SELECT transaction_id
        FROM {self.schema_name}.sat_transaction
        '''
    
        response = self.engine.connect().execute(statement=query)
        transaction_ids = response.fetchall()

        self.transaction_ids = []
        if transaction_ids == None: self.transaction_ids = []
        else:
            for item in transaction_ids:
                self.transaction_ids.append(item[0])

        print(self.transaction_ids)

    
    def first_keys_controller(self, body:dict):
        
        # flag & errors
        flag = True
        errors = ""

        first_keys = ["ids"]
        categories = ["description"]

        for key in first_keys:
            
            if not key in body.keys(): 
                flag = False
                errors += f"please consider sending '{first_keys}' as body dictionary keys. "
        
            elif type(body[key]) != list:
                flag = False 
                errors += f"please consider sending a list for {key}."
            
            if key == "ids":
                for id in body[key]:
                    if not id in self.transaction_ids:
                        flag = False
                        errors += f"transaction_id '{id}' does not exist in db. " 
            
            elif key == "categories":
                for category in body[key]:
                    if not category in categories:
                        flag = False
                        errors += f"category '{category}' does not exist, please send {categories}. " 

        return flag, errors
    
    def run(self, body:dict):

        # flag & errors
        flag = True
        errors = ""

        if type(body) != dict:
            flag = False 
            errors += "please consider sending a body like: {'ids' : [], 'categories' : []}. "
            return flag, errors

        flag, errs = self.first_keys_controller(body)
        if not flag:
            errors += errs
            return flag, errors

        return flag, errors