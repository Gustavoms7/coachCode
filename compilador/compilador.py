import sys
import re
import random

# --- Parte 1: Definições de Tokens e Palavras-Chave (COMPLETO) ---

symbol_map = {
    "=": "ASSIGN_OP",
    "{": "OPEN_BRACE",
    "}": "CLOSE_BRACE",
    ";": "SEMICOLON",
    ".": "DOT",
    ">": "OP_GT",
    "<": "OP_LT",
    "==": "OP_EQ",
    "-": "HYPHEN",
}

reserved_words = {
    "DEFINIR": "CMD_DEFINIR", "time": "TYPE_TIME", "PARTIDA": "CMD_PARTIDA",
    "ataque": "ATTR_ATAQUE", "defesa": "ATTR_DEFESA", "meio_campo": "ATTR_MEIO_CAMPO",
    "formacao": "ATTR_FORMACAO", "estrategia": "ATTR_ESTRATEGIA",
    "casa": "ATTR_CASA", "visitante": "ATTR_VISITANTE",
    "SE": "KW_IF", "ENTAO": "KW_THEN", "SENAO": "KW_ELSE",
    "REPETIR": "KW_REPEAT", "VEZES": "KW_TIMES", "MOSTRAR": "KW_SHOW",
}

# --- Parte 2: Ferramentas de Análise (Léxica e Pré-processamento) ---

class SourcePreprocessor:
    @staticmethod
    def clean_source(code):
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code

class LexicalToken:
    def __init__(self, token_type, content, line_num):
        self.token_type = token_type
        self.content = content
        self.line_num = line_num
    def __repr__(self):
        return f"Token({self.token_type}, {self.content})"

class TokenGenerator:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line_num = 1
        self.next_token = None
        self.advance_token()

    def advance_token(self):
        if self.position >= len(self.source):
            self.next_token = LexicalToken("END", None, self.line_num)
            return

        char = self.source[self.position]

        if char in " \t\r\n":
            if char == '\n':
                self.line_num += 1
            self.position += 1
            return self.advance_token()

        if self.source[self.position:self.position+2] == '==':
            self.next_token = LexicalToken(symbol_map['=='], '==', self.line_num)
            self.position += 2
            return

        if char in symbol_map:
            self.next_token = LexicalToken(symbol_map[char], char, self.line_num)
            self.position += 1
            return

        if char == '"':
            self.position += 1
            text = ""
            while self.position < len(self.source) and self.source[self.position] != '"':
                text += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next_token = LexicalToken("STR_LIT", f'"{text}"', self.line_num)
            return

        if char.isdigit():
            num_str = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num_str += self.source[self.position]
                self.position += 1
            self.next_token = LexicalToken("NUMBER", int(num_str), self.line_num)
            return

        if char.isalpha() or char == '_':
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                identifier += self.source[self.position]
                self.position += 1
            
            token_type = reserved_words.get(identifier, "IDENTIFIER")
            self.next_token = LexicalToken(token_type, identifier, self.line_num)
            return

        raise ValueError(f"Caractere inválido: '{char}' na linha {self.line_num}")


# --- Parte 3: Nós da Árvore Sintática Abstrata (AST) e Execução ---

class ASTNode:
    def execute(self, environment):
        pass

class CodeBlock(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def execute(self, environment):
        for stmt in self.statements:
            stmt.execute(environment)

class TeamDefinitionNode(ASTNode):
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
    def execute(self, environment):
        print(f">> Time {self.name} definido com sucesso.")
        environment[self.name] = self.attributes

class MatchNode(ASTNode):
    def __init__(self, home_team_name, away_team_name):
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
    def execute(self, environment):
        home_name = self.home_team_name.strip('"')
        away_name = self.away_team_name.strip('"')
        print(f"\n--- RELATÓRIO TÁTICO: {home_name} vs. {away_name} ---")

        if self.home_team_name not in environment or self.away_team_name not in environment:
            raise ValueError("Erro: Um ou ambos os times da partida não foram definidos.")

        home = environment[self.home_team_name]
        away = environment[self.away_team_name]

        def simular_confronto(attr_casa, valor_casa, attr_vis, valor_vis):
            sorte_casa = random.randint(-10, 10)
            sorte_vis = random.randint(-10, 10)
            valor_sim_casa = valor_casa + sorte_casa
            valor_sim_vis = valor_vis + sorte_vis
            resultado = "Vantagem Casa" if valor_sim_casa > valor_sim_vis else "Vantagem Visitante" if valor_sim_casa < valor_sim_vis else "Equilíbrio"
            print(f"- {attr_casa} ({valor_casa}) vs. {attr_vis} ({valor_vis})")
            print(f"  Resultado Simulado: [{valor_sim_casa}] vs. [{valor_sim_vis}] -> {resultado}")

        print(f"\n[SIMULAÇÃO DE CONFRONTO DIRETO]")
        simular_confronto("Ataque Casa", home['ataque'], "Defesa Visitante", away['defesa'])
        simular_confronto("Meio-Campo Casa", home['meio_campo'], "Meio-Campo Visitante", away['meio_campo'])
        simular_confronto("Defesa Casa", home['defesa'], "Ataque Visitante", away['ataque'])

class ValueNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def evaluate(self, environment):
        return self.value

class AttributeAccessNode(ASTNode):
    def __init__(self, team_name, attribute):
        self.team_name = team_name
        self.attribute = attribute
    def evaluate(self, environment):
        if self.team_name not in environment:
            raise ValueError(f"Time {self.team_name} não definido.")
        if self.attribute not in environment[self.team_name]:
            raise ValueError(f"Atributo '{self.attribute}' não encontrado para o time {self.team_name}.")
        return environment[self.team_name][self.attribute]

class ConditionNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def evaluate(self, environment):
        left_val = self.left.evaluate(environment)
        right_val = self.right.evaluate(environment)
        if self.op.token_type == "OP_GT": return left_val > right_val
        if self.op.token_type == "OP_LT": return left_val < right_val
        if self.op.token_type == "OP_EQ": return left_val == right_val
        return False

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
    def execute(self, environment):
        if self.condition.evaluate(environment):
            self.then_block.execute(environment)
        elif self.else_block:
            self.else_block.execute(environment)

class RepeatNode(ASTNode):
    def __init__(self, times, block):
        self.times = times
        self.block = block
    def execute(self, environment):
        repeat_count = self.times.evaluate(environment)
        for i in range(repeat_count):
            print(f"\n[Repetição {i+1}/{repeat_count}]")
            self.block.execute(environment)

class ShowNode(ASTNode):
    def __init__(self, message):
        self.message = message
    def execute(self, environment):
        evaluated_message = self.message.evaluate(environment)
        cleaned_message = evaluated_message.strip('"')
        print(f"MOSTRAR: {cleaned_message}")

# --- Parte 4: Analisador Sintático (Parser) ---

class SyntaxParser:
    def __init__(self, source_code):
        self.tokenizer = TokenGenerator(source_code)

    def consume(self, expected_type):
        token = self.tokenizer.next_token
        if token.token_type == expected_type:
            self.tokenizer.advance_token()
            return token
        raise ValueError(f"Esperado token '{expected_type}', mas encontrou '{token.token_type}' na linha {token.line_num} com conteúdo '{token.content}'")

    def parse_program(self):
        statements = []
        while self.tokenizer.next_token.token_type != "END":
            statements.append(self.parse_statement())
        return CodeBlock(statements)

    def parse_statement(self):
        token_type = self.tokenizer.next_token.token_type
        if token_type == "CMD_DEFINIR": return self.parse_team_definition()
        if token_type == "CMD_PARTIDA": return self.parse_match()
        if token_type == "KW_IF": return self.parse_if_statement()
        if token_type == "KW_REPEAT": return self.parse_repeat_statement()
        if token_type == "KW_SHOW": return self.parse_show_statement()
        raise ValueError(f"Comando inesperado: {token_type} na linha {self.tokenizer.next_token.line_num}")

    def parse_attribute(self, attr_token, value_token_type):
        self.consume(attr_token)
        self.consume("ASSIGN_OP")
        value = self.consume(value_token_type).content
        self.consume("SEMICOLON")
        return value

    def parse_team_definition(self):
        self.consume("CMD_DEFINIR")
        self.consume("TYPE_TIME")
        team_name = self.consume("STR_LIT").content
        self.consume("OPEN_BRACE")
        attributes = {}
        
        def parse_multi_word_value():
            value_parts = []
            while self.tokenizer.next_token.token_type != "SEMICOLON":
                token = self.tokenizer.next_token
                # Adiciona o conteúdo do token à lista
                value_parts.append(str(token.content))
                # Avança para o próximo token
                self.tokenizer.advance_token()
            return " ".join(value_parts)

        attributes['ataque'] = self.parse_attribute("ATTR_ATAQUE", "NUMBER")
        attributes['defesa'] = self.parse_attribute("ATTR_DEFESA", "NUMBER")
        attributes['meio_campo'] = self.parse_attribute("ATTR_MEIO_CAMPO", "NUMBER")

        self.consume("ATTR_FORMACAO")
        self.consume("ASSIGN_OP")
        # Inclui hífens na junção, se existirem como tokens separados
        attributes['formacao'] = "".join(parse_multi_word_value().split())
        self.consume("SEMICOLON")

        self.consume("ATTR_ESTRATEGIA")
        self.consume("ASSIGN_OP")
        attributes['estrategia'] = parse_multi_word_value()
        self.consume("SEMICOLON")

        self.consume("CLOSE_BRACE")
        return TeamDefinitionNode(team_name, attributes)

    def parse_match(self):
        self.consume("CMD_PARTIDA")
        self.consume("OPEN_BRACE")
        home_team = self.parse_attribute("ATTR_CASA", "STR_LIT")
        away_team = self.parse_attribute("ATTR_VISITANTE", "STR_LIT")
        self.consume("CLOSE_BRACE")
        return MatchNode(home_team, away_team)

    def parse_block(self):
        self.consume("OPEN_BRACE")
        statements = []
        while self.tokenizer.next_token.token_type != "CLOSE_BRACE":
            statements.append(self.parse_statement())
        self.consume("CLOSE_BRACE")
        return CodeBlock(statements)

    def parse_if_statement(self):
        self.consume("KW_IF")
        condition = self.parse_condition()
        self.consume("KW_THEN")
        then_block = self.parse_block()
        else_block = None
        if self.tokenizer.next_token.token_type == "KW_ELSE":
            self.consume("KW_ELSE")
            else_block = self.parse_block()
        return IfNode(condition, then_block, else_block)

    def parse_repeat_statement(self):
        self.consume("KW_REPEAT")
        times = ValueNode(self.consume("NUMBER").content)
        self.consume("KW_TIMES")
        block = self.parse_block()
        return RepeatNode(times, block)

    def parse_show_statement(self):
        self.consume("KW_SHOW")
        message = ValueNode(self.consume("STR_LIT").content)
        self.consume("SEMICOLON")
        return ShowNode(message)

    def parse_value(self):
        if self.tokenizer.next_token.token_type == "NUMBER":
            return ValueNode(self.consume("NUMBER").content)
        elif self.tokenizer.next_token.token_type == "TYPE_TIME":
            self.consume("TYPE_TIME")
            self.consume("DOT")
            team_name = self.consume("STR_LIT").content
            self.consume("DOT")
            attr_token = self.tokenizer.next_token
            if attr_token.token_type in ["ATTR_ATAQUE", "ATTR_DEFESA", "ATTR_MEIO_CAMPO"]:
                self.tokenizer.advance_token()
                return AttributeAccessNode(team_name, attr_token.content)
            else:
                raise ValueError(f"Atributo desconhecido '{attr_token.content}' na linha {attr_token.line_num}")
        else:
            raise ValueError(f"Valor numérico ou acesso a atributo de time esperado na linha {self.tokenizer.next_token.line_num}.")

    def parse_condition(self):
        left = self.parse_value()
        op_token = self.tokenizer.next_token
        if op_token.token_type in ["OP_GT", "OP_LT", "OP_EQ"]:
            self.tokenizer.advance_token()
        else:
            raise ValueError(f"Operador de comparação esperado, mas encontrou {op_token.token_type}")
        right = self.parse_value()
        return ConditionNode(left, op_token, right)


# --- Parte 5: Execução Principal ---

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python compilador.py 'arquivo.coach'")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            source = file.read()

        source = SourcePreprocessor.clean_source(source)
        if not source.strip():
            raise ValueError("Arquivo de código fonte está vazio ou contém apenas comentários.")

        print("--- Iniciando Analise do coachCode ---")
        parser = SyntaxParser(source)
        ast = parser.parse_program()

        team_environment = {}
        ast.execute(team_environment)
        print("\n--- Analise concluida com sucesso ---")

    except Exception as e:
        print(f"\nERRO: {e}", file=sys.stderr)
        sys.exit(1)