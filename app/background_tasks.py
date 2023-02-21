from app.update_positions import Update
from app.insert_positions import Insert
from app.delete_positions import Delete

def deleter(body:list):

    deleter = Delete()
    response = deleter.run(body=body)
    if response: return True
    else: return False

def updater(body:list):
    
    updater = Update()
    response = updater.run(positions=body)
    if response: return True
    else: return False

def inserter(body:list):
    
    inserter = Insert()
    response = inserter.run(positions=body)
    if response: return True
    else: return False