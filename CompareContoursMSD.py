#### Poorly written code by Sam Johnston
#### 09-23-15

#### Computes the mean sum of distances (MSD) for a trace by averaging
#### the distance between the y-value of two points in two different 
#### traces with the same x-coordinate.  This does not include a difference 
#### measure for x-coordinate points that have no cooresponding points
#### in the other trace.  The number of unmatched points will be reported
#### at the end with MSD.

#### Requires .json filetype traces.
#### By default safes the generated comparison file to the Desktop

from __future__ import division
from collections import defaultdict as dd
import os
import sys
import json


class CompareContours:

	def __init__(self):
		# obtain file paths for the json trace files to be compared
		if len(sys.argv) > 1:
			self.path1 = sys.argv[1]
			self.path2 = sys.argv[2]
		else:
			self.path1 = raw_input("Enter the path for the first json file: ")
			self.path2 = raw_input("Enter the path for the second json file: ")
		userpath = os.path.expanduser("~")
		try:
			self.writepath = sys.argv[3]
		except:
			self.writepath = os.path.join(userpath,"Desktop/")
		self.main()

	def compute_msd(self):
		# data storage structures
		self.missingtraces1 = set([])
		self.missingtraces2 = set([])
		# msd dd(list) value contains:
		# [0] msd value for each trace comparison, 
		# [1] & [2] signed msd value tells if tracer1 is generally above or below tracer2 (&viceversa)
		# [3] & [4] # of unmatched points from trace1,trace2, and 
		self.msd = dd(lambda: dd(list))

		self.tracer1 = self.traces1['tracer-id']
		self.tracer2 = self.traces2['tracer-id']
		self.total_msd = 0
		self.total_signedmsd1 = 0
		self.total_signedmsd2 = 0
		self.total_untraced1 = 0
		self.total_untraced2 = 0
		for tracefile in self.traces1['trace-data']:
			# determines if trace exists in the second json file, and extracts list of trace points
			try:
				tracedata2 = self.traces2['trace-data'][tracefile]
			except KeyError:
				self.missingtraces1.add(tracefile)
				continue
			tracedata1 = self.traces1['trace-data'][tracefile]
			# find the min and max for each trace, and the min and max of the comparable x-coordinates
			minx1, maxx1 = tracedata1[0]['x'], tracedata1[-1]['x']
			minx2, maxx2 = tracedata2[0]['x'], tracedata2[-1]['x']
			trace_start = max(minx1,minx2)
			trace_end = min(maxx1,maxx2)
			trace_range = (trace_end+1)-trace_start
			# find _index_ of min and max of the comparable points in each list
			start1 = trace_start-minx1
			# end1 = start1+trace_range
			start2 = trace_start-minx2
			# end2 = start2+trace_range
			# compute msd
			sumsd = 0
			# signed to help tell if a tracer is generally tracing below or above another
			signedsd1 = 0
			signedsd2 = 0
			for i in range(trace_range):
				sumsd += abs(tracedata1[start1+i]['y']-tracedata2[start2+i]['y'])
				signedsd1 += tracedata1[start1+i]['y']-tracedata2[start2+i]['y']
				signedsd2 += tracedata2[start2+i]['y']-tracedata1[start1+i]['y']
			if i == 0:
				print tracefile, "contains no data points."
			self.total_msd += sumsd / i
			self.total_signedmsd1 += signedsd1 / i
			self.total_signedmsd2 += signedsd2 / i
			self.msd[tracefile][0] = sumsd / i
			self.msd[tracefile][1] = signedsd1 / i
			self.msd[tracefile][2] = signedsd2 / i
			# find the number of points not traced by each user compared with the other
			self.msd[tracefile][3] = minx1-minx2 if minx1-minx2 > 0 else 0
			self.msd[tracefile][3] += maxx1-maxx2 if maxx1-maxx2 > 0 else 0
			self.total_untraced1 += self.msd[tracefile][3]
			self.msd[tracefile][4] = minx2-minx1 if minx2-minx1 > 0 else 0
			self.msd[tracefile][4] += maxx2-maxx1 if maxx2-maxx1 > 0 else 0
			self.total_untraced2 += self.msd[tracefile][4]
			# print self.msd[tracefile]
			# print self.tracer1, self.tracer2, '|', tracefile, '|', minx1, maxx1, '|', minx2, maxx2
		
		for tracefile in self.traces2['trace-data']:
			if tracefile not in self.traces1['trace-data']:
				self.missingtraces2.add(tracefile)

		self.numoftraces = (len(self.traces1['trace-data'])-len(self.missingtraces1))
		self.total_msd = self.total_msd / self.numoftraces
		self.total_signedmsd1 = self.total_signedmsd1 / self.numoftraces
		self.total_signedmsd2 = self.total_signedmsd2 / self.numoftraces
		self.total_untraced1 = self.total_untraced1 / self.numoftraces
		self.total_untraced2 = self.total_untraced2 / self.numoftraces

		if len(self.missingtraces1) == 0:
			self.missingtraces1.add(None)
		if len(self.missingtraces2) == 0:
			self.missingtraces2.add(None)

	def writelog(self):
		filepath = os.path.join(self.writepath,self.traces1['tracer-id']+'-'+self.traces2['tracer-id']+'_'+self.traces1['subject-id']+'.traces.msd.txt')

		logfile = open(filepath,'w')
		logfile.write("Comparison of:\t{0}\tand\t{1}\n".format(self.tracer1,self.tracer2))
		logfile.write("For subject:\t{0}\n".format(self.traces1['subject-id']))
		logfile.write("For project:\t{0}\n".format(self.traces1['project-id']))
		logfile.write("Total number of traces utilized:\t{0}\n".format(str(self.numoftraces)))
		logfile.write("Total Mean Standard Distance (in pixels):\t{0}\n".format(str(self.total_msd)))
		logfile.write("Signed MSD for Tracer 1; Tracer 1 above/below Tracer 2 on average by:\t{0}\n".format(str(self.total_signedmsd1)))
		logfile.write("Signed MSD for Tracer 2; Tracer 2 above/below Tracer 1 on average by:\t{0}\n".format(str(self.total_signedmsd2)))
		logfile.write("The ratio of untraced points for Tracer 1 and Tracer 2 is:\t{0} (value of 1 means same length of trace)\n".format(str(self.total_untraced1 / self.total_untraced2)))
		logfile.write("The traces that were traced by Tracer 1 but not Tracer 2 are:\n")
		for missingtrace in self.missingtraces1:
			logfile.write("\t-{0}\n".format(missingtrace))
		logfile.write("The traces that were traced by Tracer 2 bot not Tracer 1 are:\n")
		for missingtrace in self.missingtraces2:
			logfile.write("\t-{0}\n".format(missingtrace))
		logfile.write("The MSD, Signed MSD, and the number of unmatched datapoints (by speaker)\n is given below, by trace file:\n")
		self.checkcount = 0
		for tracefile in sorted(self.msd.items()):
			# print tracefile[1][0]
			tracefileName = tracefile[0]
			meansd = tracefile[1][0]
			signedsd1 = tracefile[1][2]
			untraced1 = tracefile[1][3]
			untraced2 = tracefile[1][4]
			# print tracefileName, meansd,signedsd1,untraced1,untraced2
			if (meansd > 3) or (untraced1+untraced2 > 40):
				tobechecked = "Yes"
				self.checkcount += 1
			else:
				tobechecked = "No"
			logfile.write("\t{0}\n\t\tDoes this need to be checked?:\t{1}\n\t\tMSD:\t{2}\n\t\tTracer 1 signed MSD:\t{3}\n\
		Tracer 2 signed MSD:\t{4}\n\t\tPoints traced only by Tracer 1:\t{5}\n\
		Points traced only by Tracer 2:\t{6}\n".format\
		(tracefileName,tobechecked,str(meansd),str(signedsd1),str(signedsd1*-1),str(untraced1),str(untraced2)))
		logfile.write("Total number of items to be checked:\t{0}".format(self.checkcount))

	def printsummary(self):
		print("Comparison of:\t{0}\tand\t{1}\n".format(self.tracer1,self.tracer2))
		print("For subject:\t{0}\n".format(self.traces1['subject-id']))
		print("For project:\t{0}\n".format(self.traces1['project-id']))
		print("Total number of traces utilized:\t{0}\n".format(str(self.numoftraces)))
		print("Total Mean Standard Distance (in pixels):\t{0}\n".format(str(self.total_msd)))
		print("Signed MSD for Tracer 1; Tracer 1 above/below Tracer 2 on average by:\t{0}\n".format(str(self.total_signedmsd1)))
		print("Signed MSD for Tracer 2; Tracer 2 above/below Tracer 1 on average by:\t{0}\n".format(str(self.total_signedmsd2)))
		print("The ratio of untraced points for Tracer 1 and Tracer 2 is:\t{0} (value of 1 means same length of trace)\n".format(str(self.total_untraced1 / self.total_untraced2)))
		print("Total number of frames to investigate:\t{0}".format(self.checkcount))

	def main(self):
		# python json data structures resemble multi-level embedded dictionaries, 
		# and can be accessed in the same way
		print self.path1, self.path2
		with open(self.path1, 'r') as datafile:
			self.traces1 = json.load(datafile)
		with open(self.path2, 'r') as datafile:
			self.traces2 = json.load(datafile)

		self.compute_msd()

		i = self.writelog()

		self.printsummary()





if __name__ == "__main__":
	CompareContours()

