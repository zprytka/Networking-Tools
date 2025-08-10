#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import shodan
import fileinput

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--query", help="query para shodan")
parser.add_argument('-k', '--key', metavar='FILE', nargs='*', help='api key de shodan')
args = parser.parse_args()

def shodanSearch(key, query):
    try:
        motor = shodan.Shodan(key)
        resultado = motor.host(query)
        ip = resultado["ip_str"]
        for key,value in resultado.items():
            if key == "vulns":
                for vuln, descripcion in value.items():
                    print(ip, vuln, descripcion["verified"])
    except shodan.APIError as error:
        print(error)
        
def obtenerArchivo(argskey):
    input_text = ""
    retorno = ""
    if len(argskey) > 0:
        input_text = fileinput.input(files=argskey)
    else: 
        input_text = fileinput.input(files=('-', ))
    for line in input_text:
        retorno += line
    return retorno
    

if __name__ == '__main__':
    if args.query:
        if args.key:
            key = obtenerArchivo(args.key).strip()
            shodanSearch(key, args.query)
