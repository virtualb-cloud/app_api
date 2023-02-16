# Allianz v2.0

import numpy as np
import pandas as pd
import json
from pipelines_ingestion.ingestion_utils import Type_Null_controller


class Products:

    def __init__(self, external_df:pd.DataFrame) -> None:

        # copy
        self.external_df = external_df

        # columns
        self.columns_expected_type = {
            "FAMIGLIA" : "string",
            "MACRO_PRODOTTO" : "string",
            "" : "string",
            "SOTTO_PRODOTTO" : "string",
            "COD_SOTTOPROD" : "string",
            "COD_ISIN" : "string",
            "ESPERIENZA_T" : "string",
            "CONOSCENZA_MIFID" : "string",
            "Sottotipologia" : "string",
            "Bisogno" : "string",
            "CODICE_AA" : "string",
            "ISR_PRODOTTO" : "float",
            "PESO" : "float",
            "data_riferimento" : "string",
            #"ART 6-8-9" : ""
            }

        # initialization
        initializer = Type_Null_controller(self.columns_expected_type)
        response = initializer.run(self.external_df)
        if response[0] == False: print(response)
        else: self.initialized_df = response[1]

        # renaming
        final_naming = {
            'FAMIGLIA' : "product_family", 
            'MACRO_PRODOTTO' : 'product_macro',
            'GRUPPO_PRODOTTO' : "product_group", 
            'PRODOTTO' : 'product_name',
            'COD_PROD' : "product_code", 
            'SOTTO_PRODOTTO' : 'subproduct_name',
            'COD_SOTTOPROD' : "subproduct_code", 
            'Tipologia' : "type", 
            'Sottotipologia' : 'sub_type',
            'COD_ISIN' : "isin_code", 
            'ESPERIENZA_T' : 'requested_financial_experience',
            'CONOSCENZA_MIFID' : "requested_financial_knowledge", 
            'ISR_PRODOTTO' : 'requested_risk_tolerance',
            'CODICE_AA' : "asset_code", 
            'PESO' : 'weight',
            'Bisogno' : 'need'
        }
        self.ready_df = self.initialized_df.rename(columns=final_naming)

# maps

    def read_map_need(self) -> dict:
        
        self.our_needs = [
            "capital_accumulation_investment_need",
            "capital_protection_investment_need",
            "liquidity_investment_need",
            "income_investment_need",
            "retirement_investment_need",
            "heritage_investment_need",
            "home_insurance_need",
            "health_insurance_need",
            "longterm_care_insurance_need",
            "payment_financing_need",
            "loan_financing_need",
            "mortgage_financing_need"
        ]

        self.their_needs = [
            "Liquidità",
            "Multiramo (no PRV)",
            "Accumulo",
            "Income",
            "Protezione capitale",
            "Previdenza",
            "Protezione persona",
            "LTC"
        ]
        mappa = {
            "Liquidità" : ["liquidity_investment_need"], 
            "Multiramo (no PRV)" : [ ], 
            "Accumulo" : [ "capital_accumulation_investment_need" ],
            "Income" : [ "income_investment_need" ], 
            "Protezione capitale" : [ "capital_protection_investment_need" ],
            "Previdenza" : [ "retirement_investment_need" ],
            "Protezione persona" : [ "health_insurance_need", "home_insurance_need" ], 
            "LTC" : [ "longterm_care_insurance_need" ],
            'Income - Liquidità' : [ "income_investment_need", "liquidity_investment_need" ],
            '0' : [ ]
            }

        return mappa

    def read_map_product(self) -> dict:
        
        # read the map
        with open('pipelines_ingestion/maps/map_product.json') as json_file:
            mappa = json.load(json_file)

        return mappa
    
# final tables

    def hub_product(self, last_primary_key:int) -> pd.DataFrame:

        # copy
        temp_df = self.ready_df

        # drop duplicates on identity
        products_identity = [
            'product_family', 'product_macro', 'product_group',
            'product_name', 'product_code', 'subproduct_name', 'subproduct_code'
        ]
        temp_df = temp_df.drop_duplicates(subset=products_identity)
        
        # create primary key
        temp_df = temp_df.reset_index()
        temp_df["product_id"] = temp_df.index + last_primary_key + 1

        # select columns
        temp_df = temp_df[["product_id"] + products_identity]
        
        ##### write the map
        products_list = temp_df.to_dict(orient="records")

        mappa = dict()

        # build
        for product in products_list:
            
            key = tuple()

            for identity in product.keys():
                if identity in products_identity:
                    key = (*key, product[identity])

            mappa[str(key)] = product["product_id"]
        
        # save
        with open("pipelines_ingestion/maps/map_product.json", "w") as write_file:
            json.dump(mappa, write_file, indent=4)

        # set
        temp_df.set_index("product_id", inplace=True)

        return temp_df

    def sat_product_properties(self) -> pd.DataFrame:
        
        # copy
        temp_df = self.ready_df

        # drop duplicates on identity
        products_identity = [
            'product_family', 'product_macro', 'product_group',
            'product_name', 'product_code', 'subproduct_name', 'subproduct_code'
        ]
        products_properties = [
            "type", "sub_type", "isin_code",
            "requested_financial_experience", "requested_financial_knowledge",
            "requested_risk_tolerance"
        ]
        temp_df = temp_df.drop_duplicates(subset=products_identity + products_properties)
        
        # select the desired columns
        temp_df = temp_df[products_identity + products_properties]
        
        # create foreign key
        mappa = self.read_map_product()

        for idx, row in temp_df.iterrows():
            
            # make the key
            key = tuple(row[products_identity])

            # ask the id
            temp_df.loc[idx, "product_id"] = mappa[str(key)] if str(key) in mappa.keys() else np.nan

        # select
        temp_df = temp_df[["product_id"] + products_properties]

        # set
        temp_df.set_index("product_id", inplace=True)

        return temp_df

    def sat_product_asset_allocation(self) -> pd.DataFrame:

        # copy
        temp_df = self.ready_df

        # drop duplicates on identity
        products_identity = [
            'product_family', 'product_macro', 'product_group',
            'product_name', 'product_code', 'subproduct_name', 'subproduct_code'
        ]
        products_asset_allocation = [
            'asset_code', 'weight'
        ]
        # drop duplicates on identity
        temp_df = temp_df.drop_duplicates(subset=products_identity + products_asset_allocation)
        
        # select the desired columns
        temp_df = temp_df[products_identity + products_asset_allocation]

        #### create product_id column
        
        # read map
        mappa = self.read_map_product()

        for idx, row in temp_df.iterrows():
            
            # make the key
            key = tuple(row[products_identity])

            # ask the id
            temp_df.loc[idx, "product_id"] = mappa[str(key)] if str(key) in mappa.keys() else np.nan
        
        # select
        temp_df = temp_df[["product_id"] + products_asset_allocation]

        # set
        temp_df.set_index("product_id", inplace=True)

        return temp_df
        
    def sat_product_needs(self) -> pd.DataFrame:

        # copy
        temp_df = self.ready_df

        # drop duplicates on identity
        products_identity = [
            'product_family', 'product_macro', 'product_group',
            'product_name', 'product_code', 'subproduct_name', 'subproduct_code'
        ]
        products_need = [
            'need'
        ]
        temp_df = temp_df.drop_duplicates(subset=products_identity + products_need)

        # select the desired columns
        temp_df = temp_df[products_identity + products_need]

        #### create product_id column
        
        # read map
        mappa = self.read_map_product()

        for idx, row in temp_df.iterrows():
            
            # make the key
            key = tuple(row[products_identity])

            # ask the id
            temp_df.loc[idx, "product_id"] = mappa[str(key)] if str(key) in mappa.keys() else np.nan

        #### create need columns
        
        # read map
        mappa = self.read_map_need()
        
        # create
        for need in self.our_needs:
            temp_df[need] = 0.0

        # build
        for idx, row in temp_df.iterrows():
            
            their_element = temp_df.loc[idx, products_need[0]]

            if their_element in mappa.keys():
                    
                for our_element in mappa[their_element]:

                    temp_df.loc[idx, our_element] = 1

        # select the desired columns
        temp_df = temp_df[["product_id"] + self.our_needs]

        # set
        temp_df.set_index("product_id", inplace=True)

        return temp_df

        
