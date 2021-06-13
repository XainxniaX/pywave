# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 20:04:55 2021

@author: xainx
"""
import numpy as np


class Stator():
    
    """holds state information"""#I SUCK AT PYTHON, THESE ARE ALL STATIC MEMBERS !!!!
    """
    tmin = None
    tmax = None
    
    gt = None    
    gx = None
    gy = None
    
    grid = None
    
    sources = None #list of sources
    
    _indx = None
    _opcount = 0 #number of operations (append/insert/etc...)
    """
    
    def __init__(self, gt, gx, gy, tmin, tmax, initval=0.0):
        self.gx = gx
        self.gy = gy
        self.gt = gt
        self.tmin = tmin
        self.tmax = tmax
        self._indx = 0
        self._opcount = 0
        
        self.sources = []
        self.grid = initval * np.ones((gt, gx, gy))
        
    def Current(self):
        return self.grid[self._indx,:,:]
    
    def Last(self):
        if self._indx == 0: raise Exception('Stator index out of range! cannot get last from 0th index!')
        return self.grid[self._indx-1,:,:]
    
    def Get(self, irange=(0,1)):
        if (self._indx + irange[0] < 0 or self._indx + irange[0] >= self.gt or self._indx + irange[1] < 0 or self._indx + irange[1] >= self.gt):
            raise Exception('Stator index out of range! Get irange params out of range!')        
        return self.grid[self._indx+irange[0]:self._indx+irange[1],:,:]
    
    def Set(self, index, state):
        if index < 0 or index >= self.gt: raise Exception('Stator index out of range!')
        self.grid[index,:,:] = state
        self._opcount += 1
        
            
    
    def Append(self, state):
        if self._indx >= self.gt: #full! 
            return False
        self.grid[self._indx,:,:] = state
        self._indx += 1
        self._opcount += 1
        return True
    
    #not sure what it is used for but probably useful somewhere
    def Insert(self, state, index, overwrite=False):
        if index >= self.gt or index < 0:
            return False
        if overwrite:
            self.grid[index,:,:] = state
            self._opcount += 1
            return True
        else:
            if index+1 == self.gt:
                self._grid[index,:,:] = state
                return True
            #changes length of array... dont want that
            #np.insert(self.grid, index, state, axis=0)
            #roll elements right, and discard last element
            self._grid[index+1:,:,:] = self._grid[index:-1,:,:]
            self._grid[index,:,:] = state
            self._opcount += 1
            return True
    
    def AddSource(self, source):
        self.sources.append(source)
        self._opcount += 1
        
    def Clear(self, gridval=0.0):
        self.grid[:,:,:] = gridval        
        self._indx = 0
        self._opcount += 1
        self.sources.clear()
        
    def ClearState(self, gridval=0.0):
        self.grid[:,:,:] = gridval
        self._indx = 0
        self._opcount += 1
        
    def ClearSources(self):
        self.sources.clear()
        
        
        
    