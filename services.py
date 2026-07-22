import hashlib
import os

def cript_senha(senha, salt_user=None):
       # criptografar
       senha_b = senha.encode()
       algoritmo = 'sha256'
       iteracoes = 100_000
       salt = bytes(16)    
       salt = salt_user or salt

       chave = hashlib.pbkdf2_hmac(algoritmo, senha_b, salt, iteracoes)

       string_registro_banco = f"{algoritmo}${iteracoes}${salt.hex()}${chave.hex()}"

       return string_registro_banco