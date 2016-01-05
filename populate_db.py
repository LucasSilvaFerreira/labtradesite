__author__ = 'lucas'
# -*- coding: utf-8 -*-
import random
import time

from tinydb import TinyDB, where, Query
import os






import sys


def main():
    nomes = open('/home/lucas/PycharmProjects/reagenttrade/Nomes.txt','r').read().split('\n')
    produtos = open('/home/lucas/PycharmProjects/reagenttrade/materiais.txt','r').read().split('\n')

    db = TinyDB('/home/lucas/PycharmProjects/reagenttrade/trocas.data')
    for r in range(20):
        db.insert({
                'trade_id':r,
               'usuario_nome': random.choice(nomes).decode('utf8'),
               'produto':random.choice(produtos).decode('utf8'),
                'quantidade':str(random.randint(0,100)),
                'foto_produto':'x',
               'data_anuncio':time.strftime("%d/%m/%Y")})


if __name__ == '__main__':
    sys.exit(main())
