# coachCode
Repositório criado para a realização da APS de Lógica Computacional

Gustavo Mendes

## O coachCode
O coachCode é uma linguagem de programação declarativa, feita para modelar as características essenciais de times de futebol e simular o resultado de partidas. Nela, você atua definindo a formação de cada equipe, como seu poder de ataque e defesa, e estabelecendo suas táticas, como a formação e o estilo de jogo. Com base nessas configurações, a linguagem permite que um simulador determine o vencedor do confronto de forma lógica, traduzindo sua visão tática em um resultado.

## Gramatica EBNF

```
LETTER = ( "a" | "b" | "c" | ... | "Z" );
DIGIT = ( "0" | "1" | ... | "9" );
NUMBER = DIGIT, {DIGIT};
STRING = '"', {LETTER | DIGIT | " "}, '"';
COMMENT = "/*", {LETTER | DIGIT | " "}, "*/";

/* --- Definições Específicas de Futebol --- */

FORMACAO_TIPO = "4-4-2" | "4-3-3" | "3-5-2" | "5-3-2" ;
ESTRATEGIA_TIPO = "Contra-ataque" | "Posse de bola" | "Pressao alta" | "Defesa solida" ;

/* --- Estrutura Principal da Linguagem --- */

PROGRAMA = {DEFINIR_TIME}, {PARTIDA};

DEFINIR_TIME = "DEFINIR", "time", STRING, "{", 
    "ataque", "=", NUMBER, ";",
    "defesa", "=", NUMBER, ";",
    "meio_campo", "=", NUMBER, ";",
    "formacao", "=", FORMACAO_TIPO, ";",
    "estrategia", "=", ESTRATEGIA_TIPO, ";",
    "}" ;

PARTIDA = "PARTIDA", "{",
    "casa", "=", STRING, ";",
    "visitante", "=", STRING, ";",
    "}" ;

```
