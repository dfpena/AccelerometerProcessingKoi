
#!/usr/bin/env python
from decorator import decorator

import pandas as pd
import matplotlib.pyplot as plt


@decorator
def on_start(func,*args, **kwargs):
    if kwargs !={}:
        try:
            if kwargs['Start']:
                if 'Verbose' in kwargs['Settings']:
                    if kwargs['Settings']['Verbose']:
                        print(func)
                        pass
                response= func(*args,**kwargs)
                return response
            else:
                kwargs['Start'] = False
                print(func,"DID NOT START")
                return(kwargs)
        except Exception as e:
            print('NODE ERROR OCCURED TRYING TO START NODE FUNCTION:')
            print('===========================================')
            print(func,e)
            print('===========================================')
            print('LAST STATE SET TO:')
            print('===========================================')
            print('ekwargs')
            print('===========================================')
            print('LAST NODE FUNCTION SET TO:')
            print('===========================================')
            print('efunc')
            print('===========================================')
            global ekwargs
            global efunc
            ekwargs = kwargs
            efunc = func
            print('HALTING')
            raise
    else:
        print('Empty kwargs')
        return ()



def start():
    return {'Start':True,'Settings':{'Verbose':True},'Status':{}}

 
@on_start
def excel2Pandas1(*args,**kwargs):
    kwargs['Data']=pd.read_excel('data/data.xlsx')
    return kwargs
 
 
@on_start
def pandasScatter2(*args,**kwargs):
    axl = kwargs['Data'].plot.scatter(x='time',y='gforce')
    #plt.show()
    return kwargs
 
@on_start
def pandasThreshold3(*args,**kwargs):
    df = kwargs['Data']
    kwargs['Data']= df.loc[df['gforce']>2]
    return kwargs
 
@on_start
def pandasScatter4(*args,**kwargs):
    axl = kwargs['Data'].plot.scatter(x='time',y='gforce')
    plt.show()
    return kwargs
 
@on_start
def pandaExcelDump(*args,**kwargs):
    kwargs['Data'].to_excel(''+'test.xls')
    return kwargs
 


class StremeNode:
    def __init__(self):
        pass

    def run(self,*args,**kwargs):
        self.kwargs=pandaExcelDump(**pandasScatter4(**pandasThreshold3(**pandasScatter2(**excel2Pandas1(**kwargs)))))
        return (self.kwargs)

class liveprocess:
    def __init__(self):
        self.status="pending"
    def run(self,expname):
        self.response=pandaExcelDump(**pandasScatter4(**pandasThreshold3(**pandasScatter2(**excel2Pandas1(**start())))))
        self.status="completed"
        return(self.status)

if __name__ == '__main__':
    process = liveprocess()
    process.run('Local')
    