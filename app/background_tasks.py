from app.update_customers import Update
from app.insert_customers import Insert
from app.delete_customers import Delete

def deleter(body:list):

    deleter = Delete()
    response = deleter.run(body=body)
    if response: return True
    else: return False

def updater(body:list):
    
    updater = Update()
    response = updater.run(customers=body)
    if response: return True
    else: return False

def inserter(body:list):
    
    inserter = Insert()
    response = inserter.run(customers=body)
    if response: return True
    else: return False