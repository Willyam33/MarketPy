import pandas as pd

df=pd.read_csv("/home/ubuntu/test_files/valid2.csv")
df['price_week']=df['price_week']*0.8
df.to_csv("/home/ubuntu/test_files/valid3.csv",index=False)