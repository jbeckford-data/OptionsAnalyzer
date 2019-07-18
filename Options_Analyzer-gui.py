# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 08:53:21 2019

@author: Sarco1
"""

import mibian
import tkinter as tk
from yahoo_fin import stock_info as si
from datetime import date as dt
from datetime import datetime
import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib import style
#style.use('ggplot')

prices_dict = {}

class Calculator(object):
    
    def __init__(self,master):
        xy=None
        
        self.total = []
        self.fields = ('Quantity','Expiration','Strike','Option','Price','Vol')
        
        self.frame1 = tk.Frame(master)
        
        self.lsym = tk.Label(self.frame1, text='Symbol: ')
        self.sym = tk.Entry(self.frame1)
        self.intl = tk.Label(self.frame1,text='Interest Rate: ')
        self.int = tk.Entry(self.frame1)
        self.intvl = tk.Label(self.frame1, text='Interval: ')
        self.intv = tk.Entry(self.frame1)
        self.lsym.grid(row=0,column=0)
        self.sym.grid(row=0,column=1)
        self.intl.grid(row=0,column=2,padx=20)
        self.int.grid(row=0,column=3)
        self.intvl.grid(row=0,column=4,padx=20)
        self.intv.grid(row=0,column=5)
        
        
        self.frame1.grid(row=0,column=0,sticky='W')
        
        self.frame2 = tk.Frame(master)
        self.figure = plt.Figure(figsize=(10,4), dpi=100)
        self.figure.subplots_adjust(left=.05,right=1.0,top=1.0,bottom=.15,hspace=0,wspace=0)
        self.ax = self.figure.add_subplot(111)
        x = []
        y = []
        self.expiry, = self.ax.plot(x,y,'r-',label="Expiry")
        self.today, =  self.ax.plot(x,y,'b-',label="Today")
        self.days, =   self.ax.plot(x,y,'g-',label="Interval")
        self.canvas = FigureCanvasTkAgg(self.figure,master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()
        self.canvas._tkcanvas.grid()
        self.frame2.grid(row=1)
        
        self.toolbarFrame = tk.Frame(master)
        self.toolbarFrame.grid(row=1,column=0,sticky='S')
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        
        self.frame3 = tk.Frame(master)
        
        self.makeform(self.frame3,self.fields)       
        self.leg1 = Entrys(self.frame3, row=1)
        self.leg2 = Entrys(self.frame3, row=2)
        self.leg3 = Entrys(self.frame3, row=3)
        self.leg4 = Entrys(self.frame3, row=4)
        self.leg5 = Entrys(self.frame3, row=5)
        self.leg6 = Entrys(self.frame3, row=6)
        self.leg7 = Entrys(self.frame3, row=7)
        self.leg8 = Entrys(self.frame3, row=8)
        
        
        self.frame3.grid(row=2,columnspan=2,sticky='W')
        
        self.frame4 = tk.Frame(master)
        
        self.quit = tk.Button(self.frame4, text='Quit',command=master.destroy)
        self.quit.grid(row=0,column=0,pady=2)
        self.pri = tk.Button(self.frame4, text='Calculate',
                            command = lambda: self.draw())
        self.pri.grid(row=1,column=0,pady=2)
        
        self.frame4.grid(row=0,column=6)
        
    def makeform(self,master,fields):
        for i,field in enumerate(fields):
            lab = tk.Label(master,text=field, anchor='w')
            lab.grid(row=0,column=i)
    
        
    def draw(self):
        total = pd.DataFrame(columns=self.fields)
        for leg in [self.leg1,self.leg2,self.leg3,self.leg4,self.leg5,self.leg6,self.leg7,self.leg8]:
            try:
                i = Calculate(self.sym.get(),self.int.get(),leg)
                leg.v['text'] = i.vol
                total = total.append(pd.DataFrame([[i.qty,i.expiry,i.strike,i.option,
                              i.price,i.vol]], columns = self.fields),ignore_index=True)
            except: pass
        price = prices_dict[self.sym.get()+str(dt.today())]
        df = XandY(total,self.sym.get(),price,self.int.get(),self.intv.get())
        x = df.x
        y_exp = df.y_exp
        y_today = df.y_today
        y_days = df.y_days
        self.expiry.set_data(x,y_exp)
        self.today.set_data(x,y_today)
        self.days.set_data(x,y_days)
        ax = self.canvas.figure.axes[0]
        ax.axvline(price,alpha=.5)
        ax.legend(loc='best')
        ax.set_xlim(x.min()*.95, x.max()*1.05)
        ax.set_ylim(min(y_exp.min(),y_today.min(),y_days.min())*1.05,
                    max(y_exp.max(),y_today.max(),y_days.max())*1.05)        
        self.canvas.draw()        
    
class Calculate(Calculator):

        def __init__(self,symbol,interest,leg):
            
            symbol = symbol
            interest = float(interest)

            self.qty = int(leg.q.get())
            self.expiry = datetime.strptime(leg.ex.get()+' 2359',
                                               '%m/%d/%y %H%M')
            self.strike = float(leg.s.get())
            self.option = leg.var.get()
            self.price = float(leg.p.get())
            sym_today = symbol+str(dt.today())
            self.dte = (self.expiry - datetime.today()).days
            if sym_today in prices_dict:
                uprice = prices_dict[sym_today]
            else:
                uprice = si.get_live_price(symbol)
                prices_dict[sym_today] = uprice
                
            if leg.var.get() == 'Call':
                v = mibian.BS([uprice,self.strike,interest,self.dte],
                                    callPrice=self.price).impliedVolatility
            if leg.var.get() == 'Put':
                v = mibian.BS([uprice,self.strike,interest,self.dte],
                                    putPrice=self.price).impliedVolatility
            self.vol = v
        

class Entrys:
    
    def __init__(self,master,row):
        
        r = row
        
        self.var= tk.StringVar(master)
        self.q = tk.Entry(master)
        self.q.grid(row=r, column=0,padx=5,pady=2)
        self.ex = tk.Entry(master)
        self.ex.grid(row=r, column=1,padx=5,pady=2)
        self.s = tk.Entry(master)
        self.s.grid(row=r, column=2,padx=5,pady=2)
        self.opt = tk.OptionMenu(master, self.var, 'Call', 'Put')
        self.opt.grid(row=r, column=3,padx=5,pady=2)
        self.p = tk.Entry(master)
        self.p.grid(row=r, column=4,padx=5,pady=2)
        self.v = tk.Label(master,text='')
        self.v.grid(row=r,column=5,pady=2)
                  
class XandY:
    
    def __init__(self,df,symbol,uprice,interest=1.0,interval = 0.0):
        
        self.df = df
        self.symbol = symbol
        self.uprice = uprice
        self.interest = float(interest)
        self.interval = float(interval)
        num_intervals = 250
        ll = min(min(self.df.Strike),uprice) * .9
        ul = max(max(self.df.Strike),uprice) * 1.1

        self.x = np.linspace(round(ll,2), round(ul,2), num_intervals)
        self.df['Y_exp'] = self.df.apply(self.y_exp, axis=1)
        self.df['Y_today'] = self.df.apply(self.y_today,
                                           args=(self.interest, ),axis=1)
        self.df['Y_days'] = self.df.apply(self.y_days,
                                           args=(self.interest, self.interval, ),axis=1)
        
        self.y_exp = np.sum(self.df.Y_exp,axis=0)
        self.y_today = np.sum(self.df.Y_today,axis=0)
        self.y_days = np.sum(self.df.Y_days,axis=0)
        
        
    def y_exp(self, row):
        x=self.x
        y=[]
        for a in x:
            call = max(0,a - row.Strike) - row.Price
            put =  max(0,row.Strike - a) - row.Price
            if row.Option == 'Call':
                y.append(call*row.Quantity*100)
            if row.Option == 'Put':
                y.append(put*row.Quantity*100)
        return np.array(y)
    
    def y_today(self,row,int_rate=1.0):
        x = self.x
        dte = (row.Expiration - pd.Timestamp('today')).days
        y=[]
        for a in x:
            if row.Option == 'Call':
                y.append((mibian.BS([float(a),row.Strike,int_rate,dte],\
                                   volatility=row.Vol).callPrice-row.Price)*row.Quantity*100)
            if row.Option == 'Put':
                y.append((mibian.BS([float(a),row.Strike,int_rate,dte],\
                                   volatility=row.Vol).putPrice-row.Price)*row.Quantity*100)
        return np.array(y)
    
    def y_days(self, row,int_rate=1.0,interval=0.0): 
        days = interval
        x = self.x
        y=[]
        dte = (row.Expiration - pd.Timestamp('today')).days - days
        if dte < 0:
            return []
        if dte == 0:
            dte = .1
    
        for a in x:
            if row.Option == 'Call':
                y.append((mibian.BS([float(a),row.Strike,int_rate,dte],volatility=row.Vol)
                .callPrice-row.Price)*row.Quantity*100)
            if row.Option == 'Put':
                y.append((mibian.BS([float(a),row.Strike,int_rate,dte],volatility=row.Vol)
                .putPrice-row.Price)*row.Quantity*100)
        return np.array(y)            
            
class Start(Calculator):
    
    def __init__(self,master):
        super().__init__(master)

if __name__ == '__main__':
    
    root = tk.Tk()
    a = Start(root)
    root.mainloop()