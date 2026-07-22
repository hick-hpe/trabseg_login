import hashlib
import os

def cript_senha(senha, salt_user=None):
       # criptografar
       senha_b = senha.encode()
       algoritmo = 'sha256'
       iteracoes = 100_000
       salt = salt_user or bytes(16)

       chave = hashlib.pbkdf2_hmac(algoritmo, senha_b, salt, iteracoes)

       string_registro_banco = f"$pbkdf2${algoritmo}${iteracoes}${salt.hex()}${chave.hex()}"

       return string_registro_banco