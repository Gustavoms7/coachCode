%{
#include "coach.tab.h" // Inclui os tokens que vamos definir no Bison
%}

%%

"DEFINIR"           { return DEFINIR; }
"time"              { return TIME; }
"ataque"            { return ATAQUE; }
"defesa"            { return DEFESA; }
"meio_campo"        { return MEIO_CAMPO; }
"formacao"          { return FORMACAO; }
"estrategia"        { return ESTRATEGIA; }
"PARTIDA"           { return PARTIDA; }
"casa"              { return CASA; }
"visitante"         { return VISITANTE; }

[0-9]+              { yylval.num = atoi(yytext); return NUMBER; }

\"[^\"]*\"           { 
                        // Remove as aspas do início e do fim da string
                        yytext[strlen(yytext) - 1] = '\0';
                        yylval.str = strdup(yytext + 1);
                        return STRING; 
                    }

"{"                 { return '{'; }
"}"                 { return '}'; }
"="                 { return '='; }
";"                 { return ';'; }

[ \t\n\r]+          { /* Ignora espaços, tabs e quebras de linha */ }

\/\*([^*]|\*+[^*/])*\*+\/ { /* Ignora comentários no formato C */ }

.                   { printf("Erro lexico: caractere desconhecido -> %s\n", yytext); }

%%

int yywrap() {
    return 1;
}