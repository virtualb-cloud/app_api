from sqlalchemy import create_engine

class Update:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def update_position_description(self, position:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.link_position
        SET 
        '''
        set_query = ""

        record = position["description"]

        # control keys
        keys_list = [
            "portfolio_id", "product_id"
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''{key} = '{record[key]}','''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE position_id = '{record['position_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def run(self, positions:list):

        for position in positions:
            
            position_id = position["id"]

            if "description" in position.keys(): 
                position["description"]["position_id"] = position_id
                self.update_position_description(position=position)
                print("description pushed")
                
        return True
