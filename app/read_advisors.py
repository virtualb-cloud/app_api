from sqlalchemy import create_engine

class Read:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
    
    def description(self, ids:list):

        query = f'''
        SELECT advisor_id, classification_index, qualification_index, diversification_index

        FROM {self.schema_name}.hub_advisor
        '''
        if ids == []:
            query = query 

        elif len(ids) == 1:
            query = query + f'''
            WHERE advisor_id = '{ids[0]}'
            '''

        elif len(ids) >= 1:
            query = query + f'''
            WHERE advisor_id in {tuple(ids)}
            '''

        data = self.engine.connect().execute(statement=query)

        new_advisors = {}
        for advisor in data:

            id = advisor[0]

            new_advisors[id] = {
                "classification_index" : advisor[1],
                "qualification_index" : advisor[2],
                "diversification_index" : advisor[3]
                }

        return new_advisors

    def run(self, body:dict):

        ids = body["ids"]

        categories = body["categories"]

        flags = {
            "description" : False
            }

        if categories == []:
            
            flags["description"] = True
            advisors_desc = self.description(ids=ids)
            final_keys = advisors_desc.keys()

        if "description" in categories:
            flags["description"] = True
            advisors_desc = self.description(ids=ids)
            final_keys = advisors_desc.keys()
        
        advisors = []

        for id in final_keys:
            
            advisor = {
                "id" : id
            } 

            if flags["description"]: advisor["description"] = advisors_desc[id]

            advisors.append(advisor)

        return advisors