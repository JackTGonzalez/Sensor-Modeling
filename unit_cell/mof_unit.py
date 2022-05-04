import os
import numpy as np
import re #library for regular expressions
import fnmatch #library for matching filenames
import itertools #for iterations
import math
## Code to determine number of unit cells necessary to fulfill cutoff requirements for H-T GCMC siml'ns
cutoff =12.8
## Grab unit cell dimensions from cif file
mofs = os.listdir("./")
mof_list=[]
for i in range(len(mofs)):
	if fnmatch.fnmatch(mofs[i], '*'+'cif'):
		mof_list.append(mofs[i])
for i in range(len(mof_list)):
	with open(mof_list[i], 'r') as cif:
		mof_cif= cif.read()
	for line in mof_cif.split("\n"):
		if "_cell_length_a" in line:
			length_a = line.split()[1]#unit cell vector
			length_a =float(length_a)#string to float
		if "_cell_length_b" in line:
			length_b = line.split()[1]
			length_b = float(length_b)
		if "_cell_length_c" in line:
			length_c= line.split()[1]
			length_c= float(length_c)
		if "_cell_angle_alpha" in line:
			alpha = line.split()[1]
			alpha = float(alpha)
		if "_cell_angle_beta" in line:
			beta= line.split()[1]
			beta= float(beta)
		if "_cell_angle_gamma" in line:
			gamma = line.split()[1]
			gamma = float(gamma)
	
	#Convert cif information to unit_cell vectors
	ax = length_a
	ay = 0.0
	az = 0.0
	bx = length_b * np.cos(gamma * np.pi / 180.0)
	by = length_b * np.sin(gamma * np.pi / 180.0)
	bz = 0.0
	cx = length_c * np.cos(beta * np.pi / 180.0)
	cy = (length_c * length_b * np.cos(alpha * np.pi /180.0) - bx * cx) / by
	cz = (length_c ** 2 - cx ** 2 - cy ** 2) ** 0.5
	
	unit_cell =  np.asarray([[ax, ay, az],[bx, by, bz], [cx, cy, cz]])
	#Unit cell vectors
	A = unit_cell[0]
	B = unit_cell[1]
	C = unit_cell[2]
	#minimum distances between unit cell faces
	Wa = np.divide(np.linalg.norm(np.dot(np.cross(B,C),A)), np.linalg.norm(np.cross(B,C)))
	Wb = np.divide(np.linalg.norm(np.dot(np.cross(C,A),B)), np.linalg.norm(np.cross(C,A)))
	Wc = np.divide(np.linalg.norm(np.dot(np.cross(A,B),C)), np.linalg.norm(np.cross(A,B)))
	#Wa = np.divide(np.linalg.norm(np.cross(np.dot(A,B),C)), np.linalg.norm(np.cross(B,C)))
	#Wb = np.divide(np.linalg.norm(np.cross(np.dot(B,C),A)), np.linalg.norm(np.cross(C,A)))
	#Wc = np.divide(np.linalg.norm(np.cross(np.dot(C,A),B)), np.linalg.norm(np.cross(A,B)))
	
	uc_x = int(np.ceil(cutoff/(0.5*Wa)))
	uc_y = int(np.ceil(cutoff/(0.5*Wb)))
	uc_z = int(np.ceil(cutoff/(0.5*Wc)))
	#uc_x = np.ceil(0.5*Wa/cutoff)
	#uc_y = np.ceil(0.5*Wb/cutoff)
	#uc_z = np.ceil(0.5*Wc/cutoff)
	print (mof_list[i], os.path.splitext(mof_list[i])[0])
	#print (length_a, alpha, length_b, beta, length_c, gamma)
	#print (Wa, Wb, Wc)
	print (uc_x, ' ', uc_y, ' ', uc_z)
	
	with open("mof_list_unitcell.dat", "a") as out_file:
		out_file.write(os.path.splitext(mof_list[i])[0]+ ' ' +str(uc_x)+ ' '+ str(uc_y)+ ' '+ str(uc_z) + '\n')
