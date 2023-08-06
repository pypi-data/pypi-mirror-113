from collections import Counter

class PackPOOII():
    """Aplica métodos para manipulação de texto
    
    """
    def __init__(self):
        pass

    def subString(self, palavra):
        """ Procura uma sub-string dentro de uma determinada string

        Parametros
        ----------
        palavra : str
        Endereço da string 
    
        """
        total = 0
        for letras in range(len(palavra)):
            if(palavra[letras: letras+6] == "banana"):
                total += 1
        return total
    

    def deleteLine(self, arq_text, linha):
        """ Deleta uma linha de um arquivo de texto

        Parametros
        ----------
        arq_text : str
        Nome do arquivo de texto, com a extenção.

        linha : str
        Conteúdo da linha de se deseja excluir 
    
        """
        with open(arq_text, "r") as f:
            lines = f.readlines()
        with open(arq_text, "w") as f:
            for line in lines:
                if line.strip("\n") != linha:
                    f.write(line)


    def popularidade(self, arq_text, palavras):
        """ Retorna quantas vezes uma ou mais palavras aparecem em um arquivo de texto

        Parametros
        ----------
        arq_text : str
        Nome do arquivo de texto, com a extenção

        palavras : str
        Palavras que se deseja obter 
    
        """ 
        palavras = palavras.lower().replace(',', '').split() # tirar virgulas

        lista = []
        with open(arq_text, "r") as f:
            lines = f.readlines()
        with open(arq_text, "r") as f:
            for line in lines:
                texto = line.lower().split()
                for p in palavras:
                    for t in texto:
                        if p == t:
                            lista.append(t)
        return Counter(lista) # return quando todas as palavras verificadas

    def cor(palavra, cor):
        """ Retorna a palavra com a cor escolhida

        Parametros
        ----------
        palavra : str
        Texto para ter sua cor alterada

        cor : str
        Cor escolhida para o texto 
    
        """ 
        cor = cor.upper()
        if cor == "YELLOW":
            pYellow = f"\033[33m{palavra} \033[m"
            return pYellow
        elif cor == "BLACK":
            pBlack = f"\033[30m{palavra} \033[m"
            return pBlack
        elif cor == "RED":
            pRed = f"\033[1;31m{palavra} \033[m"
            return pRed
        elif cor == "BLUE":
            pBlue = f"\033[1;34m{palavra} \033[m"
            return pBlue
        elif cor == "CIAN":
            pCian = f"\033[1;36m{palavra} \033[m"
            return pCian
        elif cor == "GREEN":
            pGreen = f"\033[1;32m{palavra} \033[m"
            return pGreen
        elif cor == "WHITE":
            pWhite = f"\033[37m{palavra} \033[m"
            return pWhite
        else:
            return "Cor não existe"