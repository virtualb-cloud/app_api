from sqlalchemy import create_engine

class Update:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def update_advisor_description(self, advisor:dict):
        
        # fixed query
        fixed_query = f'''
        UPDATE {self.schema_name}.hub_advisor
        SET 
        '''
        set_query = ""

        record = advisor["description"]

        # control keys
        keys_list = [
            "classification_index", "qualification_index", "diversification_index"
        ]

        for key in keys_list:

            if key in record.keys(): 
                set_query += f'''{key} = '{record[key]}','''

        # to exclude the last ","
        set_query = set_query[:-1]
        query = fixed_query + set_query + f" WHERE advisor_id = '{record['advisor_id']}'" 

        # execute the query
        self.engine.connect().execute(statement=query)

        return True

    def run(self, advisors:list):

        for advisor in advisors:
            
            advisor_id = advisor["id"]

            if "description" in advisor.keys(): 
                advisor["description"]["advisor_id"] = advisor_id
                self.update_advisor_description(advisor=advisor)
                print("description pushed")
                
        return True
