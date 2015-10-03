import pandas as pd
import sys,os,glob

from myCPI.user.models import ComponentCPI

#script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data"
#files = os.listdir(script_dir)
#files_xlsx = [f for f in files if f.endswith("xlsx")]
#df = pd.DataFrame()
#for f in files_xlsx:
#    data = pd.read_excel(f, 'BLS Data Series')
#    df = df.append(data)
#    print df

#allFiles = glob.glob(script_dir + "/*.xlsx")
allFiles = glob.glob("data/*.xlsx")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_excel(file_,'BLS Data Series')
    list_.append(df)
frame = pd.concat(list_)
print frame

