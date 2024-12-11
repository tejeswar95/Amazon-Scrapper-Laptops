import pandas as pd
import re
import GetPerformance as gp
import getCPUnames as gcn

def GetSpecs(newDF,df):
    
    Specs = {'Performance':[],'Team':[],'Processor':[],'RAM':[],'Storage':[],'Price2Performance':[]}
    
    RamList = ['4GB','8GB','16GB','32GB','4 GB','8 GB','16 GB','32 GB','12GB','12 GB']
    StorageList = ['256GB','512GB','1TB','2TB','256GB','512 GB','1 TB','2 TB','512','256']
    
    
    for i in range(len(df)):
        temp = df.loc[i,'Name'].upper()
        for j in range(len(newDF)):
            if temp.find(newDF.loc[j,'CPU']) != -1:
                Specs['Performance'].append(newDF.loc[j,'Performance'])
                Specs['Team'].append(newDF.loc[j,'Team'])
                Specs['Processor'].append(newDF.loc[j,'CPU'])
                break
        rflag = True
        sflag = True
        temp = temp.upper().replace("/"," / ").replace("("," ( ")
        for r in RamList:
            if temp.find(r) != -1:
                t = r.replace(' ',"").replace("GB", '')
                Specs['RAM'].append(int(t))
                rflag = False
                break
        if rflag: 
            print(i,'RAM Missing')
            Specs['RAM'].append(0)
        for s in StorageList:
            if temp.find(s) != -1:
                t = s.replace(' ',"").replace("GB", '')
                if t .find('TB') != -1:
                    t=int(t.replace('TB',"")) * 1000
                Specs['Storage'].append(int(t))
                sflag = False
                break
        if sflag: 
            print(i,'Storage Missing')
            Specs['Storage'].append(0)
            
        Specs['Price2Performance'].append(df.loc[i,'Price']/Specs['Performance'][i])
    
    Specs_df = pd.DataFrame(Specs)
    return Specs_df

def SearchAndDropRows(df,stringList):
    toremove = []
    for i in df.index:
        for j in stringList:
            if df.loc[i,'Name'].find(j) != -1:
                toremove.append(i)
                break
    df = df.drop(toremove)
    df.index = range(len(df))
    return df

def GetCpuSet(df,ProcessorDF):
    cpuSet = set()
    for i in range(len(df)):
        name = df.loc[i,'Name'].upper()
        flag = True
        for j in range(len(ProcessorDF)):
            cpu = ProcessorDF.loc[j,'Processors']
            if re.search(r'\b'+cpu+r'\b',name):
                flag = False
                #print(name,cpu,i)
                cpuSet.add(cpu)
                break
        if flag: df = df.drop(i)
    df.index = range(len(df))
    return df,cpuSet

def GetCpuInfo(cpuSet,PerformanceDF):
    List=[]
    Team=[]
    for c in cpuSet:
        for i in range(len(PerformanceDF)):
            string = PerformanceDF.iloc[i,0]
            if re.search(r'\b'+c+r'\b',string):
                if string.find('AMD') != -1: 
                    Team.append('AMD')
                if string.find('Intel') != -1: 
                    Team.append('Intel')
                List.append(int(PerformanceDF.iloc[i,1]))
                break

    return pd.DataFrame({'CPU':list(cpuSet),'Performance':List,'Team':Team})


df=pd.read_csv('laptops.csv')
ProcessorDF = gcn.GetDF().sort_values(by='Processors', ascending=False)
ProcessorDF.index= range(len(ProcessorDF))
PerformanceDF = gp.GetDF()

df = SearchAndDropRows(df,["Refurbished","Renewed"])
df.index = range(len(df))

df,cpuSet = GetCpuSet(df, ProcessorDF)

newDF = GetCpuInfo(cpuSet, PerformanceDF)
print(newDF)

df1 = pd.concat([df,GetSpecs(newDF, df)],axis=1)
print(df1)

df1.to_csv('new_laptops.csv',index=False)
