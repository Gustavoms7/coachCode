import sys
import re

# --- Parte 1: Definições de Tokens e Palavras-Chave para coachCode ---

# Mapeamento de símbolos para coachCode
symbol_map = {
    "=": "ASSIGN_OP",
    "{": "OPEN_BRACE",
    "}": "CLOSE_BRACE",
    ";": "SEMICOLON",
}

# Palavras reservadas do coachCode
reserved_words = {
    "DEFINIR": "CMD_DEFINIR",
    "time": "TYPE_TIME",
    "ataque": "ATTR_ATAQUE",
    "defesa": "ATTR_DEFESA",
    "meio_campo": "ATTR_MEIO_CAMPO",
    "formacao": "ATTR_FORMACAO",
    "estrategia": "ATTR_ESTRATEGIA",
    "PARTIDA": "CMD_PARTIDA",
    "casa": "ATTR_CASA",
    "visitante": "ATTR_VISITANTE",
}

# --- Parte 2: Ferramentas de Análise (Léxica e Pré-processamento) ---

class SourcePreprocessor:
    @staticmethod
    def clean_source(code):
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'#.*', '', code)
        return re.sub(r'//.*', '', code)

class LexicalToken:
    def __init__(self, token_type, content, line_num):
        self.token_type = token_type
        self.content = content
        self.line_num = line_num

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

        if char in " \t\r":
            self.position += 1
            return self.advance_token()
        if char == "\n":
            self.position += 1
            self.next_token = LexicalToken("NEWLINE", "\n", self.line_num)
            self.line_num += 1
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
        
        if char in symbol_map:
            self.next_token = LexicalToken(symbol_map[char], char, self.line_num)
            self.position += 1
            return
        
        if char.isalpha():
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
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
        home_name_no_quotes = self.home_team_name.strip('"')
        away_name_no_quotes = self.away_team_name.strip('"')

        print(f"\n--- RELATÓRIO TÁTICO: {home_name_no_quotes} vs. {away_name_no_quotes} ---")
        
        if self.home_team_name not in environment or self.away_team_name not in environment:
            raise ValueError("Erro: Um ou ambos os times da partida não foram definidos.")

        home = environment[self.home_team_name]
        away = environment[self.away_team_name]

        print(f"\n[CONFRONTO DIRETO]")
        print(f"- Ataque Casa ({home['ataque']}) vs. Defesa Visitante ({away['defesa']}): {'Vantagem Casa' if home['ataque'] > away['defesa'] else 'Vantagem Visitante' if home['ataque'] < away['defesa'] else 'Equilíbrio'}")
        print(f"- Meio-Campo Casa ({home['meio_campo']}) vs. Meio-Campo Visitante ({away['meio_campo']}): {'Vantagem Casa' if home['meio_campo'] > away['meio_campo'] else 'Vantagem Visitante' if home['meio_campo'] < away['meio_campo'] else 'Equilíbrio'}")
        print(f"- Defesa Casa ({home['defesa']}) vs. Ataque Visitante ({away['ataque']}): {'Vantagem Casa' if home['defesa'] > away['ataque'] else 'Vantagem Visitante' if home['defesa'] < away['ataque'] else 'Equilíbrio'}")

        print(f"\n[SUGESTÃO PARA O TIME DA CASA: {home_name_no_quotes}]")
        if away['estrategia'] == '"Defesa solida"':
            print("- O adversário joga com 'Defesa solida'. Sugestão: adote uma estratégia de 'Posse de bola' para ter paciência e encontrar espaços.")
        elif away['ataque'] > home['defesa'] + 10:
            print("- O ataque adversário é muito forte. Sugestão: reforce a defesa com uma formação '5-3-2'.")
        else:
            print("- O confronto parece equilibrado. Mantenha sua tática e explore seu jogador-chave.")

# --- Parte 4: Analisador Sintático (Parser) para coachCode ---

class SyntaxParser:
    def __init__(self, source_code):
        self.tokenizer = TokenGenerator(source_code)

    # FUNÇÃO ADICIONADA para tornar o parser mais flexível
    def skip_newlines(self):
        """Avança o token enquanto ele for uma quebra de linha."""
        while self.tokenizer.next_token.token_type == "NEWLINE":
            self.tokenizer.advance_token()
            
    def parse_program(self):
        statements = []
        self.skip_newlines() # Pula newlines no início do arquivo
        while self.tokenizer.next_token.token_type != "END":
            token_type = self.tokenizer.next_token.token_type
            if token_type == "CMD_DEFINIR":
                statements.append(self.parse_team_definition())
            elif token_type == "CMD_PARTIDA":
                statements.append(self.parse_match())
            else:
                raise ValueError(f"Comando inesperado no início de um bloco: {token_type}")
            self.skip_newlines() # Pula newlines entre os blocos
        return CodeBlock(statements)

    def consume(self, expected_type):
        """ Avança o token, verificando se é do tipo esperado. """
        token = self.tokenizer.next_token
        if token.token_type == expected_type:
            self.tokenizer.advance_token()
            return token
        raise ValueError(f"Esperado token '{expected_type}', mas encontrou '{token.token_type}' na linha {token.line_num}")

    # FUNÇÃO ATUALIZADA
    def parse_team_definition(self):
        self.consume("CMD_DEFINIR")
        self.consume("TYPE_TIME")
        team_name = self.consume("STR_LIT").content
        self.consume("OPEN_BRACE")
        self.skip_newlines()  # <--- CORREÇÃO

        attributes = {}
        attributes['ataque'] = self.parse_attribute("ATTR_ATAQUE", "NUMBER")
        attributes['defesa'] = self.parse_attribute("ATTR_DEFESA", "NUMBER")
        attributes['meio_campo'] = self.parse_attribute("ATTR_MEIO_CAMPO", "NUMBER")
        attributes['formacao'] = self.parse_attribute("ATTR_FORMACAO", "STR_LIT")
        attributes['estrategia'] = self.parse_attribute("ATTR_ESTRATEGIA", "STR_LIT")

        self.skip_newlines()  # <--- CORREÇÃO
        self.consume("CLOSE_BRACE")
        return TeamDefinitionNode(team_name, attributes)

    # FUNÇÃO ATUALIZADA
    def parse_match(self):
        self.consume("CMD_PARTIDA")
        self.consume("OPEN_BRACE")
        self.skip_newlines()  # <--- CORREÇÃO
        
        home_team = self.parse_attribute("ATTR_CASA", "STR_LIT")
        away_team = self.parse_attribute("ATTR_VISITANTE", "STR_LIT")

        self.skip_newlines()  # <--- CORREÇÃO
        self.consume("CLOSE_BRACE")
        return MatchNode(home_team, away_team)

    def parse_attribute(self, attr_token, value_token):
        """ Função genérica para parsear uma linha de atributo. """
        self.skip_newlines() # Permite newlines antes de cada atributo
        self.consume(attr_token)
        self.consume("ASSIGN_OP")
        value = self.consume(value_token).content
        self.consume("SEMICOLON")
        return value

# --- Parte 5: Execução Principal ---

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python coach_interpreter.py 'arquivo.coach'")
        sys.exit(1)
        
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            source = file.read()

        source = SourcePreprocessor.clean_source(source)
        if not source.strip():
            raise ValueError("Arquivo de código fonte está vazio.")

        print("--- Iniciando Analise do coachCode ---")
        parser = SyntaxParser(source)
        ast = parser.parse_program()
        
        team_environment = {} 
        ast.execute(team_environment)
        print("\n--- Analise concluida com sucesso ---")

    except Exception as e:
        print(f"\nErro: {e}", file=sys.stderr)
        sys.exit(1)