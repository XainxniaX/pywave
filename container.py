# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 15:14:16 2021

@author: xainx
"""
import numpy as np
import stator.py as sta
import umeth.py as umeth

class Container():
    #I SUCK AT PYTHON !!!! THESE ARE ALL STATIC MEMBERS !!!
    '''General wave container'''
    '''
    ctype = 'rect'
    
    count = (50, 50) #2-tuple
    grid = None
    world = None #2-tuple of world positions cooresponding to grid
    wavespeed = (0.5, 0.5)
            
    
    updateMethod = None
    stator = None
    '''
    
    def __init__(self, um_ftype, countAxis0, countAxis1, dx, dy, wavespeed, offset=(0.0, 0.0), gridinit = 0.0):
        self.ctype = 'rect'
        self.updateMethod = umeth.UpdateMethod(um_ftype)
        self.wavespeed = wavespeed
        self.count = (countAxis0, countAxis1)
        self.grid = self._makeGrid(initval=gridinit)
        self.world = self._makeWorld(dx, dy, offset[0], offset[1])
        self.stator = None
        
    def Init(self, tmin, tmax, tcount, sources):
        self.stator = sta.Stator(tcount, self.count[0], self.count[1], tmin, tmax)
        self.stator.AddSource(sources)
        
        self.stator.Insert(self.grid, 0, overwrite=True)
                
    
    def _makeGrid(self, initval = 0.0):
        return initval * np.ones(self.count)
    
    def _makeWorld(self, dx, dy, ox, oy):
        return np.meshgrid(np.linspace(ox, dx, self.count[0]), np.linspace(oy, dy, self.count[1]))        

class CircularContainer(Container):
    #STATIC MEMBERS !!! ahhhh
    '''circular container'''
    '''
    radius = 1.0
    '''
    
    def __init__(self, updateMethod, radius, rcount, thcount, wavespeed, gridinit = 0.0):        
        self.ctype = 'circ'
        self.updateMethod = updateMethod
        self.radius = radius
        self.wavespeed = wavespeed        
        self.count = (rcount, thcount)
        self.grid = self._makeGrid(initval=gridinit)
        self.world = self._makeWorld()
        self.stator = None
        
    def Init(self, tmin, tmax, tcount, sources):
        self.stator = sta.Stator(tcount, self.count[0], self.count[1], tmin, tmax)
        self.stator.AddSource(sources)
        
        self.stator.Insert(self.grid, 0, overwrite=True)
 
    def Update(self, dt):
        self.updateMethod(self, dt)
        
     
    
    def _makeGrid(self, initval = 0.0):
        return initval * np.ones(self.count)
    
    def _makeWorld(self):
        dr = self.radius / self.count[0]
        dth = 2*np.pi / self.count[1]
        return np.meshgrid(np.linspace(0.0, dr, self.count[0], np.linspace(0.0, dth, self.count[1])))        
    
    @staticmethod
    def cart(r, theta):
        return r*np.cos(theta), r*np.sin(theta)
    
    @staticmethod
    def polar(x, y):
        return np.sqrt(x**2 + y**2), np.atan2(x, y)
    
    

