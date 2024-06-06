from sympy import randprime, mod_inverse
from math import gcd

from sympy import randprime, mod_inverse, gcd

def obtenerClaves(dato):
    try:
        p = randprime(1, dato)
        q = randprime(1, dato)
        n = p * q
        phi = (p - 1) * (q - 1)
        
        e = 2
        while True:
            if phi % e != 0 and gcd(e, phi) == 1:  
                break
            e += 1
            
        clave_publica = e
        clave_privada = mod_inverse(clave_publica, phi)
        
        return clave_privada, clave_publica, n
    
    except ValueError as ve:
        # Captura errores de randprime si el rango dado es incorrecto
        raise ValueError("Error al generar los números primos") from ve
    except ZeroDivisionError as ze:
        # Captura errores si no se puede encontrar un número e coprimo con phi
        raise ValueError("No se puede encontrar un número e que sea coprimo con phi") from ze


def encriptar(base,clave_publica,modulo):
    binario = format(clave_publica,'b')
    x=1
    for num in binario:
        if num=='1':
            x=(pow(x,2)*base)%(modulo)
        else:
            x=pow(x,2)%modulo
    return x

def desencriptar(base,clave,modulo):
    binario = format(clave,'b')
    x=1
    for num in binario:
        if num=='1':
            x=(pow(x,2)*base)%(modulo)
        else:
            x=pow(x,2)%modulo
    return x

def split_encrypted_data(datos):
    chunks = []
    for numero in datos:
        str_num = str(numero)
        grupo = [str_num[i:i+2] for i in range(0, len(str_num), 2)]
        chunks.append(grupo)
    return chunks

def display_encrypted_data(chunks):
    ascii_resultado = []
    for grupo in chunks:
        ascii_grupo = ""
        for valor in grupo:
            if valor != '000':  
                valor_int = int(valor)
                if valor_int != 45:  
                    if 48 <= valor_int <= 57:  
                        ascii_grupo += valor + '-'
                    elif valor_int >= 33:
                        ascii_grupo += chr(valor_int) + '-'
                    else:
                        ascii_grupo += valor + '-'
        ascii_resultado.append(ascii_grupo.rstrip('-'))  
    data_formated = '  '.join(ascii_resultado) 
    return data_formated


def convert_ascii_to_decimal(encrypted_data):
    original_data = []
    current_number = ''
    for char in encrypted_data:
        if char.isdigit():
            current_number += char
        elif char == '-':
            if current_number:
                original_data.append(current_number)
                current_number = ''
        elif char == ' ':
            if current_number:
                original_data.append(current_number)
                current_number = ''
            original_data.append(' ')
        else:
            if current_number:
                original_data.append(current_number)
                current_number = ''
            if char == '0':
                current_number += char
            else:
                original_data.append(ord(char))
    if current_number:  # Agregar el último número si no se ha agregado todavía
        original_data.append(current_number)
    return original_data

def convertir_cadena(original_data):
    resultado = []
    numero = ''
    for elemento in original_data:
        if isinstance(elemento, int):
            numero += str(elemento)
        elif elemento == ' ':
            if len(numero) > 0:
                resultado.append(int(numero))
                numero = ''
        else:
            numero += elemento
    if len(numero) > 0:
        resultado.append(int(numero))
    return resultado



def convert_to_decimal(original_data):
    return [int(caracter) if caracter.isdigit() else ord(caracter) for caracter in original_data]


def encrypt_string(s, clave_publica, modulo):
    return [encriptar(ord(c), clave_publica, modulo) for c in s]

def decrypt_string(s, clave_privada, modulo):
    return ''.join(chr(desencriptar(c, clave_privada, modulo)) for c in s)




