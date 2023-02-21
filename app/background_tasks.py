from app.update_portfolios import Update
from app.insert_portfolios import Insert
from app.delete_portfolios import Delete

def deleter(body:list):

    deleter = Delete()
    response = deleter.run(body=body)
    if response: return True
    else: return False

def updater(body:list):
    
    updater = Update()
    response = updater.run(portfolios=body)
    if response: return True
    else: return False

def inserter(body:list):
    
    inserter = Insert()
    response = inserter.run(portfolios=body)
    if response: return True
    else: return False