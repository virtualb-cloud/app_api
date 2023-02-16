from sqlalchemy import create_engine

class Read_controller:

    def __init__(self) -> None:

        # object to control the sample
        # before adding to enrichment db

        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        
        # product id

        query = f'''
        SELECT product_id
        FROM {self.schema_name}.hub_product
        '''
    
        response = self.engine.connect().execute(statement=query)
        product_ids = response.fetchall()

        self.product_ids = []
        if product_ids == None: self.product_ids = []
        else:
            for item in product_ids:
                self.product_ids.append(item[0])

    
    def first_keys_controller(self, body:dict):
        
        # flag & errors
        flag = True
        errors = ""

        first_keys = ["ids", "categories"]
        categories = ["description", "needs", "assets", "cultures"]

        for key in first_keys:
            
            if not key in body.keys(): 
                flag = False
                errors += f"please consider sending '{first_keys}' as body dictionary keys. "
        
            if type(body[key]) != list:
                flag = False 
                errors += f"please consider sending a list for {key}."
            
            if key == "id":
                for id in body[key]:
                    if not id in self.product_ids:
                        flag = False
                        errors += f"product_id '{id}' does not exist in db. " 
            
            if key == "categories":
                for category in body[key]:
                    if not category in categories:
                        flag = False
                        errors += f"category '{category}' does not exist in db. " 

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