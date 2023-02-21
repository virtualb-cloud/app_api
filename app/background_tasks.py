from app.update_transactions import Update
from app.insert_transactions import Insert
from app.delete_transactions import Delete

def deleter(body:list):

    deleter = Delete()
    response = deleter.run(body=body)
    if response: return True
    else: return False

def updater(body:list):
    
    updater = Update()
    response = updater.run(transactions=body)
    if response: return True
    else: return False

def inserter(body:list):
    
    inserter = Insert()
    response = inserter.run(transactions=body)
    if response: return True
    else: return False