#!/usr/bin/env python

# Gradient Descent - Tutorial

# Import python modules
import numpy as onp
import autograd.numpy as np
import autograd

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, PathPatch
from matplotlib.path import Path
from IPython import display


# Visualize 1-dimensional function f(x)

# Function
def func(x):
	return (x-4)*(x)*(x-0.8)*(x+2)*(x-2)*(x-4)

# Variables
n = 1000
bounds = [-2,2]
x = np.linspace(*bounds,n)
y = func(x)


# Plotting
fig,ax = plt.subplots()

# Plot values
ax.plot(x,y,'-',color='#07223E');

# Plot properties
ax.grid(True);
# ax.axis(False);
ax.set_xlabel('x');
ax.set_ylabel('f(x)');

# Save plot
path = None
if path is not None:
	fig.savefig(path)


# Utility functions

def norm(x,ord=2):
	'''
	Compute norm of vector |x|
	Args:
		x (array): Array to compute norm
		ord (int): Order of norm
	Returns:
		norm (array): Norm of array of order ord
	'''
	return np.linalg.norm(x,ord=ord)

def plot(x=None,func=None,pts=None,fig=None,ax=None,**kwargs):
	'''
	Plot function of data
	Args:
		x (array): n points of d-dimensional function data of shape (d,n)
		func (callable): Function to plot that takes d-dimensional data and returns scalar
		pts (array,list,tuple): Additional k, d-dimensional points of shape (k,d)
		fig (plt.fig): Plot figure object
		ax (plt.axes): Plot axes object
		kwargs (dict): Additional plot properties
	Returns:
		fig (plt.fig): Updated plot figure object
		ax (plt.ax): Updated plot axes object
	'''

	# Get figure and ax objects
	if fig is None:
		fig,ax = plt.subplots()
	if ax is None:
		ax = fig.gca()

	# Get shape of data (dimensions, number of points)
	if x is not None and x.ndim == 1:
		x = x.reshape(-1,1)
	d,n = x.shape

	# Get all combinations of datapoints with grid of shape (n,n,n,...) (d times)
	x = np.array([u.ravel() for u in np.meshgrid(*x)])

	# Compute function at each grid point
	if func is not None:
		y = np.array([func(u) for u in x.T])

	# Reshape data for contour plots
	x = x.reshape((d,n,n))
	y = y.reshape((n,n))

	plots = ax.contour(x[0],x[1],y,100)
	plt.colorbar(plots,ax=ax)

	# Plot additional data points on grid
	if pts is not None:
		ax.plot([p[0] for p in pts],[p[1] for p in pts],'-o',
			color=kwargs.get('color','k'),
			label=kwargs.get('label',None),
			lw=2)

	# Draw plots
	fig.canvas.draw()

	# Set plot properties
	ax.set_xlabel(xlabel='x')
	ax.set_ylabel(ylabel='y')
	ax.set_title(label=kwargs.get('title',None))
	if 'label' in kwargs:
		fig.legend()
	else:
		pass
	fig.set_size_inches(7,7)
	fig.subplots_adjust(hspace=1, wspace=1)


	# Display plots
	display.display(fig)
	display.clear_output(wait=True)

	return fig,ax


# Visualize curvature of 1-dimensional function f(x)

# Function
def func(x):
	return (x-4)*(x)*(x-0.8)*(x+2)*(x-2)*(x-4)

# Function gradient
def grad(x):
	gradient = autograd.grad(func)
	return np.array([gradient(u) for u in x])

# Plot arrows of curvature of function
def path(x,y,fig,ax):
	vertices = list(zip(x,y))
	n = len(vertices)
	shift = (y.max()/y.min())+20
	segment = n//30;
	directions = [1,-1]
	i = 0
	while i + segment < n:

		for direction in directions:
			_x = x[i:i+segment][::direction]
			_y = y[i:i+segment][::direction] + direction*shift

			ax.plot(_x,_y, 'k')

			posA, posB = zip(_x[-2:], _y[-2:])
			edge_width = 2.
			arrowstyle = "fancy,head_length={},head_width={},tail_width={}".format(2*edge_width, 3*edge_width, edge_width)
			arrow = FancyArrowPatch(posA=posA,posB=posB,arrowstyle=arrowstyle,color='k')
			ax.add_artist(arrow)

		i += 2*segment
	return


# Variables
n = 1000
bounds = [-2,2]
alpha = 3e-3
x = np.linspace(*bounds,n)
y = func(x)
g = grad(x)

# Points
x0 = np.array([-1.6,-0.9,0.9])
y0 = func(x0)

# Points after gradient update
x1 = x0 - alpha*grad(x0)
y1 = func(x1)

# Find where function is at an extremal value and the gradient ~ 0
eps = 2.7e-1
i = np.where(np.abs((g-0))<eps)[0]

# Plotting
fig,ax = plt.subplots()

# Plot values
ax.plot(x,y,'-',color='#07223E');

# Plot extremal values
ax.plot(x[i],y[i],'o',color='#EB008B');

# Plot points
# ax.plot(x0,y0,'o',color='#18BD9A')
# ax.plot(x1,y1,'o',color='#BDA718')

# Plot function curvature
path(x,y,fig,ax)

# Plot properties
ax.grid(True);
# ax.axis(False);
ax.set_xlabel('x');
ax.set_ylabel('f(x)');


# Save plot
path = None
if path is not None:
	fig.savefig(path)


# Functions and gradients

def params(n,d,bounds=[-2.5,2.5]):
	'''
	Get n points of d-dimensional data for functions
	Args:
		n (int): Number of points
		d (int): Number of dimensions
		bounds (list): Bounds of data
	Returns:
		x (array): Input data of shape (d,n)
	'''
	x = np.array([np.linspace(*bounds,n) for i in range(d)])
	return x


def func(x):
	'''
	Scalar function of d-dimensional input data
	Args:
		x (array): input data of shape (d,)
	Returns:
		y (array): function scalar value of shape (1,)
	'''
	return np.sin(x[0]) + np.cos(x[1])

def grad(x):
	'''
	Gradient of scalar function of d-dimensional input data with autograd
	Args:
		x (array): input data of shape (d,)
	Returns:
		g (array): gradient derivative values of func of shape (d,)
	'''
	return autograd.grad(func)(x)

def grad_finite(x,eps=1e-6):
	'''
	Gradient of scalar function of d-dimensional input data with finite-difference
	Args:
		x (array): input data of shape (d,)
		eps (float): Difference for finite difference method
	Returns:
		g (array): gradient derivative values of func of shape (d,)
	'''
	d = x.size
	i = np.eye(d)
	return np.array([(func(x + eps*i[j]) - func(x - eps*i[j]))/(2*eps)
					for j in range(d) ])

def grad_analytical(x):
	'''
	Gradient of scalar function of d-dimensional input data with analytical derivative
	Args:
		x (array): input data of shape (d,)
		eps (float): Difference for finite difference method
	Returns:
		g (array): gradient derivative values of func of shape (d,)
	'''
	return np.array([np.cos(x[0]), -np.sin(x[1])])


# Visualize curvature of 2-dimensional function f(x,y) and gradient

# Setup variables

n = 100 # number of points
d = 2 # number of dimensions
x = params(n,d) # n points of d-dimensional data of shape (d,n)

# Function, its gradient and the 2-norm of the gradient
# function of d-dimensional data -> Returns scalar
# gradient of d-dimensional data -> Returns d-dimensional vector for the derivative along each dimension
# norm of gradient of d-dimensional data -> Returns scalar of 2-norm of d-dimensional gradient
f = lambda x: func(x)
g = lambda x: grad(x)
g_diff = lambda x: grad_finite(x)
g_anl = lambda x: grad_analytical(x)

h = lambda x: norm(grad(x))
h_diff = lambda x: norm(grad_finite(x))
h_anl = lambda x: norm(grad_analytical(x))

h_delta = lambda x: norm(grad(x) - grad_finite(x))

# Plot function and gradient
n_plots = 2
fig,axes = plt.subplots(n_plots)
fig,axes[0] = plot(x,f,fig=fig,ax=axes[0],title='$f(x,y) = sin(x) + cos(y)$')
fig,axes[1] = plot(x,h,fig=fig,ax=axes[1],title='$g(x,y) = |\\nabla f(x)|$')
# fig,axes[2] = plot(x,h_delta,fig=fig,ax=axes[2],title='$g(x) = |\\nabla_{auto} f(x) - \\nabla_{finite} f(x)|$')



# Perform gradient descent

def update(i,x,func,grad,value_previous,gradient_previous,alpha,beta,lmbda):
	'''
	Gradient descent update of data
	Args:
		i (int): Iteration step
		x (array): Current data of shape (d,) at step i
		func (callable): Function to optimize
		grad (callable): Gradient of function to optimize
		value_previous (array): Function value at step i-1
		gradient_previous (array): Gradient value at step i-1
		alpha (float): Learning rate
		beta (float): Momentum rate
		lmbda (float): Randomness rate
	Returns:
		delta (array): Value to update data at step i, x -> x + delta
		value (array): Value of function at step i
		gradient (array): Value of gradient at step i
	'''

	shape = x.shape # (d,)
	delta,value,gradient = np.zeros(shape),0,np.zeros(shape)

	##### TODO: IMPLEMENT FUNCTION AND GRADIENT EVALUATION #####
	value = func(x)
	gradient = grad(x)
	delta = -alpha*gradient

	##### TODO: IMPLEMENT RANDOM DESCENT #####

	##### TODO: IMPLEMENT GRADIENT DESCENT #####

	##### TODO: IMPLEMENT GRADIENT DESCENT WITH MOMENTUM #####


	return delta,value,gradient


# Gradient Descent

# Number of dimensions
d = 2

# Function to optimize (x is d-dimensional)
func = lambda x: np.cos(x[0]) + np.sin(x[1])

# Gradient of function
grad = autograd.grad(f)

# Hyperparameters
x = np.array([-0.9,-0.2]) # initial value of data of shape (d,)
alpha = 1e-1 # learning rate
beta = 2e-1 # momentum rate
lmbda = 0e-1 # random rate
iterations = 10 # number of gradient descent steps

# Plotting (plot function contours and optimization points)
fig,ax = plt.subplots() # plot figure and axes objects
n = 100 # number of plot points
bounds = [-3,3] # bounds of plot
X = params(n,d,bounds) # plot points of shape (d,n)
fig,ax = plot(X,func,fig=fig,ax=ax) # plot function contours with plotting data

# Set initial values
value = func(x) # initial function value at x
gradient = grad(x) # initial gradient value at x

# Perform gradient descent
for i in range(iterations):
	delta,value,gradient = update(i,x,func,grad,value,gradient,alpha,beta,lmbda)
	x += delta
	fig,ax = plot(pts=[x-delta,x],fig=fig,ax=ax)


# Perform gradient descent with several combinations of hyperparameters

# Hyperparameters
xs = [4*np.random.rand(d)-2, # initial value of data of shape (d,)
		 4*np.random.rand(d)-2,
		 4*np.random.rand(d)-2]
alphas = [0,1e-1,1e-1] # learning rate
betas = [0,0,2e-1] # momentum rate
lmbdas = [1e-1,0,0] # random rate
iterationss = [10,10,10] # number of gradient descent steps
labels = ['Random','Gradient','Momentum']

# Plotting
kwargs = {}
fig,ax = plot(X,func) # plot function contours with plotting data

# Iterate over hyperparameter combinations

for x,alpha,beta,lmbda,iterations,label in zip(xs,alphas,betas,lmbdas,iterationss,labels):

	# Set initial values
	value = func(x)
	gradient = grad(x)
	kwargs.clear()
	kwargs.update({'color': np.random.rand(3)})

	# Perform gradient descent iterations
	for i in range(iterations):
	delta,value,gradient = update(i,x,func,grad,value,gradient,alpha,beta,lmbda)
	x += delta
	kwargs.update({'label':label if i==(0) else None})
	fig,ax = plot(X,pts=[x-delta,x],fig=fig,ax=ax,**kwargs)