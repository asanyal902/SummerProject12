#!/usr/bin/env python
import ROOT 
import array
output = {}
count = {}
def dist(a,b,x,y):			#calculates euclidean distance between given points
	return ((x-a)*(x-a)+(y-b)*(y-b))

def comp(prim,sec):			#compares points in surrounding 8 buckets
	global output,count,m  	
	a = prim[0][0]
	b = prim[0][1]
	square = m*m 
	for val in reversed(sec):
		c = val[0][0]
		d = val[0][1]
		if (dist(a,b,c,d)) <= square :
			if (a,b) in output:
				output[(a,b)].append([(c,d)])			
			else:
				output[(a,b)] = [[(c,d)]]
			count[(a,b)] = count[(a,b)]+1
			sec.remove([(c,d)])

def main(r,name):
	global m 
	m=r
	f = open(name)
	varnames = ['x','y']	# the variable names for the output tuple
	vertex = {}	
	for line in f:			#initial copying of input into dictionary, each key being a tuple
		if(line!='\n'):			
			a = line.split()
			key = (int(float(a[0])/r),int(float(a[1])/r))			
			value = [(float(a[0]),float(a[1]))]			
			if key in vertex:
				vertex[key].append(value)
			else:
				vertex[key] = [value]	
	f.close()		
	#actual nearest neighbour search algo begins	
	global output,count
	mean = [] 
	for key in vertex:
		for pot in reversed(vertex[key]):		#check all 8 surrounding boxes for possible points		
			count[(pot[0][0],pot[0][1])] = 0			
			mean_x = 0
			mean_y = 0			
			comp(pot,vertex[key])
			if (key[0]+1,key[1]) in vertex:			
				comp(pot,vertex[(key[0]+1,key[1])])
			if (key[0]+1,key[1]+1) in vertex:			
				comp(pot,vertex[(key[0]+1,key[1]+1)])
			if (key[0],key[1]+1) in vertex:			
				comp(pot,vertex[(key[0],key[1]+1)])
			if (key[0]-1,key[1]) in vertex:			
				comp(pot,vertex[(key[0]-1,key[1])])
			if (key[0],key[1]-1) in vertex:			
				comp(pot,vertex[(key[0],key[1]-1)])
			if (key[0]-1,key[1]-1) in vertex:			
				comp(pot,vertex[(key[0]-1,key[1]-1)])	
			if (key[0]-1,key[1]+1) in vertex:			
				comp(pot,vertex[(key[0]-1,key[1]+1)])
			if (key[0]+1,key[1]-1) in vertex:			
				comp(pot,vertex[(key[0]+1,key[1]-1)])
			count[(pot[0][0],pot[0][1])] = count[(pot[0][0],pot[0][1])] - 1
			pot[0]
			for val in output[(pot[0][0],pot[0][1])]:
				mean_x = mean_x + val[0][0]
				mean_y = mean_y + val[0][1]
			mean.append([mean_x/(count[(pot[0][0],pot[0][1])]+1),mean_y/(count[(pot[0][0],pot[0][1])]+1)])	
	fout = ROOT.TFile("output.root", "RECREATE")	# open the output file
	fout.cd()
	output_tuple = ROOT.TNtuple("tuple","tuple",":".join(varnames)) 	# create the ntuple
	values = []	
	for l in mean:				# loop over events	
		values = [l[0],l[1]]	 # calculate the values to be stored in the output tuple
		output_tuple.Fill(array.array("f",values))
	output_tuple.SetMarkerColor(ROOT.kRed)
	output_tuple.SetMarkerStyle(7)
	output_tuple.Draw("y:x")	# end of loop over events and draw scatter plot of tntuple
	fout.cd()					# write the tuple to the output file and close it
	output_tuple.Write()	
if __name__ == '__main__': 
		import sys
		if len(sys.argv) < 3:
			print "Please enter "r" parameter and file name!"	
			sys.exit()
		if float(sys.argv[1]) == 0.0:
			print "Non Zero values only!!"	
			sys.exit()			
		main(float(sys.argv[1]), sys.argv[2])