from sqlalchemy import create_engine

class Read:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
    
    def description(self, ids:list):

        query = f'''
        SELECT position_id, portfolio_id, product_id

        FROM {self.schema_name}.link_position
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE position_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE position_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_positions = {}
        for position in data:

            id = position[0]

            new_positions[id] = {
                "portfolio_id" : position[1],
                "product_id" : position[2]
                }

        return new_positions

    def run(self, body:dict):

        ids = body["ids"]

        categories = body["categories"]

        flags = {
            "description" : False
            }

        if categories == []:
            
            flags["description"] = True
            positions_desc = self.description(ids=ids)
            final_keys = positions_desc.keys()

        if "description" in categories:
            flags["description"] = True
            positions_desc = self.description(ids=ids)
            final_keys = positions_desc.keys()
        
        positions = []

        for id in final_keys:
            
            position = {
                "id" : id
            } 

            if flags["description"]: position["description"] = positions_desc[id]

            positions.append(position)

        return positions