import numpy as np
import matplotlib.pyplot as plt, mpld3

def demoPlot():
	#demoPlot = plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
	fig = plt.figure()
	np.random.seed(0)
	x, y = np.random.normal(size=(2, 200))
	color, size = np.random.random((2, 200))
	plt.scatter(x, y, c=color, s=500 * size, alpha=0.3)
	plt.grid(color='lightgray', alpha=0.7)
	return(mpld3.fig_to_html(fig))

def demoPie():
	fig = plt.figure()
	sizes = [0.5,0.3,0.2]
	labels = ['tesing','testing','testing']

	patches, texts = plt.pie(sizes,shadow=True, startangle=90) #labels = labels, shadow=True, startangle=90)
	plt.legend(patches, labels, loc="best")
	plt.axis('equal')
	plt.tight_layout()
	return(mpld3.fig_to_html(fig))

def demoDualPie():
	sizes1 = [0.5,0.3,0.2]
	labels1 = ['tesing','testing','testing']

	sizes2 = [0.7,0.1,0.2]
	labels2 = ['testing','tesing','testing']

	fig = plt.figure()

	plt.subplot2grid((3,7),(0,0), colspan=3,rowspan=3)
	patches1, texts1 = plt.pie(sizes1,shadow=True, startangle=90) #labels = labels, shadow=True, startangle=90)
	plt.legend(patches1, labels1, loc="best")
	plt.axis('equal')
	plt.tight_layout()

	plt.subplot2grid((3,7),(0,4), colspan=3,rowspan=3)
	patches2, texts2 = plt.pie(sizes2,shadow=True, startangle=90) #labels = labels, shadow=True, startangle=90)
	plt.legend(patches2, labels2, loc="best")
	plt.axis('equal')
	plt.tight_layout()

	return(mpld3.fig_to_html(fig))