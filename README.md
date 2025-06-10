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
