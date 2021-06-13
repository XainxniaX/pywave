# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 23:48:00 2021

@author: xainx
"""
import container.py as cont
import source.py as src
import umeth.py as umeth
import stator.py as sta
import numpy as np
import matplotlib.pyplot as plt



xcount = 25
xmin, xmax = 0.0, 10.0
ycount = 25
ymin, ymax = 0.0, 10.0
tcount = 100
tmax = 5.0

wavespeed = np.array([0.5, 0.5])

xs = np.linspace(xmin, xmax, xcount)
ys = np.linspace(ymin, ymax, ycount)
dx, dy = xs[1] - xs[0], ys[1] - ys[0]

def INIT(um_ftype, sources):
    #initalize simulation
    ct = cont.Container(um_ftype, xcount, ycount, dx, dy, wavespeed, gridinit=0.0)    
    ct.Init(0.0, tmax, tcount, sources)
    return ct
    
def RUN(con, quiet=True):
    ufun = con.updateMethod.ufunc
    ufun()

#make sources here
sources = []
container = INIT('Lax-Fr', sources)
RUN(container, quiet=False)



        
        
    
    
    
    
    
    
    
    
   
    
   