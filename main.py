from scannerLast import Scanner
from scanner import Scannerr
from trabajoFinal import parser,code_translate
from utils import printter
file_path='ejemplo2.txt'
scanner = Scanner('ejemplo2.txt')
scanner.scan()
#scanner.imprimir()
print("Tokens:")
scanner.print_tokens()


print("---------------------------------------------------")
scannerr = Scannerr(file_path);
scannerr.scan()
scannerr.imprimir()



lista_tokens = []
lista_tokens = scannerr.printter_to_parser()
lista_tokens+=('$')
#print(scanner.tokenType)
#print(scanner.tokenName)
print("Errores Parser :")
scanner.print_errors()

p = parser(lista_tokens)

print("----------------------------------------------")
#imprimir arbol
p.parse()
p.listaErroress()
p.display_errors()
p.parse_all_tokens()
p.print_errors()

# Translate code and generate tree visualization
#code_translate(p.arbol, 'code.txt')



###
#scanner = Scanner('ejemploMis.txt')
#scanner.scan()

#print("Tokens:")
#scanner.print_tokens()

#print("Errors Scanner :")
#scanner.print_errors()
