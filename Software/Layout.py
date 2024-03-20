import numpy as np
from matplotlib import pyplot
from scipy import stats 
import probscale
import math


fig, ax3 = pyplot.subplots(figsize=(9, 6), ncols=1, sharex=True)

cut = [5.8,4.7,3.3,2.1]
dist = [99.31818182,95.45454545,81.81818182,54.54545455]


ax3.scatter(cut, dist)

ax3.plot([1,10],[50,50], c='#FF0000')

x_list = np.linspace(1,10,1000)

mu = 0.69
sigma = 0.513

mu2 = 0.67
sigma2 = 0.55

cdf = [50 * (1 + math.erf((np.log(x)-mu)/(sigma*(2**.5)))) for x in x_list]
cdf2 = [50 * (1 + math.erf((np.log(x)-mu2)/(sigma2*(2**.5)))) for x in x_list]

ax3.plot(x_list,cdf,c='#090909',lw=1)
ax3.plot(x_list,cdf2,c='#090909',lw=1)

ax3.set_title('% less than D_p')

ax3.set_yscale('prob')
ax3.set_xscale('log')
ax3.set_xlim(left=1, right=10)
ax3.set_ylim(bottom=0.01, top=99.99)
fig.tight_layout()

ax3.set_xticks([i+1 for i in range(10)], [f'{i+1:.1f}' for i in range(10)])

pyplot.grid(True)
pyplot.show()