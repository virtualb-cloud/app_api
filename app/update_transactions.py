from sqlalchemy import create_engine

class Update:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def update_transaction_description(self, transaction:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.sat_transaction
        SET 
        '''
        set_query = ""

        record = transaction["description"]

        # control keys
        keys_list = [
            "position_id", "type", "amount"
        ]

        for key in keys_list:

            if key in record.keys(): 

                if key != "type":
                    set_query += f'''{key} = '{record[key]}','''
                else:
                    set_query += f'''{key}_ = '{record[key]}','''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE transaction_id = '{record['transaction_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def run(self, transactions:list):

        for transaction in transactions:
            
            transaction_id = transaction["id"]

            if "description" in transaction.keys(): 
                transaction["description"]["transaction_id"] = transaction_id
                self.update_transaction_description(transaction=transaction)
                print("description pushed")
                
        return True
