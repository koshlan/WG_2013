from nL_data_object import target, assay, RepresentsFloat
import re
import sys

#### POPULATE DATABASE #####
#fh = open('./Ex_Inputs/nL_WG_summarize_test_input.txt', 'r')
fh = open(sys.argv[1],'r')
list_assay_names = list()
list_sample_names = list()
dict_assay_objects = dict()
for line in fh:
	line = line.strip()
	my_sample = line.split("\t")[3]
	r = re.match('(OSU_[0-9]+)_*', my_sample)
	k = re.search('1to5', my_sample)
	my_sample = r.group(1)	
	if k:
		my_conc = 1.0
	else: 
		my_conc = 5.0
	try:
		my_cpr= float(line.split("\t")[-5])
		my_ct = float(line.split("\t")[5])
	except ValueError:
		my_cpr= 'null'
		my_ct = 'null'	
	my_class = line.split("\t")[-1]
	my_assay = line.split("\t")[2]
	my_target = my_assay.split("_")[0]
	my_multiple_peaks = "null"
	if my_sample not in dict_assay_objects.keys():
		list_sample_names.append(my_sample)
		dict_assay_objects[my_sample] = dict() 
	if my_assay not in dict_assay_objects[my_sample].keys():
		list_assay_names.append(my_assay)
		a = assay(my_assay,my_target,my_class,my_class)
		dict_assay_objects[my_sample][my_assay] = a
	if RepresentsFloat(my_ct) and RepresentsFloat(my_cpr): # CHECK THAT YOU ACTUALLY HAVE A VALUE NOT A 'NA'
		if my_conc == 5.0:
			dict_assay_objects[my_sample][my_assay].list_ct.append(my_ct)
			dict_assay_objects[my_sample][my_assay].list_cpr.append(my_cpr)
		elif my_conc == 1.0:
			dict_assay_objects[my_sample][my_assay].list_dilute_ct.append(my_ct)
			dict_assay_objects[my_sample][my_assay].list_dilute_cpr.append(my_cpr)
fh.close()
#### EXECUTE CALCULATIONS FOR EACH ASSAY #####
for s in list_sample_names:
	for a in list_assay_names:
		dict_assay_objects[s][a].perform_all_calculations()
		
#### IN THE LAST LINE BASICALLY WE ARE GOING TO GO THROUGH ALL OF OUR OBJECTS, AND ADD THEM TO TARGET OBJECTS

dict_target_objects = {}
for s in list_sample_names:
	for a in list_assay_names:
		x = dict_assay_objects[s][a]
		target_name =  x.target
		if target_name.startswith(">de") or target_name.startswith(">16") or target_name.startswith(">RD"):
			continue
		else:
			if target_name not in dict_target_objects.keys():
				y = target(target_name)
				dict_target_objects[target_name] = y
			dict_target_objects[target_name].assay_list.append(x)

for target_name in dict_target_objects.keys():
	dict_target_objects[target_name].calculate_cpr_stats()
	
for target_name in sorted(dict_target_objects.keys()):
	print "%s\t%f\t%f\t%f" %(target_name, dict_target_objects[target_name].cpr_mean, dict_target_objects[target_name].cpr_stdev, dict_target_objects[target_name].cpr_count)
	

# print dict_target_objects.keys()
# import pprint 
# pp = pprint.PrettyPrinter(indent = 4)
# pp.pprint(dict_target_objects)
# 		
		




# #.perform_all_calculations()
# for sample_name in list_sample_names:
# 	for assay_name in list_assay_names:
# 		dict_assay_objects[my_sample][my_assay].perform_all_calculations()
# 
# 
# import pprint 
# pp = pprint.PrettyPrinter(indent = 4)
# pp.pprint(dict_assay_objects['OSU_5']['>ACZ62482.1_1084_spec_F_527'].__dict__)
# 
# # dict_assay_objects['OSU_5']['>ACZ62482.1_1084_spec_F_527']
# # pp.pprint(dict_assay_objects['OSU_5']['>ACZ62482.1_1084_spec_F_527'].__dict__)
# # 
# # #dict_assay_objects['OSU_5']['>ACZ62482.1_1084_spec_F_527'].perform_all_calculations()
# # dict_assay_objects['OSU_5']['>ACZ62482.1_1084_spec_F_527'].perform_all_calculations()
# # pp.pprint(dict_assay_objects['OSU_5']['>ACZ62482.1_1084_spec_F_527'].__dict__)
# # 
# # 
# # 
# # for sample_name in list_sample_names:
# #  	for assay_name in list_assay_names:
# # 		print my_target, my_class
# #  		print dict_assay_objects[my_sample][my_assay].__dict__
# # 		print "%s\t%s"%(sample_name,assay_name)
# # # 
# # 
# # print "\n"*5
# # import pprint 
# # pp = pprint.PrettyPrinter(indent = 4)
# # pp.pprint(dict_assay_objects['OSU_5']['>ACZ62482.1_1084_spec_F_527'].__dict__)
# # 
# # 	
# 	# 0 	Row
# 	# 1 	Column
# 	# 2 	Assay
# 	# 3 	ID
# 	# 4 	Sample
# 	# 5 	Conc
# 	# 6 	Ct
# 	# 7 	Tm
# 	# 8 	Expected
# 	# 9 	Tm
# 	# 10 	R2
# 	# 11 	Chi2
# 	# 12 	Straight
# 	# 13 	R2
# 	# 14 	Efficiency
# 	# 15 	Multiple
# 	# 16 	peaks
# 	# 17 	Outlier
# 	# 18 	Multimodal
# 	# 19 	melt
# 	# 20 	peaks
# 	# 21 	F0
# 	# 22 	Flags
# 	# 23 	Asymmetry
# 	# 24 	A
# 	# 25 	B
# 	# 26 	C
# 	# 27 	D
# 	# 28 	E
# 	# 29 	AmpRatio
# 	# 30 	Tm
# 	# 31 	minus
# 	# 32 	mean
# 	# 33 	Ct
	# 34 	minus
	# 35 	mean
	

