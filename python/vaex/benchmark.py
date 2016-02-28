import vaex as vx
import sys
import timeit
import numpy as np
import argparse

subspace, dataset, limits = None, None, None

def main(argv):
	global subspace, dataset, limits
	parser = argparse.ArgumentParser(argv[0])
	parser.add_argument("-N", help="run each batch N times (default: %(default)s)", type=int, default=5)
	parser.add_argument("-f", "--fraction", help="fraction of dataset to use (default: %(default)s)", default=1., type=float, nargs="*")
	parser.add_argument("filename", help="filename of dataset to use")
	parser.add_argument("expressions", help="list of expressions to export (or all when empty)", nargs="*")

	args = parser.parse_args(argv[1:])


	progressbar = False
	fn = args.filename
	#print(("opening", fn))
	dataset = vx.open(fn)
	dataset.set_active_fraction(args.fraction)
	#dataset = vx.open_many(fn)

	expressions = args.expressions
	#print "subspace", expressions
	subspace = dataset(*expressions)
	byte_size = len(dataset) * len(expressions) * 8
	#sums = subspace.sum()

	limits = subspace.minmax()

	N = args.N
	print "benchmarking minmax"
	expr = "subspace.minmax()"
	times = timeit.repeat(expr, setup="from vaex.benchmark import subspace, dataset, np", repeat=5, number=N)
	print "minimum time", min(times)/N
	bandwidth = [byte_size/1024.**3/(time/N) for time in times]
	print "%f GiB/s" % max(bandwidth)

	speed = [len(dataset)/(time/N)/1e9 for time in times]
	print "%f billion rows/s " % max(speed)

	print
	print "benchmarking histogram"
	expr = "subspace.histogram(limits, 256)"
	times = timeit.repeat(expr, setup="from vaex.benchmark import subspace, dataset, np, limits", repeat=5, number=N)
	print "minimum time", min(times)/N
	bandwidth = [byte_size/1024.**3/(time/N) for time in times]
	print "%f GiB/s" % max(bandwidth)

	speed = [len(dataset)/(time/N)/1e9 for time in times]
	print "%f billion rows/s " % max(speed)
	print

	#expr = "np.nansum(dataset.columns['x'])"
	print "benchmarking sum"
	expr = "subspace.sum()"
	times = timeit.repeat(expr, setup="from vaex.benchmark import subspace, dataset, np", repeat=5, number=N)
	print "minimum time", min(times)/N
	bandwidth = [byte_size/1024.**3/(time/N) for time in times]
	print "%f GiB/s" % max(bandwidth)
