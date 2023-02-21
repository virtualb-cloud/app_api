from app.update_advisors import Update
from app.insert_advisors import Insert
from app.delete_advisors import Delete

def deleter(body:list):

    deleter = Delete()
    response = deleter.run(body=body)
    if response: return True
    else: return False

def updater(body:list):
    
    updater = Update()
    response = updater.run(advisors=body)
    if response: return True
    else: return False

def inserter(body:list):
    
    inserter = Insert()
    response = inserter.run(advisors=body)
    if response: return True
    else: return False