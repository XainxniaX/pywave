# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 19:57:02 2021

@author: xainx
"""
import numpy as np
import scipy.integrate as spi
import time
#UPDATE METHODS
def STATIC(cont, dt):
    return cont.grid    

def LINEAR(cont, dt, quiet=True): 
    '''
    Not a numerical wave equation, rather => mesh of springs!
    p = p_lastframe + (v_lastframe + (attack * (p_left + p_right + p_top + p_bottom - 4*p_lastframe))) * slowdown
    
    https://vvvv.org/documentation/wave-simulation    
    '''
    return 0


def LAX_FRIEDRICHS(cont, tmin, tmax, tcount, xs, ys, quiet=True, initvalue= 0.0): 
    '''
    Lax-Friedrichs numerical evolution scheme for 2D wave equation. 
    
    https://indico.ictp.it/event/a0282/session/8/contribution/6/material/0/0.pdf
    PG: 47-49 
    '''    
    if cont.ctype == 'rect':         
        ts = np.linspace(tmin, tmax, tcount)
        dx, dy, dt = xs[1] - xs[0], ys[1] - ys[0], ts[1] - ts[0] 
        
        stable = (dt <= dx / np.sqrt(2*(cont.wavespeed[0]**2 + cont.wavespeed[1]**2))) and (dt <= dy / np.sqrt(2*(cont.wavespeed[0]**2 + cont.wavespeed[1]**2)))
        if not (stable or quiet): print('[LAX-FR] Unstable parameters detected!')            
        
        g1 = np.ones(cont.count)
        cont.stator.Append(g1*initvalue)
        
        #slow for-loop implementation until I do slicing...
        time0 = time.perf_counter()
        for it in range(1,len(ts)-1): 
            if not quiet:
                perc = np.round((it/(len(ts)-2))* 100,2)                
                curtime = time.perf_counter()
                if int(perc) % 5 == 0:
                    print(f'[LAX-FR] Process elapsed {np.round(curtime - time0,2)} sec, {perc}% complete.')
                
            #current 3d grid (including time) last frame and cur frame           
            grid = cont.stator.Get(irange=(-1,1))  
            
            #apply boundry conditions
            g1[:,0], g1[:,-1] = 0.0, 0.0
            g1[0,:], g1[-1,:] = 0.0, 0.0
            
            #s=du/dt, r=c*du/dx, l=c*du/dy
            s, r, l = np.gradient(grid)            
            r, l = cont.wavespeed[0]*r, cont.wavespeed[1]*l 
            
            #Lax-Friedrichs scheme
            g1[1:-1,1:-1] = 0.25*(s[0,2:,1:-1] + s[0,:-2,1:-1] + s[0,1:-1,2:] + s[0,1:-1,:-2]) \
                - (dt/2.0)*((r[0,2:,1:-1] - r[0,:-2,1:-1])/dx + (l[0,1:-1,2:] - l[0,1:-1,:-2])/dy)
            
            #trapezoid integration along t-axis => appended to state as position @ t+1                       
            res = cont.stator.Append((dt/2.0)*(g1[:,:] + grid[1,:,:]))
            
            if res: continue
            else: 
                print('[LAX-FR] Stator cannot append!')
                #could offload full stator to temp file, and clear stator to continue sim. not implemented yet                            
        time1 = time.perf_counter()
        print('[LAX-FR] Simulation Done! Took {np.round(time1 - time0,2)} sec')
    elif cont.ctype == 'circ':
        return None #this ain't implemented yet, and it wont be until regular containers work
        
        
class UpdateMethod():
        
    ftypes = {'None' : STATIC, 'Linear' : LINEAR, 'Lax-Fr' : LAX_FRIEDRICHS}
    
    def __init__(self, ftype):
        self.ftype = ftype 
        self.ufunc = UpdateMethod.ftypes[ftype]
        
    def Invoke(self, dt, quiet=True):
        return UpdateMethod.ftypes[self.ftype](dt, quiet)
