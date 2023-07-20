import re
from prettytable import PrettyTable


class Scanner:
    def __init__(self, file_path):
        self.file = open(file_path, 'r')
        self.tokens = []
        self.errors = []
        self.tokenType=[]
        self.tokenName=[]
        self.keywords = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
        ]

    def scan(self):
        for line_num, line in enumerate(self.file, start=1):
            line = line.strip()
            # Remove comments starting with '#'
            comment_index = line.find('#')
            if comment_index != -1:
                line = line[:comment_index]

            column_num = 1  # Initialize column number    

            while line:
                if re.match(r'^[a-zA-Z][a-zA-Z0-9_]*', line):
                    identifier = re.match(r'^[a-zA-Z][a-zA-Z0-9_]*', line).group()
                    if identifier in self.keywords:
                        self.tokens.append(('KEYWORD', identifier, line_num, column_num))
                        self.tokenType.append('KEYWORD')
                        self.tokenName.append(identifier)
                        
                    else:
                        self.tokens.append(('IDENTIFIER', identifier, line_num, column_num))
                        self.tokenType.append('IDENTIFIER')
                        if len(identifier) ==1 :
                            self.tokenName.append('ID')
                        else:
                            self.tokenName.append(identifier)
                    line = line[len(identifier):].strip()
                elif re.match(r'^"[^\x00-\x1F\x7F]+"', line):
                    string_literal = re.match(r'^"[^\x00-\x1F\x7F]+"', line).group()
                    self.tokens.append(('STRING_LITERAL', string_literal, line_num, column_num))
                    self.tokenType.append('STRING_LITERAL')
                    self.tokenName.append(string_literal)
                    line = line[len(string_literal):].strip()
                elif re.match(r'^[0-9]+', line):
                    integer_literal = re.match(r'^[0-9]+', line).group()
                    if int(integer_literal) > 2147483647:
                        self.errors.append(('Lexical_Error', 'Integer value exceeds limit', line_num, column_num))
                    else:
                        self.tokens.append(('INTEGER_LITERAL', integer_literal, line_num, column_num))
                        self.tokenType.append('INTEGER_LITERAL')
                        self.tokenName.append(integer_literal)
                    line = line[len(integer_literal):].strip()
                elif re.match(r'^\+', line):
                    self.tokens.append(('PLUS', '+', line_num, column_num))
                    self.tokenType.append('OPERATOR_PLUS')
                    self.tokenName.append('+')
                    line = line[1:].strip()
                elif re.match(r'^-', line):
                    self.tokens.append(('MINUS', '-', line_num, column_num))
                    self.tokenType.append('OPERATOR_MINUS')
                    self.tokenName.append('-')
                    line = line[1:].strip()
                elif re.match(r'^\*', line):
                    self.tokens.append(('ASTERISK', '*', line_num, column_num))
                    self.tokenType.append('OPERATOR_ASTERISK')
                    self.tokenName.append('*')
                    line = line[1:].strip()
                elif re.match(r'^//', line):
                    self.tokens.append(('DOUBLE_SLASH', '//', line_num, column_num))
                    self.tokenType.append('OPERATOR_D_SLASH')
                    self.tokenName.append('//')
                    line = line[2:].strip()
                elif re.match(r'^%', line):
                    self.tokens.append(('PERCENT', '%', line_num, column_num))
                    self.tokenType.append('OPERATOR_PERCENT')
                    self.tokenName.append('%')
                    line = line[1:].strip()
                elif re.match(r'^<=', line):
                    self.tokens.append(('LESS_THAN_OR_EQUAL', '<=', line_num, column_num))
                    self.tokenType.append('OPERATOR_LTE')
                    self.tokenName.append('<=')
                    line = line[2:].strip()
                elif re.match(r'^>=', line):
                    self.tokens.append(('GREATER_THAN_OR_EQUAL', '>=', line_num, column_num))
                    self.tokenType.append('OPERATOR_GTE')
                    self.tokenName.append('>=')
                    line = line[2:].strip()
                elif re.match(r'^==', line):
                    self.tokens.append(('EQUAL_EQUAL', '==', line_num, column_num))
                    self.tokenType.append('OPERATOR_EE')
                    self.tokenName.append('==')
                    line = line[2:].strip()
                elif re.match(r'^!=', line):
                    self.tokens.append(('NOT_EQUAL', '!=', line_num, column_num))
                    self.tokenType.append('OPERATOR_NE')
                    self.tokenName.append('!=')
                    line = line[2:].strip()
                elif re.match(r'^<', line):
                    self.tokens.append(('LESS_THAN', '<', line_num, column_num))
                    self.tokenType.append('OPERATOR_LT')
                    self.tokenName.append('<')
                    line = line[1:].strip()
                elif re.match(r'^>', line):
                    self.tokens.append(('GREATER_THAN', '>', line_num, column_num))
                    self.tokenType.append('OPERATOR_GT')
                    self.tokenName.append('>')
                    line = line[1:].strip()
                elif re.match(r'^=', line):
                    self.tokens.append(('EQUAL', '=', line_num, column_num))
                    self.tokenType.append('OPERATOR_E')
                    self.tokenName.append('=')
                    line = line[1:].strip()
                elif re.match(r'^\(', line):
                    self.tokens.append(('LEFT_PAREN', '(', line_num, column_num))
                    self.tokenType.append('OPERATOR_LP')
                    self.tokenName.append('(')
                    line = line[1:].strip()
                elif re.match(r'^\)', line):
                    self.tokens.append(('RIGHT_PAREN', ')', line_num, column_num))
                    self.tokenType.append('OPERATOR_RP')
                    self.tokenName.append(')')
                    line = line[1:].strip()
                elif re.match(r'^\[', line):
                    self.tokens.append(('LEFT_BRACKET', '[', line_num, column_num))
                    self.tokenType.append('OPERATOR_LB')
                    self.tokenName.append('[')
                    line = line[1:].strip()
                elif re.match(r'^\]', line):
                    self.tokens.append(('RIGHT_BRACKET', ']', line_num, column_num))
                    self.tokenType.append('OPERATOR_RB')
                    self.tokenName.append(']')
                    line = line[1:].strip()
                elif re.match(r'^,', line):
                    self.tokens.append(('COMMA', ',', line_num, column_num))
                    self.tokenType.append('OPERATOR_CM')
                    self.tokenName.append(',')
                    line = line[1:].strip()
                elif re.match(r'^:', line):
                    self.tokens.append(('COLON', ':', line_num, column_num))
                    self.tokenType.append('OPERATOR_CL')
                    self.tokenName.append(':')
                    line = line[1:].strip()
                elif re.match(r'^\.', line):
                    self.tokens.append(('DOT', '.', line_num, column_num))
                    self.tokenType.append('OPERATOR_DOT')
                    self.tokenName.append('.')
                    line = line[1:].strip()
                elif re.match(r'^->', line):
                    self.tokens.append(('ARROW', '->', line_num, column_num))
                    self.tokenType.append('OPERATOR_ARROW')
                    self.tokenName.append('->')
                    line = line[2:].strip()
                else:
                    self.errors.append(('Lexical_Error', f'Invalid token: {line[0]}', line_num, column_num))
                    line = line[1:].strip()

                column_num += 1



    def print_tokenTypes(self):
        for tokenType in self.tokenType:
            print(tokenType)

    def print_tokenNames(self):
        for tokenName in self.tokenName:
            print(tokenName)         

    def print_tokens(self):
        table = PrettyTable(['Type', 'Value', 'Row','Column'])
        for token in self.tokens:
            table.add_row(token)
        print(table)

    def print_errors(self):
        for error in self.errors:
            print(error)

    def close_file(self):
        self.file.close()

    def printter_to_parser(self):
        lista_tokens_parser = [token_type for _, token_type, _, _ in self.tokens]
        return lista_tokens_parser
  


# Example usage
scanner = Scanner('ejemploMis.txt')
scanner.scan()

#print("Tokens:")
#scanner.print_tokens()

#print("Errors Scanner :")
#scanner.print_errors()

#scanner.print_tokenTypes()
#scanner.print_tokenNames()

tokensFinal = scanner.tokenName.copy()

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.errors = []

    def parse(self):
        self.next_token()
        self.program()
        if not self.errors:
            print("Parser funciona sin errores")
        else:
            for error in self.errors:
                print(error)

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    def match(self, expected_token):
        if self.current_token == expected_token:
            self.next_token()
        else:
            self.errors.append(f"Expected {expected_token}, found {self.current_token}")

    def program(self):
        self.def_list()

    def def_list(self):
        if self.current_token == "def":
            self.def_()
            self.def_list()

    def def_(self):
        self.match("def")
        self.match("ID")
        self.match("(")
        self.typed_var_list()
        self.match(")")
        self.return_()
        self.match(":")
        self.block()

    def typed_var_list(self):
        if self.current_token == "ID":
            self.typed_var()
            self.typed_var_list_tail()

    def typed_var_list_tail(self):
        if self.current_token == ",":
            self.match(",")
            self.typed_var()
            self.typed_var_list_tail()

    def typed_var(self):
        self.match("ID")
        self.match(":")
        self.type_()

    def type_(self):
        if self.current_token in ["int", "str"]:
            self.match(self.current_token)
        elif self.current_token == "[":
            self.match("[")
            self.type_()
            self.match("]")

    def return_(self):
        if self.current_token == "->":
            self.match("->")
            self.type_()

    def block(self):
        self.statement_list()

    def statement_list(self):
        if self.current_token in ["if", "while", "for", "ID", "pass", "return"]:
            self.statement()
            self.statement_list()

    def statement(self):
        if self.current_token == "if":
            self.match("if")
            self.expr()
            self.match(":")
            self.block()

        elif self.current_token == "while":
            self.while_loop()
        
        elif self.current_token == "for":
            self.match("for")
            self.match("ID")
            self.match("in")
            self.expr()
            self.match(":")
            self.block()

        elif self.current_token == "ID":
            self.match("ID")
        elif self.current_token == "pass":
            self.match("pass")
        elif self.current_token == "return":
            self.match("return")
            self.return_expr()

    def return_expr(self):
        if self.current_token != "NEWLINE":
            self.expr()
    
    def while_loop(self):
        self.match("while")
        self.expr()
        self.match(":")
        self.block()

    def expr(self):
        self.or_expr()

    def or_expr(self):
        self.and_expr()

    def and_expr(self):
        self.not_expr()

    def not_expr(self):
        if self.current_token == "not":
            self.match("not")
            self.comp_expr()
        else:
            self.comp_expr()

    def comp_expr(self):
        self.int_expr()

    def int_expr(self):
        self.term()

    def term(self):
        self.factor()

    def factor(self):
        if self.current_token == "-":
            self.match("-")
            self.factor()
        elif self.current_token == "ID":
            self.match("ID")
        elif self.current_token in ["None", "True", "False", "INTEGER", "STRING"]:
            self.match(self.current_token)
        elif self.current_token == "[":
            self.match("[")
            self.expr_list()
            self.match("]")
        elif self.current_token == "(":
            self.match("(")
            self.expr()
            self.match(")")

    def expr_list(self):
        if self.current_token != "]":
            self.expr()
            self.expr_list_tail()

    def expr_list_tail(self):
        if self.current_token == ",":
            self.match(",")
            self.expr()
            self.expr_list_tail()


# Lista de tokens
#tokens = ["def", "foo", "(", "x", ":", "int", ")", "->", "str", ":", "ID", "=", "ID", "NEWLINE", "def", "bar", "(", "y", ":", "str", ")", "->", "None", ":", "pass", "NEWLINE", "if", "x", "==", "1", ":", "pass", "else", ":", "pass", "NEWLINE", "INVALID"]

tokens = ["ID", "+", "ID"]

# Crear una instancia del parser
#parser = Parser(tokens)

# Ejecutar el análisis sintáctico
#parser.parse()
#scanner.close_file()

