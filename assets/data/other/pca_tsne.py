#!/usr/bin/env python

import os,sys
import argparse

import numpy as np
import sklearn
import sklearn.datasets,sklearn.decomposition,sklearn.manifold

import matplotlib
import matplotlib.pyplot as plt

class context(object):
	def __init__(self,obj=None):
		self.obj = obj
	def __enter__(self,*args,**kwargs):
		return self.obj
	def __exit__(self, *args,**kwargs):
		pass

def run(n=None,l=None,d=None,k=None,model='pca',data='mnist',path=None,**kwargs):
	'''
	Train and plot data
	Args:
		n (int): size of data
		l (int): number of classes
		d (int): dimension of data
		k (int): dimension of data, k<=d
		model (str): model, allowed string in {'pca','tnse'}
		data (str): data, allowed string in {'mnist','spiral'}
		path (str): path to save plot
		kwargs (dict): additional keyword arguments
	Returns:
		X (array): data of shape (n,k)
		y (array): labels of shape (n)
	'''

	# Path
	name = '%s.%s'%(model,data)
	path = os.path.join(path,'.'.join(['path',name,'pdf'])) if path is not None else '.'.join(['plot',name,'pdf'])

	# Setup
	X,y = setup(n,l,d,data=data,**kwargs)

	# Train
	X,y = train(X,y,k,model=model,**kwargs)

	# Plot
	plot(X,y,path=path,**kwargs)

	return

def setup(n=None,l=None,d=None,data='mnist',plot=None,**kwargs):
	'''
	Setup data
	Args:
		n (int): size of data
		l (int): number of classes
		d (int): dimension of data
		data (str): data, allowed string in {'mnist','spiral'}
		plot (bool): plot data
		kwargs (dict): additional keyword arguments
	Returns:
		X (array): data of shape (n,d)
		y (array): labels of shape (n)
	'''

	if data in ['mnist']:
		X,y = mnist(n,l,d,plot=plot,**kwargs)
	elif data in ['spiral']:
		X,y = spiral(n,l,d,plot=plot,**kwargs)

	X = X[:n,:] if n is not None else X; X = X[:,:d] if d is not None else X
	y = y[:n] if n is not None else y

	return X,y

def train(X,y=None,k=None,model='pca',**kwargs):
	'''
	Train and plot data
	Args:
		X (array): data of shape (n,d)
		y (array): labels of shape (n)
		k (int): dimension of data, k<=d
		model (str): model, allowed string in {'pca','tnse'}
		kwargs (dict): additional keyword arguments
	Returns:
		X (array): data of shape (n,k)
		y (array): labels of shape (n)
	'''

	# Model
	if model in ['pca']:
		X,y = pca(X,y,k,**kwargs)
	elif model in ['tsne']:
		X,y = tsne(X,y,k,**kwargs)

	return X,y


def pca(X,y=None,k=None,**kwargs):
	'''
	Model with PCA
	Args:
		X (array): data of shape (n,d)
		y (array): labels of shape (n)
		k (int): dimensions k<=d
		kwargs (dict): additional keyword arguments
	Returns:
		X (array): data of shape (n,k)
		y (array): labels of shape (n)
	'''

	model = sklearn.decomposition.PCA(k)

	X = model.fit_transform(X,y)

	return X,y


def tsne(X,y=None,k=None,**kwargs):
	'''
	Model with TSNE
	Args:
		X (array): data of shape (n,d)
		y (array): labels of shape (n)
		k (int): dimensions k<=d
		kwargs (dict): additional keyword arguments
	Returns:
		X (array): data of shape (n,k)
		y (array): labels of shape (n)
	'''

	model = sklearn.manifold.TSNE(k)

	X = model.fit_transform(X,y)

	return X,y

def mnist(n=None,l=None,d=None,plot=None,**kwargs):
	'''
	Data for mnist
	Args:
		n (int): size of data
		l (int): number of classes
		d (int): dimension of data
		plot (bool): plot data
		kwargs (dict): additional keyword arguments
	Returns:
		X (array): data of shape (k,n)
		y (array): labels of shape (n)
	'''

	path = 'data.npz'
	options = {'allow_pickle':True}

	if os.path.exists(path):
		data = np.load(path,**options)
	else:
		data = sklearn.datasets.fetch_openml('mnist_784')
		data = {'X':data.data.to_numpy(),'y':data.target.to_numpy()}
		np.savez(path,**data,**options)


	if plot:
		x = data['X'].reshape(-1,28,28)
		options = dict(cmap=plt.cm.gray_r,interpolation='nearest')
		plots = (3,3)
		p = np.prod(plots)
		path = 'plot.mnist.pdf'

		fig,ax = plt.subplots(*plots)
		fig,ax = fig,ax.flatten()
		for i in range(p):
			ax[i].imshow(x[i],**options)
			ax[i].set_xticks([])
			ax[i].set_yticks([])
			print(i)

		fig.set_size_inches(8,8)
		fig.subplots_adjust()
		fig.tight_layout()
		fig.savefig(fname=path,bbox_inches='tight');

	X,y = data['X'],data['y']

	return X,y

def spiral(n=None,l=None,d=None,plot=None,**kwargs):
	'''
	Data for spiral
	Args:
		n (int): size of data
		l (int): number of classes
		d (int): dimension of data
		plot (bool): plot data
		kwargs (dict): additional keyword arguments
	Returns:
		X (array): data of shape (k,n)
		y (array): labels of shape (n)
	'''

	n = 2**8 if n is None else n
	d = 3 if d is None else d
	l = 5 if ls is None else l

	delta = 0
	sigma = 0
	theta = 2

	X = np.zeros(n,d)
	y = np.zeros(n)

	for i in range(l):

		p = n//l + (n%l)%(i==(l-1))

		index = slice((i+0)*p,(i+1)*p)
		radius = np.linspace(1e-1,1,p)
		angle = np.array([
			np.linspace(
				i*(2*np.pi)*(1 if j < (d-2) else 2)/l,
				i*(2*np.pi)*(1 if j < (d-2) else 2)/l + theta,p)
			for j in range(d-1)
			]) + sigma*np.random.randn(d-1,p)

		for j in range(d):
			if j < (d-1):
				x = radius*np.prod([np.sin(theta[l]) for l in range(j)],axis=0)*np.cos(theta[j])
			else:
				x = radius*np.prod([np.sin(theta[l]) for l in range(j-1)],axis=0)*np.sin(theta[j])

			X[index,j] = x

		y[index] = l

	return X,y

def plot(X,y,path=None,**kwargs):
	'''
	Plot data
	Args:
		X (array): data of shape (n,d)
		y (array): labels of shape (n)
		path (str): path to save plot
		kwargs (dict): additional keyword arguments
	'''

	mplstyle = 'plot.mplstyle'

	with matplotlib.style.context(mplstyle) if os.path.exists(mplstyle) else context(mplstyle):

		n,d = X.shape
		labels = sorted(set(y))
		l = len(labels)

		fig,ax = plt.subplots()

		options = {
			'c':np.array([int(y[i]) for i in range(n)]),
			's':np.array([10 for i in range(n)]),
			'cmap':matplotlib.colors.ListedColormap([getattr(plt.cm,'viridis')(i/l) for i in range(l)])
		}

		if d == 1:
			x = [np.arange(n),X]
		else:
			x = X.T

		plot = ax.scatter(*x,**options);

		if d == 1:
			ax.set_yticks([]);
		elif d == 2:
			ax.set_xticks([]);
			ax.set_yticks([]);
		elif d == 3:
			ax.set_xticks([]);
			ax.set_yticks([]);
			ax.set_zticks([]);

		handles,labels = plot.legend_elements(prop='colors',num=l)[0],[f'${i}$' for i in labels]
		options = {'title':'$\\text{Labels}$','ncol':1 if l<5 else 2,'loc':'lower right'}
		ax.legend(handles,labels,**options);

		if path is not None:
			fig.set_size_inches(8,8)
			fig.subplots_adjust()
			fig.tight_layout()
			fig.savefig(fname=path,bbox_inches='tight');

	return


def argparser(*args,**kwargs):
	'''
	Parse command line arguments
	Args:
		args (tuple): additional positional arguments
		kwargs (dict): additional keyword arguments
	Returns:
		arguments (dict): parsed arguments
	'''

	parser = argparse.ArgumentParser()

	parser.add_argument("--n",type=int,default=None,help='size of data')
	parser.add_argument("--l",type=int,default=None,help='number of labels')
	parser.add_argument("--d",type=int,default=None,help='dimension of data')
	parser.add_argument("--k",type=int,default=2,help='dimension of data')
	parser.add_argument("--model",type=str,default='pca',help='model')
	parser.add_argument("--data",type=str,default='mnist',help='data')

	arguments = vars(parser.parse_args())

	return arguments


def main(*args,**kwargs):

	arguments = argparser(*args,**kwargs)

	run(**arguments)

	return


if __name__ == "__main__":

	main()
