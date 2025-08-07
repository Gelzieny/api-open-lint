from fastapi import HTTPException

from App.utils.utils import * 
from App.dependencias.database import ConexaoPostgres


class ModeloRepository:
    def __init__(self, db_connection: ConexaoPostgres):
        self.base = db_connection

    def list_modelo(self, user: dict) -> list:
        query = """
            SELECT 
                m.id_modelo, 
                m.nome_modelo, 
                m.stat_modelo, 
                p.id_provedor,
                p.nome_provedor,
                CASE m.stat_modelo
                    WHEN 'A' THEN 'Ativo'
                    ELSE 'Inativo'
                END AS status_modelos
            FROM gia_modelo m
                INNER JOIN gia_provedor p
                    ON p.id_provedor = m.id_provedor
            WHERE 1 = 1
        """
        
        params = {} 

        if 'stat_modelo' in user and user['stat_modelo']:
            query += " AND m.stat_modelo = :stat_modelo"
            params['stat_modelo'] = user['stat_modelo']
        
        if 'nome_modelo' in user and user['nome_modelo']:
            query += " AND m.nome_modelo = :nome_modelo"
            params['nome_modelo'] = user['nome_modelo']
        

        return self.base.select(query, params)
    
    
    def create_modelo(self, info: dict) -> dict:
        # Busca modelos existentes com o mesmo nome
        modelos = self.list_modelo(info)

        if info['nome_modelo'] in modelos[0]:
            modelo_existente = modelos[0]
            
            # Se o modelo existente já tem os mesmos dados, não faz nada
            mesmo_nome = modelo_existente['nome_modelo'] == info['nome_modelo']
            mesmo_status = modelo_existente['stat_modelo'] == info['stat_modelo']
            mesmo_provedor = modelo_existente['id_provedor'] == info['id_provedor']
            id_modelo = modelo_existente['id_modelo'] == info['id_modelo']

            self.update_modelo(modelo_existente)
            
        info['stat_modelo'] = 'A'
        
        # Se não encontrou nenhum modelo, realiza o INSERT
        query = """
            INSERT INTO gia_modelo (
                nome_modelo,
                stat_modelo,
                id_provedor
            ) VALUES (
                :nome_modelo,
                :stat_modelo,
                :codigo_provedor
            )
        """
        
        ret = self.base.insert(query, info)

        sucesso = ret.get('success') and ret.get('rows_affected') == 1

        return {
            'codigo': 1 if sucesso else 99,
            'message': (
                f"Modelo '{info['nome_modelo']}' cadastrado com sucesso."
                if sucesso else ret.get('error', f"Erro ao cadastrar modelo: '{info['nome_modelo']}'.")
            )
        }

                    
    def update_modelo(self, info):
        param = {}     # Busca modelos existentes com o mesmo nome
        modelos = self.list_modelo(info)

        if info['nome_modelo'] in modelos[0]['nome_modelo']:
            modelo_existente = modelos[0]
            
            param = {
                'id_modelo': modelo_existente['id_modelo'],
                'nome_modelo': modelo_existente['nome_modelo'],
                'codigo_provedor': info['codigo_provedor'],
                'stat_modelo': 'I' if info.get('stat_modelo') == 'A' else 'A'
            }

            ret = self.base.update("""
                UPDATE gia_modelo 
                SET stat_modelo = :stat_modelo 
                WHERE id_modelo = :id_modelo
                RETURNING stat_modelo
            """, param)

            sucesso = ret.get('success') and ret.get('rows_affected') == 1

            return {
                'codigo': 1 if sucesso else 99,
                'message': (
                    f"Modelo '{info['nome_modelo']}' {'excluído' if info['stat_modelo'] == 'A' else 'ativado'} com sucesso."
                    if sucesso else ret.get('error', f"Erro ao atualizar modelo: '{info['nome_modelo']}'.")
                )
            }



            
                

