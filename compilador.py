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
    
    # Reconhecimento de numeros reais.
    # Aceita: inteiros (42) e reais com ponto (3.14).
    # Rejeita: multiplos pontos (3.14.5), virgulas (3,45).
    
    numero = ""

    while pos < len(linha) and linha[pos] >= '0' and linha[pos] <= '9':
        numero = numero + linha[pos]
        pos = pos + 1

    if pos < len(linha) and linha[pos] == '.':
        numero = numero + '.'
        pos = pos + 1

        if pos < len(linha) and linha[pos] >= '0' and linha[pos] <= '9':
            while pos < len(linha) and linha[pos] >= '0' and linha[pos] <= '9':
                numero = numero + linha[pos]
                pos = pos + 1

            if pos < len(linha) and linha[pos] == '.':
                while pos < len(linha) and linha[pos] != ' ' and linha[pos] != ')' and linha[pos] != '(':
                    numero = numero + linha[pos]
                    pos = pos + 1
                tokens.append((TOKEN_ERROR, numero))
                return pos
        else:
            tokens.append((TOKEN_ERROR, numero))
            return pos

    if pos < len(linha) and linha[pos] == ',':
        while pos < len(linha) and linha[pos] != ' ' and linha[pos] != ')' and linha[pos] != '(':
            numero = numero + linha[pos]
            pos = pos + 1
        tokens.append((TOKEN_ERROR, numero))
        return pos

    tokens.append((TOKEN_NUMBER, numero))
    return pos


def estadoOperador(linha, pos, tokens):
    # Estado do AFD para operadores simples: + - * ^ %
    tokens.append((TOKEN_OPERATOR, linha[pos]))
    pos = pos + 1
    return pos


def estadoDivisao(linha, pos, tokens):
    pos = pos + 1
    if pos < len(linha) and linha[pos] == '/':
        tokens.append((TOKEN_OPERATOR, "//"))
        pos = pos + 1
    else:
        tokens.append((TOKEN_OPERATOR, "/"))
    return pos

def estadoPalavraChave(linha, pos, tokens):

def estadoParenteses(linha, pos, tokens):

def parseExpressao(linha, _tokens_):
    #Analisa uma linha de expressao RPN e extrai os tokens.
    estadoInicial(linha.strip(), 0, _tokens_)

    for token in _tokens_:
        if token[0] == TOKEN_ERROR:
            print("ERRO LEXICO: token invalido '" + token[1] + "' na linha: " + linha.strip())
            return False

    nivel = 0
    for token in _tokens_:
        if token[0] == TOKEN_LPAREN:
            nivel = nivel + 1
        elif token[0] == TOKEN_RPAREN:
            nivel = nivel - 1
        if nivel < 0:
            print("ERRO: parentese de fechamento sem abertura na linha: " + linha.strip())
            return False
    if nivel != 0:
        print("ERRO: parenteses desbalanceados na linha: " + linha.strip())
        return False

    return True


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
    #Le arquivo de texto com expressoes RPN.
    try:
        arquivo = open(nomeArquivo, 'r', encoding='utf-8')
        for linha in arquivo:
            linha_limpa = linha.strip()
            if len(linha_limpa) > 0:
                linhas.append(linha_limpa)
        arquivo.close()
        return True
    except FileNotFoundError:
        print("ERRO: Arquivo '" + nomeArquivo + "' nao encontrado.")
        return False
    except PermissionError:
        print("ERRO: Sem permissao para ler '" + nomeArquivo + "'.")
        return False
    except Exception as e:
        print("ERRO ao ler arquivo: " + str(e))
        return False


def salvarTokens(tokens_por_linha, nomeArquivo):

def main():

if _name_ == "_main_":
    main()