from app.update_customers import Update
from app.insert_customers import Insert
from app.delete_customers import Delete

def deleter(body:list):

    deleter = Delete()
    response = deleter.run(body=body)
    if response: return True
    else: return False

def updater(body:dict):
    
    updater = Update()
    response = updater.run(body=body)
    if response: return True
    else: return False

def inserter(samples:list):
    
    inserter = Insert()
    response = inserter.run(body=samples)
    if response: return True
    else: return False