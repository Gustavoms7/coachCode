# coachCode ⚽
Repositório criado para a realização da Atividade Prática Supervisionada (APS) de Lógica Computacional.

**Autor:** Gustavo Mendes

---

## O coachCode
O coachCode é uma linguagem de domínio específico (DSL) projetada para a análise tática de partidas de futebol. Ela combina uma sintaxe declarativa para modelar as características de times (ataque, defesa, formação, etc.) com comandos procedurais que permitem a criação de simulações dinâmicas e análises condicionais.

O objetivo da linguagem é permitir que um "técnico" configure seus times e, em seguida, execute scripts para obter relatórios táticos, testar cenários e simular o resultado de confrontos, que variam a cada execução graças a um "Fator Sorte" que torna as partidas imprevisíveis.

---
---
## Apresentação canva: 
https://www.canva.com/design/DAGp9p7O6CY/0i0r25KSW6X-bkaT23uzNA/edit?utm_content=DAGp9p7O6CY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
---
## Gramatica EBNF



```
PROGRAMA = {COMANDO};

/* --- Comandos Principais --- */
COMANDO = ( DEFINIR_TIME | PARTIDA | BLOCO_SE | BLOCO_REPETIR | MOSTRAR_COMANDO | COMMENT );

DEFINIR_TIME = "DEFINIR", "time", STRING, "{", 
    "ataque", "=", NUMBER, ";",
    "defesa", "=", NUMBER, ";",
    "meio_campo", "=", NUMBER, ";",
    "formacao", "=", VALOR_TEXTO, ";",
    "estrategia", "=", VALOR_TEXTO, ";",
    "}" ;

PARTIDA = "PARTIDA", "{",
    "casa", "=", STRING, ";",
    "visitante", "=", STRING, ";",
    "}" ;

/* --- Comandos de Controle de Fluxo --- */
BLOCO_SE = "SE", CONDICAO, "ENTAO", "{", {COMANDO}, "}", [ "SENAO", "{", {COMANDO}, "}" ];

BLOCO_REPETIR = "REPETIR", NUMBER, "VEZES", "{", {COMANDO}, "}";

MOSTRAR_COMANDO = "MOSTRAR", STRING, ";";

/* --- Estruturas de Condição --- */
CONDICAO = VALOR, OPERADOR_COMPARACAO, VALOR;
VALOR = ( NUMBER | ATRIBUTO_TIME );
ATRIBUTO_TIME = "time", ".", STRING, ".", ("ataque" | "defesa" | "meio_campo");
OPERADOR_COMPARACAO = ">" | "<" | "==" ;

/* --- Literais e Tipos Básicos --- */
VALOR_TEXTO = { (IDENTIFIER | NUMBER | "-") };
LETTER = ( "a" | "b" | ... | "Z" );
DIGIT = ( "0" | "1" | ... | "9" );
NUMBER = DIGIT, {DIGIT};
STRING = '"', {LETTER | DIGIT | " "}, '"';
IDENTIFIER = LETTER, {LETTER | DIGIT | "_"};
COMMENT = "/*", {LETTER | DIGIT | " "}, "*/";
```

## Características
- **Linguagem Híbrida:** Combina a clareza da sintaxe declarativa para definir os times com o poder de comandos procedurais (SE, REPETIR) para criar análises complexas.
- **Controle de Fluxo para Análise:**
    - **SE...ENTAO...SENAO:** Permite criar análises que dependem dos atributos das equipes, exibindo mensagens diferentes para cada cenário.
    - **REPETIR...VEZES:** Facilita a execução de múltiplas simulações de uma mesma partida para observar diferentes resultados possíveis.
- **Simulação Dinâmica com "Fator Sorte":** O coração da linguagem. Cada vez que uma **PARTIDA** é simulada, os atributos dos times recebem uma pequena variação aleatória. Isso significa que um time mais fraco pode, com sorte, vencer um mais forte, tornando as repetições mais realistas e interessantes.
- **Análise Semântica e Execução:** O interpretador em Python não apenas valida a sintaxe, mas também realiza uma análise semântica, gerenciando o estado dos times definidos e executando a lógica do script para gerar relatórios dinâmicos.

---

## Como Executar
###  Interpretador de Análise Tática (Python)
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
/*
  APS Lógica Computacional - Exemplo Final
  Linguagem: coachCode
  Demonstração de definição de times, condicionais,
  loops e simulação com aleatoriedade.
*/

DEFINIR time "Guerreiros da IA" {
    ataque = 95;
    defesa = 70;
    meio_campo = 88;
    formacao = 4-3-3;
    estrategia = Pressao alta;
}

DEFINIR time "Gigantes do Algoritmo" {
    ataque = 82;
    defesa = 85;
    meio_campo = 90;
    formacao = 3-5-2;
    estrategia = Posse de bola;
}

MOSTRAR "Análise pré-jogo iniciada.";

SE time."Guerreiros da IA".ataque > time."Gigantes do Algoritmo".ataque ENTAO {
    MOSTRAR "Os Guerreiros possuem um ataque nominalmente superior.";
} SENAO {
    MOSTRAR "Os Gigantes possuem um ataque nominalmente superior ou equivalente.";
}

MOSTRAR "Iniciando simulação de 3 confrontos...";

REPETIR 3 VEZES {
    PARTIDA {
        casa = "Guerreiros da IA";
        visitante = "Gigantes do Algoritmo";
    }
}
```
---

## Exemplos de Saída
Abaixo estão as saídas esperadas para o arquivo `exemplo.coach` em cada versão.


### Saída  (Compilador)
*Esta saída é o relatório gerado pela execução e análise do código..*
```text
--- Iniciando Analise do coachCode ---
>> Time "Guerreiros da IA" definido com sucesso.
>> Time "Gigantes do Algoritmo" definido com sucesso.
MOSTRAR: Análise pré-jogo iniciada.
MOSTRAR: Os Guerreiros possuem um ataque nominalmente superior.
MOSTRAR: Iniciando simulação de 3 confrontos...

[Repetição 1/3]

--- RELATÓRIO TÁTICO: Guerreiros da IA vs. Gigantes do Algoritmo ---

[SIMULAÇÃO DE CONFRONTO DIRETO]
- Ataque Casa (95) vs. Defesa Visitante (85)
  Resultado Simulado: [97] vs. [95] -> Vantagem Casa
- Meio-Campo Casa (88) vs. Meio-Campo Visitante (90)
  Resultado Simulado: [83] vs. [83] -> Equilíbrio
- Defesa Casa (70) vs. Ataque Visitante (82)
  Resultado Simulado: [66] vs. [84] -> Vantagem Visitante

[Repetição 2/3]

--- RELATÓRIO TÁTICO: Guerreiros da IA vs. Gigantes do Algoritmo ---

[SIMULAÇÃO DE CONFRONTO DIRETO]
- Ataque Casa (95) vs. Defesa Visitante (85)
  Resultado Simulado: [89] vs. [89] -> Equilíbrio
- Meio-Campo Casa (88) vs. Meio-Campo Visitante (90)
  Resultado Simulado: [88] vs. [85] -> Vantagem Casa
- Defesa Casa (70) vs. Ataque Visitante (82)
  Resultado Simulado: [60] vs. [77] -> Vantagem Visitante

[Repetição 3/3]

--- RELATÓRIO TÁTICO: Guerreiros da IA vs. Gigantes do Algoritmo ---

[SIMULAÇÃO DE CONFRONTO DIRETO]
- Ataque Casa (95) vs. Defesa Visitante (85)
  Resultado Simulado: [102] vs. [81] -> Vantagem Casa
- Meio-Campo Casa (88) vs. Meio-Campo Visitante (90)
  Resultado Simulado: [83] vs. [88] -> Vantagem Visitante
- Defesa Casa (70) vs. Ataque Visitante (82)
  Resultado Simulado: [65] vs. [90] -> Vantagem Visitante

--- Analise concluida com sucesso ---
```
