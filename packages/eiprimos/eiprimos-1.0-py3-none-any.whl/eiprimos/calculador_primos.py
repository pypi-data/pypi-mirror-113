#!/usr/bin/env python3


def calculador_primos(num):

    primo = True

    for i in range(2,num):
        
        if num % i == 0:
            primo = False
            break

    return primo


