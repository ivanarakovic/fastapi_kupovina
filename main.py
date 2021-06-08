from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# kreiramo instancu klase FastAPI
app = FastAPI()


class Kupovina(BaseModel):
    id: int
    kupac: str
    grad: str
    datum_vrijeme: datetime
    proizvod: str
    cijena: float


# kreiranje novih podataka
@app.post('/kupovina')
def create(kupovina: Kupovina):
    data = pd.read_csv('kupovina.csv')
    if kupovina.id in data.to_dict()['id'].values():
        return {'id':'already exists'}
    new_data = pd.DataFrame({
        'id': [kupovina.id],
        'kupac': [kupovina.kupac],
        'grad': [kupovina.grad],
        'datum_vrijeme': [kupovina.datum_vrijeme],
        'proizvod': [kupovina.proizvod],
        'cijena': [kupovina.cijena]
    })
    data = data.append(new_data)
    data.to_csv('kupovina.csv', index = False)
    return kupovina


# citanje svih podataka
@app.get('/kupovina')
def get_all():
    data = pd.read_csv('kupovina.csv')
    all_data = data.transpose().to_dict()
    return all_data


# citanje odredjenog podatka
@app.get('/kupovina/{id}')
def get_one(id: int):
    data = pd.read_csv('kupovina.csv')
    all_data = data.transpose().to_dict()
    for data in all_data:
        if(all_data[data]['id'] == id):
            one_data = all_data[data]
            return one_data
    return {'id':'doesn\'t exist'}


# azuriranje odredjenog podatka
@app.put('/kupovina/{id}')
def update(id: int, kupovina: Kupovina):
    data = pd.read_csv('kupovina.csv')
    if id not in data.to_dict()['id'].values():
        return {'id': 'doesn\'t exist'}
    data = data.transpose().to_dict()
    returnvalue=''
    for index in data:
        if data[index]['id'] == id:
            data[index] = {
                'id': id,
                'kupac': kupovina.kupac,
                'grad': kupovina.grad,
                'datum_vrijeme': kupovina.datum_vrijeme,
                'proizvod': kupovina.proizvod,
                'cijena': kupovina.cijena
            }
            returnvalue = data[index]
    data = pd.DataFrame(data)
    data.transpose().to_csv('kupovina.csv', index=False)
    return returnvalue


# brisanje odredjenog podatka
@app.delete('/kupovina/{id}')
def delete(id: int):
    data = pd.read_csv('kupovina.csv')
    if id not in data.to_dict()['id'].values():
        return {'id': 'doesn\'t exist'}
    data = data.transpose().to_dict()
    temp=''
    for index in data:
        print(index)
        if data[index]['id'] == id:
            temp = index
            break
    del data[temp]
    if (data):
        data = pd.DataFrame(data)
        data.transpose().to_csv('kupovina.csv', index=False)
    else:
        data = pd.DataFrame({'id': [],'kupac': [], 'grad': [],'datum_vrijeme': [],'proizvod': [],'cijena': []})
        data.to_csv('kupovina.csv', index = False)
    return {'data': 'deleted successfully'}