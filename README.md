# Apriori-python 
Implementation of Apriori Algortihm[1] in python

Data (can be any file type, but type csv always gets expected output):
Each row of data will be considered as a transaction.  
Each element in a row will be considered as an item. 

To run the program at default settings:
python Apriori.py

  run with different min support (default 0.9):
  python Apriori.py --min_sup 0.7
  
  run with different file (default adult.data.csv[2]):
  python Apriori.py --FilePath ./YourFolder/YourData.csv
  
  run without details (only showing count of frequent itemset without showing contents of those frequent itemsets):
  python Apriori.py --noDetail
  
  * commends above can be combined together
  e.g. python Apriori.py --min_sup 0.7 --FilePath ./YourFolder/YourData.csv --noDetail


[1] Algorithm from: Data Mining. Concepts and Techn - Jiawei Han, Micheline Kamber, J/Page 253
[2] Data comes from: Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
