import re
import unicodedata
from App.models.perms_model import *

just_numbers = lambda a: ''.join(re.findall("\d+", a))

def mensagem_retorno(self, mensagem, cod_retorno):
    response = PermsResponse(
        mensagem=mensagem, 
        cod_retorno=cod_retorno,
        tipo_retorno='success' if cod_retorno == 0 else 'error',
    )
    return response

def retira_vazios(param):
    ret = {}
    for i in param:
        if not (len(str(param[i])) == 0  or param[i] is None):
            ret.update({i: param[i]})

    return ret

import unicodedata

def fun_remove_acentos(texto: str) -> str:
    """
    Remove acentos de uma string e retorna apenas os caracteres ASCII.
    
    Exemplo:
    >>> FUN_REMOVE_ACENTOS("ação")
    'acao'
    """
    
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_sem_acentos = ''.join([c for c in texto_normalizado if not unicodedata.combining(c)])
    return texto_sem_acentos

def processar_parametros(user: dict) -> dict:
    for chave, valor in user.items():
        if isinstance(valor, str):
            user[chave] = fun_remove_acentos(valor)
    return user

def trata_retorno_oracle(self, value, msgSuccess, msgError):
    saida = {
        'sucesso': False,
        'mensagem': msgError
    }

    if 'IsRowEffected' in value:
        saida['sucesso'] = value['IsRowEffected']

        if value['RowsEffected'] > 0:
            saida['mensagem'] = msgSuccess
        else:
            saida['mensagem'] = msgError

    else:
        saida['mensagem'] = msgError

    if 'Mensagem' in value:
        if 'ORA-20002' in value['Mensagem']:
            saida['mensagem'] = self.retorna_msg_oracle(value['Mensagem'])

    return saida