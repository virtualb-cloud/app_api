from sqlalchemy import create_engine

class Insert:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def insert_transactions(self, transactions:list):
        
        # prepare fixed query
        query = f'''
            INSERT INTO {self.schema_name}.sat_transaction(
                transaction_id, position_id, type_, amount
            )
            VALUES '''
        
        keys_list = [
            "position_id", "type", "amount"
        ]
        # add the data to query
        for transaction in transactions:
            
            transaction_id = transaction["id"]

            # check
            if not "description" in transaction.keys(): transaction["description"] = {}
            
            record = transaction["description"]

            add_statement = f'''('{transaction_id}','''
            
            # control keys
            for key in keys_list:
                if not key in record.keys(): 
                    record[key] = "NULL"
                    add_statement += f''' {record[key]},'''
                else:
                    add_statement += f''' '{record[key]}','''

            # to exclude the last ","
            query = query + add_statement[:-1] + "),"

        query = query[:-1] + ";"

        # execute the query
        with self.engine.connect() as conn:
            conn.execute(statement=query)

        return True

    def run(self, transactions:list):

        
        self.insert_transactions(transactions=transactions)
        print("description pushed")

        return True
