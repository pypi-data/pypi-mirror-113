# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 13:06:18 2021

@author: Ana
"""

def primos(n):
	primos_list = []
	for i in range(2, n+1):
		n_primo = True
		for d in range(2, i):
			if i%d == 0:
				n_primo = False
		if n_primo is True:
			primos_list.append(i)
	print(f"Estos son los números primos entre 1 y {n}:", primos_list)
