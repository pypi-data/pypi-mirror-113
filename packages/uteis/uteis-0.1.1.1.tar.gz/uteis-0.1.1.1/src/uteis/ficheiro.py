#! usr/bin/python3
# -*- coding: utf-8 -*-
# --------------------------------------------
#+ Autor:	Ran#
#+ Creado:	05/07/2021 17:36:35
#+ Editado:	13/07/2021 19:29:51
# --------------------------------------------

import os
import json

# --------------------------------------------

# carga os contidos dun ficheiro
def cargarFich(fich_nome, en_linhas=True, encoding='utf-8-sig'):
    """
    Dado un catex, ou lista con catexs, de entrada;
    devolve esta mesma estrutura pero cos catexs riscados.

    @entrada:
        fich_nome   -   Requerido   -   Catex/Lista
        └ Nome do ficheiro a cargar, con extensión.
        en_linhas   -   Opcional    -   Booleano
        └ True: carga nun array cada linha como catex.
        └ False: carga nun só catex con todo o ficheiro.
        encoding    -   Opcional    -   Catex
        └ Tipo de codificación a usar.

    @saída:
        Catex   -   Sempre
        └ O contido do ficheiro.
    """
    # se o ficheiro a cargar non existe sacar erro
    if not os.path.isfile(fich_nome):
        raise Exception('O ficheiro {} non existe'.format(nome))

    # faise neste bloque en lugar de directamente para poder pechar a conexión
    # de non pechala pódese corromper
    try:
        conn = open(fich_nome, 'r', encoding=encoding)
        if en_linhas:
            fich_contido = conn.readlines()
        else:
            fich_contido = conn.read()
    except:
        # saca o erro producido
        raise
    # se non ocorre ningunha excepción
    else:
        return fich_contido
    finally:
        if 'conn' in globals():
            conn.close()

# garda nun ficheiro os contidos proporcionados
# xFCR: pode ser o contido un array?
def gardarFich(fich_nome, contido, encoding='utf-8-sig'):
    """
    Dado un nome de ficheiro (con ou sen path/caminho) gardao en memoria.
    Se non se da camiño na propia carpeta de execución e senón non camiño dado.

    @entrada:
        fich_nome   -   Requerido   -   Catex
        └ Nome do ficheiro a gardar, con extensión. Con ou sen o camiño incluído.
        contido     -   Requerido   -   Lista de catexs
        └ Catex a gardar dentro do ficheiro.
        encoding    -   Opcional    -   Catex
        └ Tipo de codificación a usar.

    @saída:
        Booleano    -   Cando todo foi correcto.
        └ Verdadeiro:   Indica o correcto funcionamento.
    """
    try:
        os.makedirs('/'.join(fich_nome.split('/')[:-1]), exist_ok=True)

        conn = open(fich_nome, 'w')
        for ele in contido:
            conn.writelines(ele+'\n')
    except:
        # saca o erro producido
        raise
    else:
        return True
    finally:
        # se existe a variable
        if 'conn' in globals():
            conn.close()

# carga os contidos dun ficheiro
def cargarJson(fich_nome):
    """
    Dado o nome dun ficheiro json cargao en memoria

    @entrada:
        fich_nome   -   Requerido   -   Catex
        └ Nome do ficheiro (.json) a cargar.

    @saida:
        Diccionario -   Sempre
        └ Cos datos json contidos.
    """
    # se existe abrese conexión
    if os.path.isfile(fich_nome):
        try:
            conn = open(fich_nome)
        except:
            raise
        else:
            return json.loads(conn.read())
        finally:
            if 'conn' in globals():
                conn.close()
    # se non existe
    else:
        # crease
        conn = open(fich_nome, 'w')
        # soamente con {} no interior
        conn.write('{}')
        # pechase directamente
        conn.close()

        # faise recursión
        return cargarJson(fich_nome)

# garda nun ficheiro os contidos dun diccionario de python no formato json
def gardarJson(fich_nome, contido, indent=1, sort_keys=False, ensure_ascii=False):
    """
    Dado un nome de ficheiro e o seu contido gardao en memoria.

    @entrada:
        fich_nome       -   Requerido   -   Catex
        └ Nome do ficheiro a gardar, con extensión. Con ou sen o camiño incluído.
        contido         -   Requerido   -   Catex
        └ O que ten o ficheiro dentro.
        indent          -   Opcional    -   Int
        └ Grado de indentación a usar.
        sort_keys       -   Opcional    -   Boleano
        └ Indica se se ordean as chaves do diccionario ou non.
        ensure_ascii    -   Opcional    -   Boleano
        └ De estar a True, asegurase que o resultado sexan caracters
            ascii válidos e que se devolva un obxecto de tipo unicode.

    @saida:
        Booleano    -   Canto todo foi correcto.
        └ Verdadeiro:   Indica o correcto funcionamento.
    """

    # faise neste bloque en lugar de directamente para poder pechar a conexión
    # de non pechala pódese corromper
    try:
        os.makedirs('/'.join(fich_nome.split('/')[:-1]), exist_ok=True)

        conn = open(fich_nome, 'w')
        #conn = open(fich_nome.split('/')[-1], 'w')
        conn.write(json.dumps(contido, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii))
    except:
        # saca o erro producido
        raise
    else:
        return True
    finally:
        if 'conn' in globals():
            conn.close()

# --------------------------------------------

if __name__ == '__main__':
    print('*> Probas <*')
    print('> cargar')
    print('sen facer')

# --------------------------------------------
