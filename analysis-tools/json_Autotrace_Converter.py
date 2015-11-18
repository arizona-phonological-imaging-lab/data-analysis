#### Author Sam Johnston
#### 9-22-15
#### Converter from an n-point representation of a trace with all pixels to
#### a version of the trace containing 32 data points that only fall on pre-
#### established fan grid lines.  Weight calculation code and parts of this 
#### code were writen by Dr. Clayton Morrison.

import numpy as np
import json, os
from pprint import pprint
from collections import defaultdict as dd


# pre-established 'w' weight parameters, each describing a different line or
# fan-blade in the grid.  Essentially the [1] intercept and the [2] slope
params = {
	1:[ 402.13333333,-0.93333333],\
	2:[ 440.00436681,-1.03056769],\
	3:[ 484.71428571,-1.14285714],\
	4:[ 537.94029851,-1.28358209],\
	5:[ 595.98924731,-1.43010753],\
	6:[ 668.3964497,-1.62130178],\
	7:[ 748.48051948,-1.82467532],\
	8:[ 845.02158273,-2.0647482],\
	9:[ 973.40983607,-2.40163934],\
	10:[ 1139.49056604,-2.83018868],\
	11:[ 1358.61111111,-3.38888889],\
	12:[ 1664.58108108,-4.17567568],\
	13:[ 2197.91071429,-5.55357143],\
	14:[ 3059.0,-7.75],\
	15:[ 5560.5,-14.22727273],\
	16:[ 24371.80000004,-62.6],\
	17:[-11042.72727273,28.45454545],\
	18:[-4296.14285714,11.14285714],\
	19:[-2700.95454545,7.04545455],\
	20:[-1961.06666667,5.13333333],\
	21:[-1483.1025641,3.91025641],\
	22:[-1190.53684211,3.16842105],\
	23:[-1013.89189189,2.7027027],\
	24:[-858.67716535,2.30708661],\
	25:[-736.16666667,1.99305556],\
	26:[-645.0625,1.75625],\
	27:[-571.07428571,1.56571429],\
	28:[-502.63157895,1.38947368],\
	29:[-442.95145631,1.23786408],\
	30:[-397.4,1.11818182],\
	31:[-351.0,1.],\
	32:[-311.21544715,0.89837398],\
}

def translate_Y_Coord(coords):
	#the old trace files have the y-axis flipped; this flips the y-axis around a midpoint of 390
	x,y = coords[0]
	if y != -1:
		y = 390 + (390 - y)
	return [x,y]

def write_file(new_Coordinates,json_Path,tracer):
	write_Dir_Path = json_Path[:json_Path.rfind('/')+1]

	for trace in new_Coordinates:
		fName = trace+'.'+tracer+'.traced.txt'

		fPath = os.path.join(write_Dir_Path,fName)

		f = open(fPath,'w')
		for w in new_Coordinates[trace]:
			coords = new_Coordinates[trace][w]
			coords = translate_Y_Coord(coords)
			f.write(str(w)+'\t'+str(coords[0])+'\t'+str(coords[1])+'\n')
		f.close()

def predict(pred_x,w):
    X = np.zeros((pred_x.size,w.size))

    for k in range(w.size):
        X[:,k] = np.power(pred_x,k)
    # print X, np.transpose(w)
    #the y-value for the corresponding x, if it were located on a grid line
    y_estimate = np.dot(X,np.transpose(w))

    return(y_estimate)

def squared_difference(estimate,true):
    sq_error = 0
    for x in range(estimate.size):
        sq_error+= pow((estimate[x] - true[x]),2)

    return(sq_error)

def estimate_conversion(trace_Data):
	#new estimated base-32 coordinates
	new_Coordinates = dd(lambda: dd(list))
	for trace in trace_Data:
		coord_List = trace_Data[trace]
		# the first weights for the first gridline to find
		w = 1
		#index within coordinate list of the data points
		data_Point = 0
		# indicates whether a gridline has been found
		grid_Found = False
		while data_Point <= len(coord_List):

			x = np.array([coord_List[data_Point]['x']])
			
			y = np.array([coord_List[data_Point]['y']])
			y_Est = predict(x,np.array([params[w]]))

			sq_Error = squared_difference(y_Est,y)

			if sq_Error < 1:
				new_Coordinates[trace][w].append([coord_List[data_Point]['x'],coord_List[data_Point]['y']])
				w += 1
				data_Point += 1
				grid_Found = True
			# if a grid line hasn't been found and the end of the trace has been reached,
			# move on to try to match the next grid line.
			elif (data_Point == len(coord_List)-1) and grid_Found == False:
				data_Point = 1
				w += 1
			# if the grid has previously been matched, and the end of the trace has been reached,
			# don't continue trying to match grid lines and halt loop
			elif (data_Point == len(coord_List)-1) and grid_Found == True:
				break
			else:
				data_Point += 1

		# fill in non-trace grid points with the traditional -1,-1
		for w in range(1,33):
			if w not in new_Coordinates[trace]:
				new_Coordinates[trace][w] = [[-1,-1]]

	return new_Coordinates



def extract_info(data):
	tracer = data['tracer-id']
	trace_data = data['trace-data']
	return(tracer, trace_data)


def main():

	#import a .json file
	# json_Path = raw_input("Specify a path to a .json file for back-conversion: ")
	# json_Path = "/Users/apiladmin/Desktop/Alex_Images/traces_09-21-15.json"
	json_Path = "/Users/apiladmin/Desktop/test.json"
	with open(json_Path,'r') as data_file:
		data = json.load(data_file)

	#extracts relevant data from json file
	tracer, trace_Data = extract_info(data)

	#grab the x,y-axis coordinate points which fall on each modelled line
	new_Coordinates = estimate_conversion(trace_Data)
	##390 is the new midpoint
	
	#convert to the old representation and save the trace file
	write_file(new_Coordinates, json_Path, tracer)




if __name__ == "__main__":
	main()
