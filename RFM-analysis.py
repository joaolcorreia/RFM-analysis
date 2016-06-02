# Copyright (c) 2016 Joao Correia. All rights reserved.
#
# This program is licensed to you under the Apache License Version 2.0,
# and you may not use this file except in compliance with the Apache License Version 2.0.
# You may obtain a copy of the Apache License Version 2.0 at http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the Apache License Version 2.0 is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Apache License Version 2.0 for the specific language governing permissions and limitations there under.
#
# Version:     0.1.0
# URL:         -
#
# Authors:     Joao Correia <joao.correia@gmail.com> https://joaocorreia.io
# Copyright:   Copyright (c) 2016 Joao Correia
# License:     Apache License Version 2.0
#
# If you have suggestions or improvements please contribute 
# on https://github.com/joaolcorreia/RFM-analysis
#
#!/usr/bin/python

import sys, getopt
import pandas as pd
from datetime import datetime

def main(argv):
   inputfile = ''
   outputfile = ''
   inputdate = ''

   try:
      opts, args = getopt.getopt(argv,"hi:o:d:")
   except getopt.GetoptError:
      print 'RFM-analysis.py -i <orders.csv> -o <rfm-table.csv> -d <yyyy-mm-dd>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'RFM-analysis.py -i <orders.csv> -o <rfm-table.csv> -d "yyyy-mm-dd"'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg   
      elif opt in ("-d", "--dinputdate"):
         inputdate = arg  

   rfm(inputfile,outputfile,inputdate)


def rfm(inputfile, outputfile, inputdate):
   print " "
   print "---------------------------------------------"
   print " Calculating RFM segmentation for " + inputdate
   print "---------------------------------------------"

   NOW = datetime.strptime(inputdate, "%Y-%m-%d")

   # Open orders file
   orders = pd.read_csv(inputfile, sep=',')
   orders['order_date'] = pd.to_datetime(orders['order_date'])
   
   rfmTable = orders.groupby('customer').agg({'order_date': lambda x: (NOW - x.max()).days, # Recency
                                              'order_id': lambda x: len(x),      # Frequency
                                              'grand_total': lambda x: x.sum()}) # Monetary Value

   rfmTable['order_date'] = rfmTable['order_date'].astype(int)
   rfmTable.rename(columns={'order_date': 'recency', 
                              'order_id': 'frequency', 
                              'grand_total': 'monetary_value'}, inplace=True)


   quantiles = rfmTable.quantile(q=[0.25,0.5,0.75])
   quantiles = quantiles.to_dict()

   rfmSegmentation = rfmTable

   rfmSegmentation['R_Quartile'] = rfmSegmentation['recency'].apply(RClass, args=('recency',quantiles,))
   rfmSegmentation['F_Quartile'] = rfmSegmentation['frequency'].apply(FMClass, args=('frequency',quantiles,))
   rfmSegmentation['M_Quartile'] = rfmSegmentation['monetary_value'].apply(FMClass, args=('monetary_value',quantiles,))

   rfmSegmentation['RFMClass'] = rfmSegmentation.R_Quartile.map(str) + rfmSegmentation.F_Quartile.map(str) + rfmSegmentation.M_Quartile.map(str)

   rfmSegmentation.to_csv(outputfile, sep=',')

   print " "
   print " DONE! Check %s" % (outputfile)
   print " "

# We create two classes for the RFM segmentation since, being high recency is bad, while high frequency and monetary value is good. 
# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def RClass(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4
    
# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def FMClass(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1



if __name__ == "__main__":
   main(sys.argv[1:])