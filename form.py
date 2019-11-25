
try:
    from Tkinter import *
    import tkFileDialog
    from ConfigParser import SafeConfigParser
except:
    from tkinter import *
    import tkinter.filedialog as tkFileDialog
    from configparser import SafeConfigParser

import os


class Form:
    
    def __init__(self):
        self.master = Tk()
        self.master.resizable(True, False)
        self.master.title('cvConditioning')
        
        self.prf = prefs()
        
        self.okvar=False
        self.varFilename= StringVar()
        self.varFilePath= StringVar()
        self.varRecFilename= StringVar()
        self.varRecPath = StringVar()
        self.varConditions= StringVar()
        self.varCriterion= IntVar() 
        self.varLevel=DoubleVar() # normalizzato da 0 a 1
        self.varHistory=IntVar()
        
        self.varFilename.set(self.prf.get('filename'))
        self.varFilePath.set(self.prf.get('filepath'))
        self.varRecPath.set(self.prf.get('recpath'))
        self.varRecFilename.set(self.prf.get('recfile'))
        self.varConditions.set(self.prf.getConditionsStr())
        self.varCriterion.set(int(self.prf.get('criterion')))
        self.varLevel.set(float(self.prf.get('level')))
        self.varHistory.set(int(self.prf.get('history')))
        
        frame = Frame(self.master,width=768, height=576)
        frame.grid(row=0,column=0,rowspan=30,columnspan=30,sticky='NSEW')
        Grid.rowconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self.master, 0, weight=1)
        frame.grid(row=0, column=0, sticky='NSEW')
        #Grid.rowconfigure(frame, 7, weight=1)
        #Grid.columnconfigure(frame, 0, weight=1)
        for x in range(4):
            Grid.columnconfigure(frame, x, weight=1)
         
        for y in range(10):
            Grid.rowconfigure(frame, y, weight=1)
        
        self.txtFilename = Label(frame, text='Subject: ')
        self.edtFilename = Entry(frame, textvariable=self.varFilename)
        self.txtFilePath = Label(frame, text='File path: ')
        self.edtFilePath = Entry(frame, textvariable=self.varFilePath,justify=RIGHT)
        
        self.txtRec = Label(frame, text='REC file name: ')
        self.edtRec = Entry(frame, textvariable=self.varRecFilename)
        
        self.txtRecPath = Label(frame, text='REC file path: ')
        self.edtRecPath = Entry(frame, textvariable=self.varRecPath,justify=RIGHT)
        
        self.btnFilePath = Button(frame,
                               text="Browse",
                               command=self.askfilepath
                               )
        
        self.btnRecPath = Button(frame,
                               text="Browse",
                               command=self.askrecpath
                               )
        
        self.btnOk = Button(frame,
                               text="ok",
                               command=self.ok
                               )
        self.btnCancel = Button(frame,
                               text="Cancel",
                               command=self.cancel
                               )
        
        self.txtConditions = Label(frame, text='Conditions: ')
        self.edtConditions = Entry(frame, textvariable=self.varConditions,justify=CENTER)
        
        self.txtCriterion = Label(frame, text='Criterion: ')
        self.edtCriterion = Entry(frame, textvariable=self.varCriterion)
        
        self.txtLevel = Label(frame, text='Level: ')
        self.edtLevel = Entry(frame, textvariable=self.varLevel)
        
        self.txtHistory = Label(frame, text='Calibration: ')
        self.edtHistory = Entry(frame, textvariable=self.varHistory)
        
        
        self.txtFilename.grid(row=0,column=0,rowspan=1,columnspan=1,sticky='NSEW')
        self.edtFilename.grid(row=0,column=1,rowspan=1,columnspan=3,sticky='NSEW')
        self.txtFilePath.grid(row=1,column=0,rowspan=1,columnspan=1,sticky='NSEW')
        self.edtFilePath.grid(row=1,column=1,rowspan=1,columnspan=3,sticky='NSEW')
        self.btnFilePath.grid(row=1,column=4,rowspan=1,columnspan=1,sticky='NSEW')
        self.btnFilePath.grid(row=1,column=4,rowspan=1,columnspan=1,sticky='NSEW')
        self.txtRec.grid(row=2,column=0,rowspan=1,columnspan=1,sticky='NSEW')
        self.edtRec.grid(row=2,column=1,rowspan=1,columnspan=1,sticky='NSEW')
        self.txtRecPath.grid(row=3,column=0,rowspan=1,columnspan=1,sticky='NSEW')
        self.edtRecPath.grid(row=3,column=1,rowspan=1,columnspan=3,sticky='NSEW')
        self.btnRecPath.grid(row=3,column=4,rowspan=1,columnspan=1,sticky='NSEW')
        
        self.txtConditions.grid(row=4,column=0,rowspan=1,columnspan=1,sticky='NSEW')
        self.edtConditions.grid(row=4,column=1,rowspan=1,columnspan=3,sticky='NSEW')
        
        self.txtCriterion.grid(row=5,column=0,rowspan=1,columnspan=1,sticky='NSEW')
        self.edtCriterion.grid(row=5 ,column=1,rowspan=1,columnspan=1,sticky='NSEW')
        
        self.txtLevel.grid(row=6,column=0,rowspan=1,columnspan=1,sticky='NSEW')
        self.edtLevel.grid(row=6 ,column=1,rowspan=1,columnspan=1,sticky='NSEW')
        
        self.txtHistory.grid(row=7,column=0,rowspan=1,columnspan=1,sticky='NSEW')
        self.edtHistory.grid(row=7 ,column=1,rowspan=1,columnspan=1,sticky='NSEW')
        
        self.btnOk.grid(row=8 ,column=4,rowspan=1,columnspan=1,sticky='NSEW')
        self.btnCancel.grid(row=8 ,column=5,rowspan=1,columnspan=1,sticky='NSEW')
        
        
        self.master.mainloop()
    
    
    def browse(self):
        path=tkFileDialog.askdirectory(initialdir='.')
        return path
    
    def askfilepath(self):
        path= self.browse()
        if path:
            self.varFilePath.set(path)
    
    def askrecpath(self):
        path= self.browse()
        if path:
            self.varRecPath.set(path) 
        
    def ok(self):
        self.okvar=True
        self.master.destroy()
        
    def cancel(self):
        self.okvar=False
        self.master.destroy()
        
    def results(self):
        res={}
        if self.okvar:
            if self.varFilename.get():
                res['filename']=self.varFilename.get()
            else:
                res['filename']=''
            
            self.prf.set('filename',res['filename'])
                
            res['filepath']= self.varFilePath.get()
            self.prf.set('filepath',res['filepath'])
            
            if self.varRecFilename.get():
                res['recfile']=self.varRecFilename.get()
            else:
                res['recfile']=''
            self.prf.set('recfile',res['recfile'])
            
            res['recpath']=self.varRecPath.get()
            self.prf.set('recpath',res['recpath'])
            
            res['criterion'] = self.varCriterion.get()
            self.prf.set('criterion',str(res['criterion']))

            self.prf.setConditions(self.varConditions.get())
            res['conditions']=self.prf.getConditions()
            
            
            res['level']=str(self.varLevel.get())
            self.prf.set('level',str(res['level']))
            res['history']=str(self.varHistory.get())
            self.prf.set('history',str(res['history']))
            
            return res

class prefs:
    def __init__(self):
        self.filename = 'formPref.ini'
        self.config = SafeConfigParser()
        self.config.read(self.filename)
        if len(self.config.sections())==0:
            self.defaults()
            
    def defaults(self):
        self.config.add_section('general')
        self.config.set('general', 'filename', '')
        self.config.set('general', 'filepath', os.getcwd())
        self.config.set('general', 'recfile', '')
        self.config.set('general', 'recpath', os.getcwd())
        self.config.set('general', 'level', '0.5')
        self.config.set('general', 'criterion', '30')
        self.config.set('general', 'conditions', 'left,right')
        self.config.set('general', 'history', '1000')
        self.write()
        
    def set(self,what,varstr):
        self.config.set('general', what,varstr)
        self.write()
        
    def get(self,what):
        return self.config.get('general', what)
    
    def getConditionsStr(self):
        return self.config.get('general', 'conditions')
    
    def getConditions(self):
        return self.config.get('general', 'conditions').split(',')
    
    def setConditions(self,conditions):
        self.config.set('general', 'conditions',conditions)
        self.write()
    
    def write(self):
        with open(self.filename, 'w') as f:
            self.config.write(f)




if __name__=='__main__':
    
    form = Form()
    print(form.results())
    #prf = prefs()
    #print(prf.getConditions())
    
