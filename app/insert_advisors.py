from sqlalchemy import create_engine

class Insert:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "mainapp"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-mainapp.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
        

    def insert_advisors_description(self, advisors:list):
        
        # prepare fixed query
        query = f'''
            INSERT INTO {self.schema_name}.hub_advisor(
                advisor_id, classification_index, qualification_index, 
                diversification_index
            )
            VALUES '''
        
        keys_list = [
            "classification_index", "qualification_index", "diversification_index"
        ]
        # add the data to query
        for advisor in advisors:
            
            advisor_id = advisor["id"]

            # check
            if not "description" in advisor.keys(): advisor["description"] = {}
            
            record = advisor["description"]

            add_statement = f'''('{advisor_id}','''
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

    def run(self, advisors:list):

        self.insert_advisors_description(advisors=advisors)
        print("description pushed")

        return True
