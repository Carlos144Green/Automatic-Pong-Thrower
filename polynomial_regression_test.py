import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy.stats import linregress
import numpy as np
import math

lin = LinearRegression()
File = './PositiveData.csv'
raw = pd.read_csv(File, delimiter="\t")
#print(raw)
x = raw.iloc[:,0]
y = raw.iloc[:,1]
# print(y)
n = len(x)

plt.plot(x,y,'o')

p1 = np.polyfit(x,y,1)
p2 = np.polyfit(x,y,2)
p3 = np.polyfit(x,y,3)
p4 = np.polyfit(x,y,4)
p5 = np.polyfit(x,y,5)
p6 = np.polyfit(x,y,6)

plt.plot(x,y,'o')
xp = np.linspace(0,150,1000)
# plt.plot(xp,np.polyval(p1,xp),'r-')
# plt.plot(xp,np.polyval(p2,xp),'b--')
plt.plot(xp,np.polyval(p3,xp),'m:')
# plt.plot(xp,np.polyval(p4,xp))
plt.plot(xp,np.polyval(p5,xp))
plt.plot(xp,np.polyval(p6,xp))


# yfit = p1[0] * x + p1[1]

polyDegree=[p1,p2,p3,p4,p5,p6]
BIC = []

for k, p in enumerate(polyDegree):
  Yfit = np.polyval(p,x)
  yresid= y - Yfit
  SSresid = np.sum(yresid**2)
  #print(SSresid)
  BIC.append(n*math.log(SSresid)+k*math.log(n))

slope,intercept,r_value,p_value,std_err = linregress(x,y)
plt.show()
print(BIC)

plt.plot((1,2,3,4,5,6),BIC,'o')
plt.show()

