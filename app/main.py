from fastapi import FastAPI, status, HTTPException
from .schemas import Kupovina
import pandas as pd

# kreiramo instancu klase FastAPI
app = FastAPI()

filepath = './app/kupovina.csv'


# kreiranje novih podataka
@app.post('/kupovina', status_code=status.HTTP_201_CREATED)
def create(kupovina: Kupovina):
    data = pd.read_csv(filepath)
    if kupovina.id in data.to_dict()['id'].values():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'id {kupovina.id} already exists')
    new_data = pd.DataFrame({
        'id': [kupovina.id],
        'kupac': [kupovina.kupac],
        'grad': [kupovina.grad],
        'datum_vrijeme': [kupovina.datum_vrijeme],
        'proizvod': [kupovina.proizvod],
        'cijena': [kupovina.cijena]
    })
    data = data.append(new_data)
    data.to_csv(filepath, index=False)
    return kupovina


# citanje svih podataka
@app.get('/kupovina')
def get_all():
    data = pd.read_csv(filepath)
    all_data = data.transpose().to_dict()
    return all_data


# citanje odredjenog podatka
@app.get('/kupovina/{id}')
def get_one(id: int):
    data = pd.read_csv(filepath)
    all_data = data.transpose().to_dict()
    for data in all_data:
        if(all_data[data]['id'] == id):
            one_data = all_data[data]
            return one_data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not available')


# azuriranje odredjenog podatka
@app.put('/kupovina/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, kupovina: Kupovina):
    data = pd.read_csv(filepath)
    if id not in data.to_dict()['id'].values():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not available')
    data = data.transpose().to_dict()
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
    data = pd.DataFrame(data)
    data.transpose().to_csv(filepath, index=False)
    return {'detail': 'updated successfully'}


# brisanje odredjenog podatka
@app.delete('/kupovina/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    data = pd.read_csv(filepath)
    if id not in data.to_dict()['id'].values():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not available')
    data = data.transpose().to_dict()
    temp=''
    for index in data:
        print(index)
        if data[index]['id'] == id:
            temp = index
            break
    del data[temp]
    if data:
        data = pd.DataFrame(data)
        data.transpose().to_csv(filepath, index=False)
    else:
        data = pd.DataFrame({'id': [], 'kupac': [], 'grad': [], 'datum_vrijeme': [], 'proizvod': [], 'cijena': []})
        data.to_csv('kupovina.csv', index=False)
    return {'detail': 'deleted successfully'}