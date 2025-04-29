# coachCode
Repositório criado para a realização da APS de Lógica Computacional

Gustavo Mendes

## O coachCode
SoccerScript é uma linguagem de domínio específico (DSL) criada para simular a experiência de ser um técnico de futebol. Com ela, é possível gerenciar a contratação de jogadores respeitando um orçamento definido, configurar formações táticas (como 4-4-2 ou 3-5-2), definir estratégias de jogo (como ataque rápido ou posse de bola) e treinar atributos do time, como chute e resistência. Além disso, a linguagem permite a simulação de partidas usando estruturas condicionais, possibilitando a execução de ações como atacar, defender, passar e substituir jogadores com base nas características do time e do adversário. O objetivo é oferecer uma forma divertida e programável de aplicar conceitos de lógica e estrutura de linguagens, aproximando o mundo do futebol da computação.

## Gramatica EBNF

```
LETTER = ( "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" |
           "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" );

DIGIT = ( "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" );

NUMBER = DIGIT, {DIGIT};

STRING = '"', {LETTER | " "}, '"';

IDENTIFIER = LETTER, {LETTER | DIGIT | "_"};  

VALUE = STRING | NUMBER | LIST | PLAYER | SPELL | MISSION;

LIST = "[", VALUE, {",", VALUE}, "]";

COMMENT = "/*", {LETTER | DIGIT | " "}, "*/";

TEAM = "time", IDENTIFIER, "(", "orcamento", NUMBER, ")", "{", { PLAYER_CONTRACT }, "}";

PLAYER_CONTRACT = "contratar", "(", STRING, ",", NUMBER, ")", ";";

FORMATION = "formacao", "(", NUMBER, ",", NUMBER, ",", NUMBER, ")", ";";

STRATEGY = "estrategia", "(", STRING, ")", ";";

TRAINING = "treino", IDENTIFIER, "{", { TRAINING_ACTION }, "}";

TRAINING_ACTION = "treinar", "(", STRING, ",", NUMBER, ")", ";";

MATCH = "jogo", IDENTIFIER, "{", { COMMAND }, "}";

COMMAND = CONDITIONAL
        | ACTION
        ;

CONDITIONAL = "se", "(", EXPRESSION, ")", "{", { COMMAND }, "}", [ "senao", "{", { COMMAND }, "}" ];

EXPRESSION = IDENTIFIER, ".", ATTRIBUTE, COMPARISON_OPERATOR, NUMBER;

ATTRIBUTE = "ataque" | "defesa" | "energia" | "habilidade";

COMPARISON_OPERATOR = ">" | "<" | "==" | "!=";

ACTION = "chute", "(", STRING, ")", ";"
       | "passe", "(", STRING, ")", ";"
       | "defesa", "(", ")", ";"
       | "substituicao", "(", STRING, ",", STRING, ")", ";"
       | "atacar", "(", ")", ";"
       | "defender", "(", ")", ";"
       ;

BLOCK = "{", { STATEMENT }, "}";

STATEMENT = TEAM
          | FORMATION
          | STRATEGY
          | TRAINING
          | MATCH
          | CHARACTER
          | SPELL
          | MISSION
          | CAST
          | CONDITIONAL
          | LOOP
          | ASSIGNMENT
          | EXPRESSION
          | ADVANCE_MISSION
          ;

ASSIGNMENT = IDENTIFIER, ".", IDENTIFIER, "=", EXPRESSION, ";";

LOOP = "WHILE_THE_MOON_SHINES", CONDITION_BLOCK, BLOCK;

CONDITION_BLOCK = CONDITION, BLOCK;

CONDITION = EXPRESSION, ("<" | ">" | "=" | "!="), EXPRESSION;

ADVANCE_MISSION = "MISSION_STEP", STRING, "TO", STRING, ";";

CAST = "CAST", "SPELL", STRING, "BY", STRING, "ON", STRING, ";";

MISSION = "CREATE", "mission", STRING, "{", 
          "objective", "=", STRING, ";", 
          "participants", "=", LIST, ";", 
          "reward", "=", LIST, ";", 
          "location", "=", STRING, ";", 
          "}";

SPELL = "CREATE", "spell", STRING, "{", 
        "power", "=", NUMBER, ";", 
        "mana_cost", "=", NUMBER, ";", 
        "effect", "=", STRING, ";", 
        "}";

PLAYER = "CREATE", "character", STRING, "{", 
         "attributes", "=", "{", 
         "strength", "=", NUMBER, ";", 
         "mana", "=", NUMBER, ";", 
         "life", "=", NUMBER, ";", 
         "mana_regen", "=", NUMBER, ";", 
         "inventory", "=", LIST, ";",     
         "}", "}";


```
