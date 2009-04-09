import numpy

__all__ = ['mse', 'nll','class_error']

class Error(object):
    def __repr__(self):
        return self.name

    def __call__(self, os, y):
        raise NotImplementedError

    def _(self, os, y, C):
        raise NotImplementedError

    def test(self):
        self.test_grad(verbose=False)

    def test_grad(self, eps = 1e-5, verbose=True):
        eps =  float(eps)

        yc = numpy.random.random((2,5))
        yt = numpy.random.random((2,5))

        C = self(yc, yt)
        
        y_f = self._(yc, yt, C)

        ye = yc.copy()
        y_e = numpy.empty(ye.shape)
        for i, v in numpy.ndenumerate(ye):
            ye[i] += eps
            y_e[i] = (self(ye, yt) - C) / eps
            ye[i] = v
            
        eval = y_f/y_e
        
        if verbose: print eval
        if eval.max() > 1.01 or eval.min() < 0.99:
            raise ValueError('Gradient is not within norms')

class Mse(Error):
    name = "mse"

    def __call__(self, os, y):
        return ((os-y)**2).mean()

    def _(self, os, y, C):
        return 2*(os-y)/os.size

mse = Mse()

class Nll(Error):
    name = "nll"

    def __call__(self, os, y):
        return (-numpy.log(os[y.astype(numpy.bool)])).mean()

    def _(self, os, y, C):
        res = numpy.zeros(os.shape)
        sel = y.astype(numpy.bool)
        res[sel] = -1/(os[sel]*os.size)
        return res

nll = Nll()

class Class_error(Error):
	name="class_error"
	
	def __call__(self,os,y):
		return numpy.abs((numpy.round(os)-y)).mean()
		
class_error = Class_error()
