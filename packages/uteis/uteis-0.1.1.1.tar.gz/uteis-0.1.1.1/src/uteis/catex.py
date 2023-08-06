#! /usr/bin/python3
# -*- coding: utf-8 -*-
# --------------------------------------------
#+ Autor:	Ran#
#+ Creado:	05/07/2021 17:08:25
#+ Editado:	05/07/2021 21:46:23
# --------------------------------------------

# risca o texto proporcionado
def riscar(catex):
    """
    Dado un texto introducido, devolveo riscado.
    Se se introduce unha lista, mira cada elemento e,
    de ser texto, devolveo riscado.

    @entrada:
        catex   -   Requirido  -    Catex
        └ Texto/lista a modificar

    @saida:
        Catex
    """

    # se mete un catex
    if type(catex) == str:
        return ''.join([u'\u0336{}'.format(ele) for ele in catex])

    # se mete unha lista
    elif type(catex) == list:
        # para cada elemento da lista chamamos á operación de riscado e metemos o novo valor no lugar do vello
        for index, ele in enumerate(catex):
            catex[index] = riscar(ele)
        return catex

    # se non é ningún devolver a entrada tal cal
    else:
        return catex

# --------------------------------------------

if __name__ == '__main__':
    print('*> Probas <*')
    print('> riscar')
    print('Riscando "texto": ', end='')
    print(riscar('texto'))
    print('Riscando lista ["texto","lista"]: ', end='')
    print(riscar(['texto', 'lista']))
    print('Riscando lista ["texto", ["lista", "listisima"]]: ', end='')
    print(riscar(['texto', ['lista', 'listisima']]))
    print('Riscando lista ["texto", ["lista", "listisima", ["si", 2]]]: ', end='')
    print(riscar(['texto', ['lista', 'listisima', ['si', 2]]]))
    
# --------------------------------------------
