from sqlalchemy import create_engine

class Read:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
    
    def description(self, ids:list):

        query = f'''
        SELECT transaction_id, position_id, type_, amount

        FROM {self.schema_name}.sat_transaction
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE transaction_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE transaction_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_transactions = {}
        for transaction in data:

            id = transaction[0]

            new_transactions[id] = {
                "position_id" : transaction[1],
                "type" : transaction[2],
                "amount" : transaction[3]
                }

        return new_transactions

    def run(self, body:dict):

        ids = body["ids"]

        categories = body["categories"]

        flags = {
            "description" : False
            }

        if categories == []:
            
            flags["description"] = True
            transactions_desc = self.description(ids=ids)
            final_keys = transactions_desc.keys()

        if "description" in categories:
            flags["description"] = True
            transactions_desc = self.description(ids=ids)
            final_keys = transactions_desc.keys()
        
        transactions = []

        for id in final_keys:
            
            transaction = {
                "id" : id
            } 

            if flags["description"]: transaction["description"] = transactions_desc[id]

            transactions.append(transaction)

        return transactions