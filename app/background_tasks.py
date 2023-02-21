from app.update_products import Update
from app.insert_products import Insert
from app.delete_products import Delete

def deleter(body:list):

    deleter = Delete()
    response = deleter.run(body=body)
    if response: return True
    else: return False

def updater(body:list):
    
    updater = Update()
    response = updater.run(products=body)
    if response: return True
    else: return False

def inserter(body:list):
    
    inserter = Insert()
    response = inserter.run(products=body)
    if response: return True
    else: return False