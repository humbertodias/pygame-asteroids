# coding: utf-8

"""
Manipula Arquivo.
"""
__author__  = 'Humberto Lino'
__version__ = '1.0'


import sys,os
import pickle
import codecs


from score import *



class FileManager:
    CHARSET = 'utf-8'
    def load(self, file_name
                 , file_format = {'janela': 2
                                 ,'passo_simulacao': 1
                                 ,'vidas': 1
                                 ,'controle' : 1
                                 ,'asteroide': -1
                                 ,'tela_cheia': 1
                                 ,'mostrar_mouse': 1}
                 , sep=' '):
        """
        Carregar arquivo
        @param file_name:  Nome do arquivo
        @param file_format: Formato do arquivo
        @param sep:  Separador
        @return: Mapa preenchido
        """

        if not os.path.exists(file_name):
            raise RuntimeError('Arquivo %s não encontrado!\nCrie-o com o seguinte formato: %s' % (self.inFileName, self.get_file_format()))

        map = {}
        with codecs.open(file_name, 'r', self.CHARSET) as lines:
            for line in lines :

                if len(line)>1 and not line.startswith('#'):

                    key, values = line.split(sep,1)
                    lvalues = values.strip().split(sep)
                    if key in file_format:
                        if file_format[key] == -1 or len(lvalues) == file_format[key]:
                            if key in map:
                                map[key] += [lvalues]
                            else:
                                map[key] = [lvalues]
                        else:
                            raise RuntimeError('Line with key [%s] must contains [%d] values' % (key,len(lvalues)))

        return map



    def unmarshal_marshal(self, file_name, default_object):
        object = self.unmarshal(file_name)
        if object == None:
            object = default_object
            self.marshal(file_name, default_object)

        return object

    def unmarshal(self, file_name):
        object = None
        if os.path.exists(file_name):
            with open(file_name,'rb+') as file:
                object = pickle.load(file)

        return object

    def get_pickle_fixed_protocol(self):

        # Pickle uses different protocols to convert your data to a binary stream.
        # In python 2 there are 3 different protocols (0, 1, 2) and the default is 0.
        # In python 3 there are 5 different protocols (0, 1, 2, 3, 4) and the default is 3.
        if sys.version_info[0] == 2:
            return 0
        else:
            return 3

    def marshal(self, file_name, object):
        with open(file_name, 'wb+') as file:
            pickle.dump(object, file,  self.get_pickle_fixed_protocol() )
