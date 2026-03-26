# ============================================================
# Analisador Léxico e Gerador de Código Assembly ARMv7
# Projeto de Compiladores - Fase 1
#
# Integrantes do grupo:
#   Eduardo Hideo Itinoseke Ogassawara
#   Gabriel Barbosa Fernandes de Oliveira
#
# Grupo 17
#
# ============================================================
import sys

TOKEN_NUMBER   = "NUMBER"
TOKEN_OPERATOR = "OPERATOR"
TOKEN_LPAREN   = "LPAREN"
TOKEN_RPAREN   = "RPAREN"
TOKEN_KEYWORD  = "KEYWORD"
TOKEN_ERROR    = "ERROR"

def estadoInicial(linha, pos, tokens):
#classifica e passa o caractere para o estado apro
    while pos < len(linha):
        c = linha[pos]

        if c == ' ' or c == '\t' or c == '\n' or c == '\r':
            pos = pos + 1

        elif c == '(':
            tokens.append((TOKEN_LPAREN, "("))
            pos = pos + 1

        elif c == ')':
            tokens.append((TOKEN_RPAREN, ")"))
            pos = pos + 1

        elif c == '+' or c == '-' or c == '*' or c == '^' or c == '%':
            pos = estadoOperador(linha, pos, tokens)

        elif c == '/':
            pos = estadoDivisao(linha, pos, tokens)

        elif c >= '0' and c <= '9':
            pos = estadoNumero(linha, pos, tokens)

        elif c >= 'A' and c <= 'Z':
            pos = estadoPalavraChave(linha, pos, tokens)

        elif c == ',':
            erro = c
            pos = pos + 1
            while pos < len(linha) and linha[pos] != ' ' and linha[pos] != ')' and linha[pos] != '(':
                erro = erro + linha[pos]
                pos = pos + 1
            tokens.append((TOKEN_ERROR, erro))

        else:
            tokens.append((TOKEN_ERROR, str(c)))
            pos = pos + 1

    return pos


def estadoNumero(linha, pos, tokens):

def estadoOperador(linha, pos, tokens):

def estadoDivisao(linha, pos, tokens):

def estadoPalavraChave(linha, pos, tokens):

def estadoParenteses(linha, pos, tokens):

def parseExpressao(linha, tokens):

def _potencia_inteira(base, expoente):

def _truncar(valor):

def executarExpressao(tokens, resultados, memoria):

def _avaliar_subexpressao(contexto, resultados, memoria):

def _gerar_operacoes_intermediarias(tokens, resultados_hist, memoria_nomes):

def _processar_subexpr_asm(contexto, resultados_hist, memoria_nomes):

def gerarAssembly(tokens, codigoAssembly):

def exibirResultados(resultados):

def testeProgramaCompleto(nomeArquivo):

def lerArquivo(nomeArquivo, linhas):

def salvarTokens(tokens_por_linha, nomeArquivo):

def main():

if _name_ == "_main_":
    main()