%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex();
%}

%union {
    int num;
    char* str;
}

/* Declaração dos Tokens */
%token <str> STRING
%token <num> NUMBER
%token DEFINIR TIME ATAQUE DEFESA MEIO_CAMPO FORMACAO ESTRATEGIA
%token PARTIDA CASA VISITANTE

%%

/* Regras da Gramática */

programa:
    /* um programa pode ser vazio ou ter uma ou mais declaracoes */
    | declaracao programa
;

declaracao:
    definir_time
    | partida
;

definir_time:
    DEFINIR TIME STRING '{'
        ATAQUE '=' NUMBER ';'
        DEFESA '=' NUMBER ';'
        MEIO_CAMPO '=' NUMBER ';'
        FORMACAO '=' STRING ';'
        ESTRATEGIA '=' STRING ';'
    '}'
    {
        printf(">> Time '%s' definido com sucesso!\n", $3);
        printf("   Ataque: %d, Defesa: %d, Meio-campo: %d\n", $7, $11, $15);
        printf("   Formacao: %s, Estrategia: %s\n\n", $19, $23);
        free($3); free($19); free($23); // Libera a memória das strings
    }
;

partida:
    PARTIDA '{'
        CASA '=' STRING ';'
        VISITANTE '=' STRING ';'
    '}'
    {
        printf(">> Partida configurada: %s (casa) vs. %s (visitante)\n\n", $5, $9);
        free($5); free($9); // Libera a memória das strings
    }
;

%%

/* Funções Auxiliares */

void yyerror(const char *s) {
    fprintf(stderr, "Erro de Sintaxe: %s\n", s);
}

int main() {
    printf("--- Iniciando Analise Sintatica do coachCode ---\n\n");
    if (yyparse() == 0) {
        printf("--- Analise sintatica concluida com sucesso. ---\n");
    } else {
        printf("--- Erro na analise sintatica. ---\n");
    }
    return 0;
}