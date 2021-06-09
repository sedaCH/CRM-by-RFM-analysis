###############################################################
# Customer Segmentation by RFM

##################################################################
#  Business Problem
##################################################################
# An e-commerce company segments its customers and determines marketing strategies according to these segments
# requests.

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

###############################################################
Importing Data and Preparing Data
###############################################################

df_ = pd.read_excel("Bootcamp/hafta3/ödevler/online_retail_II.xlsx",sheet_name="Year 2010-2011")
df=df_.copy()
df.head()


df.describe().T

df.isnull().sum()


df.dropna(inplace=True)


df["StockCode"].nunique()


df["StockCode"].value_counts()


df["StockCode"].value_counts() .sort_values(ascending=False).head(5)

df = df[~df["Invoice"].str.contains("C", na=False)]

df["TotalPrice"]=df["Price"]*df["Quantity"]
df.head()

###############################################################
RFM Analysis
###############################################################

# Recency: analysis date -last shopping date
# Frequeny: number of shopping
# Monetory:total amount of invoices


df["InvoiceDate"].max()
rfm_date=dt.datetime(2011, 12, 11) # analysis date
rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (rfm_date - InvoiceDate.max()).days,
                                                                        'Invoice': lambda Invoice: Invoice.nunique(),
                                                                        'TotalPrice': lambda TotalPrice: TotalPrice.sum()})


rfm.columns = ["Recency","Frequency","Monetary"]
rfm=rfm[rfm["Monetary"]>0]

###############################################################
RFM Scores
###############################################################

rfm["Recency_Score"] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["Frequency_Score"] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["Monetary_Score"] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RFM_SCORE olarak kaydediniz.
rfm["RFM_SCORE"] = (rfm["Recency_Score"] .astype(str) + rfm["Frequency_Score"].astype(str))

###############################################################
Segment Descriptions
###############################################################

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm.head()

###############################################################
Segment Analysis
###############################################################

rfm[["segment", "Recency", "Frequency", "Monetary"]].groupby("segment").agg(["mean", "count"])


new_df = pd.DataFrame()
new_df= rfm[rfm["segment"] == "loyal_customers"]
new_df.head()
