from fastapi import HTTPException

from App.utils.utils import * 
from App.dependencias.database import ConexaoDB


class AprovedorRepository:
    def __init__(self, db_connection: ConexaoDB):
        self.base = db_connection

    def list_provedor(self, user: dict) -> list:
        query = """select * from gia_provedor WHERE 1 = 1"""
        
        params = {} 

        if 'nome_provedor' in user and user['nome_provedor']:
            query += " AND nome_provedor = :nome_provedor"
            params['nome_provedor'] = user['nome_provedor']
        
        query += " ORDER BY nome_provedor ASC"
        
        return self.base.select(query, params)
