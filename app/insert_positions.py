from sqlalchemy import create_engine

class Insert:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def insert_positions(self, positions:list):
        
        # prepare fixed query
        query = f'''
            INSERT INTO {self.schema_name}.link_position(
                position_id, portfolio_id, product_id
            )
            VALUES '''
        
        keys_list = [
            "portfolio_id", "product_id"
        ]
        # add the data to query
        for position in positions:
            
            position_id = position["id"]

            # check
            if not "description" in position.keys(): position["description"] = {}
            
            record = position["description"]

            add_statement = f'''('{position_id}','''
            
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

    def run(self, positions:list):

        
        self.insert_positions(positions=positions)
        print("description pushed")

        return True
