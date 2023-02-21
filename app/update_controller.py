from sqlalchemy import create_engine

class Update_controller:

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
        
        # position id
        query = f'''
        SELECT position_id
        FROM {self.schema_name}.link_position
        '''
    
        response = self.engine.connect().execute(statement=query)
        position_ids = response.fetchall()

        self.position_ids = []
        if position_ids == None: self.position_ids = []
        else:
            for item in position_ids:
                self.position_ids.append(item[0])
    
    def first_necessary_keys_controller(self, transaction:dict):

        # flag & errors
        flag = True
        errors = ""

        # controll "id"

        if not "id" in transaction.keys(): 
            errors += "try sending an id for each record. " 
            flag = False
        
        elif not transaction["id"] in self.transaction_ids:
            flag = False
            errors += f"transaction_id '{transaction['id']}' does not exist in db. " 

        return flag, errors

    def first_optional_keys_controller(self, transaction:dict):

        flags = {
            "description" : False
            } 

        if "description" in transaction.keys(): flags["description"] = True

        return flags
        
    def description_keys_controller(self, transaction:dict):
        
        # mandatory variables
        optional_keys = [
            "position_id", "type", "amount"
        ]

        # flag & errors
        flag = True
        errors = ""

        if transaction["description"] == {}:
            flag = False
            errors += f"try sending at least one of '{optional_keys}' as description dictionary keys. "

        for key in transaction["description"].keys():

            if not key in optional_keys:
                flag = False
                errors += f"try sending only '{optional_keys}' as description dictionary keys. "

            if key != "amount":
                if not type(transaction["description"][key]) in [str]:
                    flag = False
                    errors += f"try sending a string as description dictionary '{key}' values. "
            else:
                if not type(transaction["description"][key]) in [float, int]:
                    flag = False
                    errors += f"try sending a float value as description dictionary '{key}' values. "

            if key == "position_id" :
                if not transaction["description"][key] in self.position_ids:
                    flag = False
                    errors += f"position_id '{transaction['description'][key]}' does not exist in db. "

        return flag, errors

    def run(self, transactions:list):

        # flag & errors
        flag = True
        errors = ""

        if type(transactions) != list:
            flag = False
            errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
            return flag, errors
        
        for transaction in transactions:
            
            if type(transaction) != dict:
                flag = False
                errors += "try sending a body [{rescord1}, ..., {rescordn}]. "
                return flag, errors
            
            all_keys = ["id", "description"]
            for key in transaction.keys():
                if not key in all_keys:
                    flag = False
                    errors += f"try sending only '{all_keys}' as record dictionary keys. "
                    return flag, errors
                
            # necessary keys
            flag, errs = self.first_necessary_keys_controller(transaction=transaction)
            if not flag: 
                errors += errs
                return flag, errors
            else:
                transaction_id = transaction["id"]

            # optional keys
            flags = self.first_optional_keys_controller(transaction=transaction)
            
            sign = 0
            for k, v in flags.items():
                if v == True: sign = 1
            
            if sign == 0:
                flag = False
                errors = f"try sending at least one of '{all_keys[1:]}'. "
                errors +=  f"error seen at id = '{transaction_id}'. "
                return flag, errors

            # control description if exists
            if flags["description"]:

                # control description keys
                flag, errors = self.description_keys_controller(transaction=transaction)
                if not flag: 
                    errors += errs 
                    errors +=  f"error seen at id = '{transaction_id}'. "
                    return flag, errors

        return flag, errors