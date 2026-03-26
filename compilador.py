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

def estadoInicial(linha, pos, tokens):

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
    """Le arquivo de texto com expressoes RPN."""
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