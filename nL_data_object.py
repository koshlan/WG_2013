def RepresentsFloat(s):
	try: 
		float(s)
		return True
	except ValueError:
		return False

class target:
	''' TARGETS CAN BE MADE UP OF COLLECTIONS OF ASSAYS'''
	def __init__(self, name):
		self.name = name
		self.assay_list = list()
		self.cpr_mean = float()
		self.cpr_stdev = float()
		self.cpr_count = float()
	
	def add_assay(self, s):
		self.assay_list.append(s)
	
	def calculate_cpr_stats(self):
		'''THIS GOES THROUGH EACH OF THE ASSAYS FOR THIS TARGET AND PULLS THE < cpr > VALUES. THEN CALCULATES SUMMARY STATISTICS'''
		import numpy
		my_list_of_lists = [a.list_cpr for a in self.assay_list if a.cpr_dilution_test == True] # GATHER ALL THE RESULTS IN LIST OF LISTS 
		my_collapsed_list = [item for sublist in my_list_of_lists  for item in sublist] # COLLAPSE TO A SINGLE LIST
		if len(my_collapsed_list) > 0:
			self.cpr_mean = numpy.mean(my_collapsed_list)
			self.cpr_stdev = numpy.std(my_collapsed_list) 
			self.cpr_count = len(my_collapsed_list)




class assay:
	def __init__(self, name, target, assay_type, curve_type):
		self.name = name # NAME OF THE ASSAY
		self.target = target # NAME OF THE TARGET REF SEQ
		self.assay_type = assay_type # ASSAY TYPE "extended" "specific" or "private"
		self.curve_type = curve_type # ASSAY CURVE CALCULATION TYPE
		self.list_cpr = list() # cpr -> "copies per reaction"
		self.list_dilute_cpr = list()
		self.list_ct = list()
		self.list_dilute_ct = list()
		self.cpr_mean = float()
		self.dilute_cpr_mean = float()
		self.ct_mean = float()
		self.dilute_ct_mean = float()
		self.cpr_dilution_ratio = float()
		self.desired_cpr_dilution_ratio = float(2)
		self.cpr_dilution_test = False
		self.ct_minimum_cutoff = 31
	def calculate_mean(self, my_list):
		'''returns the mean of a list'''
		import numpy
		return numpy.mean(my_list)
	
	def test_dilution_ratio(self):
		if self.dilution_ratio > self.desired_dilution_ratio:
			self.dilution_test_result = True
		else:
			self.dilution_test_result = False
	
	def perform_all_calculations(self):
		'''Run All The Above Functions'''
		if len(self.list_ct) > 0 and len(self.list_cpr) > 0:
			self.ct_mean = self.calculate_mean(self.list_ct)
			self.cpr_mean = self.calculate_mean(self.list_cpr)
		if len(self.list_dilute_ct) > 0 and len(self.list_dilute_cpr) > 0:
			self.dilute_cpr_mean = self.calculate_mean(self.list_dilute_cpr)
			self.dilute_ct_mean = self.calculate_mean(self.list_dilute_ct)
		if len(self.list_cpr) > 0 and len(self.list_dilute_cpr) > 0:	
			self.cpr_dilution_ratio = self.cpr_mean/self.dilute_cpr_mean
		if self.ct_mean < self.ct_minimum_cutoff and len(self.list_dilute_ct) == 0:
			 self.cpr_dilution_test = True
		elif self.cpr_dilution_ratio > self.desired_cpr_dilution_ratio:
			self.cpr_dilution_test = True
		else:
			self.cpr_dilution_test = False
	
	
# 
# X = assay("ACZ1_1","ACZ","spec", 'calc')
# X.list_cpr.append(10.5)
# X.list_cpr.append(11.5)
# X.list_dilute_cpr.append(5.5)
# X.list_dilute_cpr.append(4.5)
# Y = assay("ACZ1_1","ACZ","spec", 'calc')
# Y.list_cpr.append(6.1)
# Y.list_cpr.append(6.5)
# 
# 					# Y.list_dilute_cpr.append(4)
# 					# Y.list_dilute_cpr.append(4.5)
# 					# print X.name
# 					# print X.list_ct
# 					# X.calculate_ct_mean()
# 					# X.calculate_dilute_ct_mean()
# 					# X.caclulate_dilution_ratio()
# 					# X.test_dilution_ratio()
# 					# Y.calculate_ct_mean()
# 					# Y.calculate_dilute_ct_mean()
# 					# Y.caclulate_dilution_ratio()
# 					# Y.test_dilution_ratio()
# X.perform_all_calculations()
# Y.perform_all_calculations()
# print
# print Y.__dict__
# print
# 						# print X.ct_mean
# 						# print X.dilute_ct_mean
# 						# print X.dilution_ratio
# 						# print X.desired_dilution_ratio
# 						# print X.dilution_test_result
# 						# print X.__dict__['ct_mean']
# 
# T = target('A')
# T.add_assay(X)
# T.add_assay(Y)
# T.calculate_cpr_stats()
# print T.__dict__