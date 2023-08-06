import os
import subprocess

class TocaFita:
    def __init__(self):
        self.player = ''        
        '''
        DESCRIPTION
            Definição da classe Toca Fita
        :param:
            Player padrão que o usuário irá utilizar
        '''
    def Tocar(self, Music):
        try:
            subprocess.run([self.player, Music])       
        except:
            print('Erro ao tocar a musica!')
            print('Recomenda-se abrir arquivos de áudio e vídeo por reprodutores como o VLC Media Player')
            print('Link para Download: https://www.videolan.org')
        '''
        DESCRIPTION
            Função Tocar onde ocorre a chamada de subprocesso
        :param :
            O reprodutor e o diretorio de uma música
        '''
    
    def TocarLista(self, lista):
        try:
            lista.insert(0, self.player) 
            subprocess.run(lista)        
        
        except:
            print('Erro ao tocar a musica!')
            print('Recomenda-se abrir arquivos de áudio e vídeo por reprodutores como o VLC Media Player')
            print('Link para Download: https://www.videolan.org')
        '''
        DESCRIPTION
            Recebe uma lista de nomes de música, contidos no diretório. A primeira posição da lista é adicionada o reprodutor que irá toca-lás. (self.player)
        :param :
            Recebe uma lista de nomes com as  música
        '''