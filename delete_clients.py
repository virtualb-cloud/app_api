from sqlalchemy import create_engine, text

class Delete:

    def __init__(self) -> None:
        
        # db connection
        self.schema_name = "data_enrichment_v3"
        self.engine = create_engine("postgresql://postgres:!vbPostgres@virtualb-rds-data-enrichment.clg6weaheijj.eu-south-1.rds.amazonaws.com:5432/postgres")
  
    def run(self, body:dict):

        ids = body["ids"]

        if len(ids) == 1:

            query = f'''
            DELETE FROM {self.schema_name}.sociodemographics as sd
            WHERE sd.person_id = {ids[0]}
            '''

        elif len(ids) >= 1:

            query = f'''
            DELETE FROM {self.schema_name}.sociodemographics as sd
            WHERE sd.person_id in {tuple(ids)}
            '''

        self.engine.connect().execute(statement=text(query))
  
        return True
