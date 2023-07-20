from asyncio.windows_events import NULL
import re
import string
from cv2 import line
from prettytable import PrettyTable
from utils import Error

from pyparsing import lineEnd



#lista de keywords
kwords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']


#lista de tokens
tokens = {
    ':=':'ASSIGN_VAR',
    '==':'EQUAL', 
    '=':'ASSIGN',
    '<=':'LTE', 
    '>=':'GTE',
    '!=':'DIFERENT',
    '>':'GT', 
    '<':'LT', 
    '/':'DIV',
     '-':'MINUS',
    '+':'PLUS', 
    '*':'MULT',
    '^':'puntero',
    'AND':'AND', 
    'OR':'OR',
    'NOT':'NOT',
    'DIV':'DIV',
    'MOD':'MOD',
    'IN':'IN'
        }


#lista de delimitadores
delimitadores = {
     '..':'DOTDOT', 
     '.':'DOT',
    ':':'COLON', 
    ';':'SEMICOLON', 
    ',':'COMMA',
    '[':'LCOL', 
    ']':'RCOL',
    '{':'LKEY', 
    '}':'RKEY',
    '(':'LBRACKET', 
    ')':'RBRACKET',
        }


#lista de tipos de datos
tipos= {'boolean': 'BOOLEAN',
    'integer': 'INTEGER',
    'INTEGER': 'INTEGER',
    'real': 'REAL',
    'REAL': 'REAL',
    'STRING': 'STRING',
    'string': 'STRING',}

#eliminar comentario con #
def eliminarComentario2(linea):
    linea = re.sub('#\S+', '', linea)
    return linea

#encontrar un elemento en la lista
def encontrar_elemento(elemento, lista):
    if elemento in lista: 
        return True
    return False

def eliminar_comentario(cadena):
    cadena_nueva = ''

    if(cadena[0] == '#'):
        return cadena_nueva

    if(cadena.find('#')):
        for i in range(len(cadena)):
            if(cadena[i] == '#'):
                return cadena_nueva
            cadena_nueva+=cadena[i]
    return cadena

def eliminarComentario3(linea):
    linea = re.sub('\(\*.*\*\)', '', linea)
    return linea

def eliminarComentario4(linea):
    if(linea.find('#')!=-1 and linea.find('\n')!=-1):
        tmp=linea[linea.find('#'):linea.find('\n')+1]
        linea=linea.replace(tmp,'')
    return linea


#eliminar saltos de linea y convertirlos en nada
def eliminarEspacios(linea):
    linea = re.sub('\n', '', linea)
    return linea

#eliminar espacios entre cada linea de codigo
def eliminarEspacios2(linea):
    linea = re.sub(' ', '', linea)
    return linea

    
class Token:
    type=NULL
    value=NULL
    row=NULL

    #defino valores de tabla
    def __init__(self, type, value, row):
        self.type = type
        self.value = value
        self.row = row

    #guardar los valores para imprimir en la tabla
    def __str__(self):
        return f'Type: {self.type}, Value: {self.value}, Row: {self.row}'

    #armar tabla
    def __repr__(self):
	    return self.__str__()


class Scannerr:
    #leer txt
    def __init__(self, file_path):
        self.file = open(file_path, 'r')
        self.data = None
        self.errors = []
        self.tokens = []
        self.value = []
        self.lista_tokens_parser = []
        
        self.tabla_simbolos = {}
        self.values = []
        self.values2 = []

        self.simbolos = 1


    def get_value(self):
        return "".join(self.value)

    def clean_value(self):
        self.value = []

    def printter(self):
        tokens = PrettyTable()
        tokens.field_names = ["Type", "value", "Row"]
        tokens.add_rows([
            [token.type, token.value, token.row] for token in self.tokens
        ])
        return tokens

    def printter_to_parser(self):
        self.lista_tokens_parser=[token.type for token in self.tokens]
        return self.lista_tokens_parser

    def imprimir_errores(self):
        with open('result.txt', 'w') as file:
            file.write("LEXEMAS: \n")
            for lex in self.values2:
                file.write('--->'+lex)

    def scan(self):
        row = 0
        for linea in self.file:

            row += 1
            
            #linea = eliminar_comentario(linea)
            #linea = eliminarEspacios(linea)
            if re.search("'.*'", linea):
                linea = re.sub("'.*'", re.search("'.*'", linea).group().replace(' ', '$'), linea)
            linea = linea.replace('"', "'")
            linea = linea.replace(';', ' ; ')
            linea = linea.replace(',', ' , ')
            linea = linea.replace('{', ' { ')
            linea = linea.replace('}', ' } ')
            linea = linea.replace('[', ' [ ')
            linea = linea.replace(']', ' ] ')
            linea = linea.replace(':', ' : ')


            linea = linea.replace('+', ' + ')
            linea = linea.replace('-', ' - ')
            linea = linea.replace('*', ' * ')
            linea = linea.replace('/', ' / ')
            
            
        
            linea = linea.replace('<', ' < ')
            linea = linea.replace('>', ' > ')
            linea = linea.replace('=', ' = ')
            linea = linea.replace('< >', ' <> ')
            linea = linea.replace('<>', ' <> ')
            linea = linea.replace(' !  = ', ' != ')
            linea = linea.replace(':=', ' := ')    
            linea = linea.replace('=  =', ' == ')
            linea = linea.replace(' :  =', ' := ')
            linea = linea.replace(' >  =', ' >= ')
            linea = linea.replace('> =', ' >= ')
            linea = linea.replace(' <  = ', ' <= ')
            linea = linea.replace('< =', ' <= ')
            linea = linea.replace('^', ' ^ ')
            linea = linea.replace(' \n}', ' } ')
            if(not re.search('\d+.\d+', linea)):
                linea = linea.replace(".", " . ")
            linea = linea.replace(' . .', ' .. ')
            linea = linea.replace(' ! =', ' != ')
            linea = linea.replace('(', ' ( ')
            linea = linea.replace('e + ', 'e+')
            linea = linea.replace('e - ', 'e-')
            linea=linea.replace("'''","''")
            linea = linea.replace(')', ' ) ').split()
            self.values.append(linea)

        for index, value in enumerate(self.values):
            for lex in value:

                #revisa si hay strings 
                if lex.find("'") != -1:
                    #revisa si se cierra el string
                    if(lex.count("'")%2 != 0):
                        self.values2.append('Error de string en la linea {}.\n'.format(index+1))
                        lex = ''
                    else:
                        self.values2.append('linea: {}, Lexema: {} , token( String, {} )\n'.format(index+1, lex.replace('$', ' '), lex.replace('$', ' ')))
                        self.tokens.append(Token('STRING_LITERAL', lex.replace('$', ' '), index+1))


                #numeros cientificos
                elif re.search(r"^[-+]?[\d]+\.?[\d]*[Ee](?:[-+]?[\d]+)?$", lex):
                    self.values2.append('linea: {}, Lexema: {} , token( {} , {} )\n'.format(index+1, lex, 'SCIENTIFIC_NUMBER', lex))
                    self.tokens.append(Token('SCIENTIFIC_NUMBER', lex, index+1))
                
                elif lex.upper() in kwords:
                    self.values2.append('linea: {}, Lexema: {} , token( Keyword , {} )\n'.format(index+1, lex, ''))
                    self.tokens.append(Token(lex.upper(), lex, index+1))
                elif lex.lower() in tipos:
                    self.values2.append('linea: {}, Lexema: {} , Tipo( Keyword , {} )\n'.format(index+1, lex, ''))
                    self.tokens.append(Token(tipos[lex], lex, index+1))
                elif lex in tokens.keys():
                    self.values2.append('linea: {}, Lexema: {} , token( {} , {} )\n'.format(index+1, lex, lex, tokens[lex]))
                    self.tokens.append(Token(tokens[lex], lex, index+1))
                elif lex in delimitadores.keys():
                    self.values2.append('linea: {}, Lexema: {} , delimitador( {} , {} )\n'.format(index+1, lex, lex, delimitadores[lex]))
                    self.tokens.append(Token(delimitadores[lex], lex, index+1))
               
                #buscar palabras
                elif re.search('^[_a-zA-Z]\w*$', lex): #usamos el lenguaje regular para hacer una busqueda
                    if lex not in self.tabla_simbolos.keys():
                        self.tabla_simbolos[lex] = ['linea: {}, Lexema: {} , token: {} , address: {} )\n'.format(index+1, lex, 'ID', self.simbolos), self.simbolos]
                        self.values2.append('linea: {}, Lexema: {} , token( {} , {} )\n'.format(index+1, lex, 'ID', self.simbolos))
                        self.simbolos += 1
                    else:
                        self.values2.append('linea: {}, Lexema: {} , token( {} , {} )\n'.format(index+1, lex, 'ID', self.tabla_simbolos[lex][1]))
                    self.tokens.append(Token('ID', lex, index+1))

                #encontrar numero solito
                elif re.search('^\d+$', lex):
                    self.values2.append('linea: {}, Lexema: {} , token( {} , {} )\n'.format(index+1, lex, 'INTEGER_CONST', lex))
                    self.tokens.append(Token('INTEGER_CONST', lex, index+1))
                    

                
                

                #errores
                else:
                    print("|"+lex+"|")
                    self.errors.append(Token('Lexical_Error',lex,index+1))
                    Error(lex, index+1, 'Lexical error')


    def imprimir(self):
        with open('result.txt', 'w') as file:
            file.write("LEXEMAS: \n")
            for lex in self.values2:
                file.write('--->'+lex)
