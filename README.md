# coachCode ⚽
Repositório criado para a realização da Atividade Prática Supervisionada (APS) de Lógica Computacional.

**Autor:** Gustavo Mendes

---

## O coachCode
O **coachCode** é uma linguagem de domínio específico (DSL) e declarativa, criada para modelar as características de times de futebol e configurar uma partida. A linguagem permite definir os atributos de uma equipe (ataque, defesa, etc.) e suas táticas.

O projeto foi desenvolvido em duas etapas principais, cumprindo os requisitos da disciplina:
1.  Um **Analisador Sintático** (usando Flex e Bison) que valida a estrutura do código.
2.  Um **Interpretador** (escrito em Python) que executa o código, gerando um relatório de análise tática.

---
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

## Características
* **Sintaxe Declarativa:** O código descreve os times e a partida de forma direta, sem a necessidade de algoritmos complexos ou lógica de fluxo.
* **Modelagem de Atributos:** Permite definir a força de cada time através de valores numéricos para `ataque`, `defesa` e `meio_campo`, além de táticas como `formacao` e `estrategia`.
* **Análise em Duas Etapas:**
    * **Analisador Sintático (Flex/Bison):** Esta implementação foca exclusivamente em validar se um arquivo `.coach` está escrito corretamente de acordo com a gramática definida. A saída confirma apenas se a sintaxe é válida ou não.
    * **Interpretador (Python):** Esta implementação vai além da validação. Ela lê os dados, armazena o estado dos times e **executa uma análise tática**, gerando o relatório (o feedback) como saída final.

---

## Como Executar
O projeto possui duas implementações distintas que podem ser executadas.

### Versão 1: Analisador Sintático (Flex & Bison)
O objetivo desta etapa é **apenas validar a sintaxe** do código.

**Pré-requisitos:** `flex`, `bison`, `gcc` (ou `clang`).

**Passos (via terminal, na pasta `flex/`):**
1.  **Gerar os arquivos do parser e do scanner:**
    ```bash
    bison -d coach.y
    flex coach.l
    ```
2.  **Compilar o analisador:**
    ```bash
    gcc coach.tab.c lex.yy.c -o meu_analisador
    ```
3.  **Executar a validação sintática:**
    ```bash
    ./meu_analisador < exemplo.coach
    ```

### Versão 2: Interpretador de Análise Tática (Python)
Esta versão **executa a análise tática** e gera o relatório como saída.

**Pré-requisitos:** `Python 3.x`.

**Passos (via terminal, na pasta `compilador/`):**
1.  **Executar o interpretador:**
    ```bash
    python compilador.py exemplo.coach
    ```

---

## Exemplo de Código (`exemplo.coach`)
```coach
/* Arquivo de exemplo para demonstrar a sintaxe do coachCode */

DEFINIR time "Real Coders" {
    ataque = 90;
    defesa = 75;
    meio_campo = 80;
    formacao = "4-3-3";
    estrategia = "Pressao alta";
}

DEFINIR time "BugsUnited FC" {
    ataque = 70;
    defesa = 92;
    meio_campo = 85;
    formacao = "5-3-2";
    estrategia = "Defesa solida";
}

PARTIDA {
    casa = "Real Coders";
    visitante = "BugsUnited FC";
}
```
---

## Exemplos de Saída
Abaixo estão as saídas esperadas para o arquivo `exemplo.coach` em cada versão.

### Saída da Versão 1 (Flex & Bison)
*Esta saída confirma que a sintaxe do arquivo é válida.*
```text
--- Iniciando Analise Sintatica do coachCode ---

>> Time '"Real Coders"' definido com sucesso!
   Ataque: 90, Defesa: 75, Meio-campo: 80
   Formacao: "4-3-3", Estrategia: "Pressao alta"

>> Time '"BugsUnited FC"' definido com sucesso!
   Ataque: 70, Defesa: 92, Meio-campo: 85
   Formacao: "5-3-2", Estrategia: "Defesa solida"

>> Partida configurada: "Real Coders" (casa) vs. "BugsUnited FC" (visitante)

--- Analise sintatica concluida com sucesso. ---
```

### Saída da Versão 2 (Compilador)
*Esta saída é o relatório gerado pela execução e análise do código..*
```text
--- Iniciando Analise do coachCode ---
>> Time "Real Coders" definido com sucesso.
>> Time "BugsUnited FC" definido com sucesso.

--- RELATÓRIO TÁTICO: Real Coders vs. BugsUnited FC ---

[CONFRONTO DIRETO]
- Ataque Casa (90) vs. Defesa Visitante (92): Vantagem Visitante
- Meio-Campo Casa (80) vs. Meio-Campo Visitante (85): Vantagem Visitante
- Defesa Casa (75) vs. Ataque Visitante (70): Vantagem Casa

[SUGESTÃO PARA O TIME DA CASA: Real Coders]
- O adversário joga com 'Defesa solida'. Sugestão: adote uma estratégia de 'Posse de bola' para ter paciência e encontrar espaços.

--- Analise concluida com sucesso ---
```
