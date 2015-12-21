#!/bin/usr/python

num_rows = sum(1 for line in open("traindata.txt", "r"))
data = [0] * num_rows

counter = 0
with open("traindata.txt", "r") as td:
	for line in td:
		data[counter] = line.split()
		counter += 1

# prob_trimono_hts_gene = {'0': 0.9, '1': 0.1}
# prob_dunetts_syndrome = {'0': 0.5, '1': 0.25, '2': 0.25}
# prob_sloepnea = {'110': 0.001, '010': 0.999, '111': 0.01, '011': 0.99, '112': 0.05, '012': 0.95, '100': 0.05, '000': 0.95, '101': 0.3, '001': 0.7, '102': 0.4, '002': 0.6}
# prob_foriennditis = {'10': 0.05, '00': 0.95, '11': 0.5, '01': 0.5, '12': 0.15, '02': 0.85}
# prob_degar_spots = {'10': 0.05, '00': 0.95, '11': 0.18, '01': 0.82, '12': 0.55, '02': 0.45}

prob_trimono_hts_gene = {'0': 0.9, '1': 0.1}
prob_dunetts_syndrome = {'0': 0.5, '1': 0.25, '2': 0.25}
prob_sloepnea = {'110': 0.001, '010': 0.999, '111': 0.01, '011': 0.99, '112': 0.05, '012': 0.95, '100': 0.05, '000': 0.95, '101': 0.3, '001': 0.7, '102': 0.4, '002': 0.6}
prob_foriennditis = {'10': 0.01, '00': 0.99, '11': 0.9, '01': 0.1, '12': 0.09, '02': 0.91}
prob_degar_spots = {'10': 0.01, '00': 0.99, '11': 0.09, '01': 0.91, '12': 0.9, '02': 0.1}

diff = 1
prev = 0

while diff > 0.01:
	print diff
	ds_gene_s_f_d_table = {}

	for ds in xrange(0,3):
		product_ds = prob_dunetts_syndrome[str(ds)]
		for gene in xrange(0, 2):
			product_gene = product_ds * prob_trimono_hts_gene[str(gene)]
			for s in xrange(0, 2):
				product_s = product_gene * prob_sloepnea[str(s) + str(gene) + str(ds)]
				for f in xrange(0, 2):
					product_f = product_s * prob_foriennditis[str(f) + str(ds)]
					for d in xrange(0, 2):
						product_d = product_f * prob_degar_spots[str(d) + str(ds)]
						ds_gene_s_f_d_table[str(ds) + str(gene) + str(s) + str(f) + str(d)] = [product_d, None]

	# for ds in xrange(0,3):
	# 	for gene in xrange(0, 2):
	# 		for s in xrange(0, 2):
	# 			for f in xrange(0, 2):
	# 				for d in xrange(0, 2):
	# 					product = prob_dunetts_syndrome[str(ds)] * prob_trimono_hts_gene[str(gene)] * prob_sloepnea[str(s) + str(gene) + str(ds)] * prob_foriennditis[str(f) + str(ds)] * prob_degar_spots[str(d) + str(ds)]
	# 					ds_gene_s_f_d_table[str(ds) + str(gene) + str(s) + str(f) + str(d)] = [product, None]

	weight_sum = 0
	for s in xrange(0, 2):
		for f in xrange(0, 2):
			for d in xrange(0, 2):
				for ds in xrange(0, 3):
					for gene in xrange(0, 2):
						lookup = str(ds) + str(gene) + str(s) + str(f) + str(d)
						weight_sum += ds_gene_s_f_d_table[lookup][0]
				for ds in xrange(0, 3):
					for gene in xrange(0, 2):
						lookup = str(ds) + str(gene) + str(s) + str(f) + str(d)
						ds_gene_s_f_d_table[lookup][1] = ds_gene_s_f_d_table[lookup][0] / weight_sum
				weight_sum = 0

	result = []
	for entry in data:
		lookup_suffix = "".join(entry[:3])
		lookup_suffix = entry[3] + lookup_suffix
		if entry[-1] == '-1':
			for ds in xrange(0, 3):
				lookup = str(ds) + lookup_suffix
				result.append([lookup, ds_gene_s_f_d_table[lookup]])
		else:
			lookup = str(ds) + lookup_suffix
			result.append([lookup, ds_gene_s_f_d_table[lookup]])
	# print sum(entry[1][0] for entry in result)
	# print sum(entry[1][1] for entry in result)
	# print sum(result[i][1][0] for i in range(100))
	# print sum(result[i][1][1] for i in range(100))

	weight_sum = sum(entry[1][1] for entry in result)
	prob_sum = sum(entry[1][0] for entry in result)

	#ds_no = sum(entry[1][1] for entry in result if entry[0][0] == '0')
	#ds_mild = sum(entry[1][1] for entry in result if entry[0][0] == '1')
	#ds_severe = sum(entry[1][1] for entry in result if entry[0][0] == '2')
	ds_no = 0
	ds_mild = 0
	ds_severe = 0
	#gene = sum(entry[1][1] for entry in result if entry[0][1] == '1')
	gene = 0
	# s_100_top = sum(entry[1][1] for entry in result if entry[0][1] == '0' and entry[0][0] == '0' and entry[0][2] == '1')
	# s_100_bot = sum(entry[1][1] for entry in result if entry[0][1] == '0' and entry[0][0] == '0')
	# s_101_top = sum(entry[1][1] for entry in result if entry[0][1] == '0' and entry[0][0] == '1' and entry[0][2] == '1')
	# s_101_bot = sum(entry[1][1] for entry in result if entry[0][1] == '0' and entry[0][0] == '1')
	# s_102_top = sum(entry[1][1] for entry in result if entry[0][1] == '0' and entry[0][0] == '2' and entry[0][2] == '1')
	# s_102_bot = sum(entry[1][1] for entry in result if entry[0][1] == '0' and entry[0][0] == '2')
	# s_110_top = sum(entry[1][1] for entry in result if entry[0][1] == '1' and entry[0][0] == '0' and entry[0][2] == '1')
	# s_110_bot = sum(entry[1][1] for entry in result if entry[0][1] == '1' and entry[0][0] == '0')
	# s_111_top = sum(entry[1][1] for entry in result if entry[0][1] == '1' and entry[0][0] == '1' and entry[0][2] == '1')
	# s_111_bot = sum(entry[1][1] for entry in result if entry[0][1] == '1' and entry[0][0] == '1')
	# s_112_top = sum(entry[1][1] for entry in result if entry[0][1] == '1' and entry[0][0] == '2' and entry[0][2] == '1')
	# s_112_bot = sum(entry[1][1] for entry in result if entry[0][1] == '1' and entry[0][0] == '2')
	#            0          1
	#         0  1  2    0  1  2
	s_top = [[0, 0, 0], [0, 0, 0]]
	s_bot = [[0, 0, 0], [0, 0, 0]]
	# f_10_top = sum(entry[1][1] for entry in result if entry[0][0] == '0' and entry[0][3] == '1')
	# f_10_bot = sum(entry[1][1] for entry in result if entry[0][0] == '0')
	# f_11_top = sum(entry[1][1] for entry in result if entry[0][0] == '1' and entry[0][3] == '1')
	# f_11_bot = sum(entry[1][1] for entry in result if entry[0][0] == '1')
	# f_12_top = sum(entry[1][1] for entry in result if entry[0][0] == '2' and entry[0][3] == '1')
	# f_12_bot = sum(entry[1][1] for entry in result if entry[0][0] == '2')
	f_top = [0, 0, 0]
	f_bot = [0, 0, 0]
	# d_10_top = sum(entry[1][1] for entry in result if entry[0][0] == '0' and entry[0][4] == '1')
	# d_10_bot = sum(entry[1][1] for entry in result if entry[0][0] == '0')
	# d_11_top = sum(entry[1][1] for entry in result if entry[0][0] == '1' and entry[0][4] == '1')
	# d_11_bot = sum(entry[1][1] for entry in result if entry[0][0] == '1')
	# d_12_top = sum(entry[1][1] for entry in result if entry[0][0] == '2' and entry[0][4] == '1')
	# d_12_bot = sum(entry[1][1] for entry in result if entry[0][0] == '2')
	d_top = [0, 0, 0]
	d_bot = [0, 0, 0]


	for entry in result:
		field_ds = entry[0][0]
		field_gene = entry[0][1]
		field_s = entry[0][2]
		field_f = entry[0][3]
		field_d = entry[0][4]
		field_weight = entry[1][1]
		# weight_sum += field_weight
		# prob_sum += entry[1][0]
		# ds
		if field_ds == '0':
			ds_no += field_weight
		elif field_ds == '1':
			ds_mild += field_weight
		elif field_ds == '2':
			ds_severe += field_weight
		# gene
		if field_gene == '1':
			gene += field_weight
		# s
		if field_gene == '1' and field_ds == '0':
			s_bot[1][0] += field_weight
			if field_s == '1':
				s_top[1][0] += field_weight
		elif field_gene == '1' and field_ds == '1':
			s_bot[1][1] += field_weight
			if field_s == '1':
				s_top[1][1] += field_weight
		elif field_gene == '1' and field_ds == '2':
			s_bot[1][2] += field_weight
			if field_s == '1':
				s_top[1][2] += field_weight
		elif field_gene == '0' and field_ds == '0':
			s_bot[0][0] += field_weight
			if field_s == '1':
				s_top[0][0] += field_weight
		elif field_gene == '0' and field_ds == '1':
			s_bot[0][1] += field_weight
			if field_s == '1':
				s_top[0][1] += field_weight
		elif field_gene == '0' and field_ds == '2':
			s_bot[0][2] += field_weight
			if field_s == '1':
				s_top[0][2] += field_weight
		# f
		if field_ds == '0':
			f_bot[0] += field_weight
			if field_f == '1':
				f_top[0] += field_weight
		elif field_ds == '1':
			f_bot[1] += field_weight
			if field_f == '1':
				f_top[1] += field_weight
		elif field_ds == '2':
			f_bot[2] += field_weight
			if field_f == '1':
				f_top[2] += field_weight
		# d
		if field_ds == '0':
			d_bot[0] += field_weight
			if field_d == '1':
				d_top[0] += field_weight
		elif field_ds == '1':
			d_bot[1] += field_weight
			if field_d == '1':
				d_top[1] += field_weight
		elif field_ds == '2':
			d_bot[2] += field_weight
			if field_d == '1':
				d_top[2] += field_weight

	prob_dunetts_syndrome['0'] = ds_no / weight_sum
	prob_dunetts_syndrome['1'] = ds_mild / weight_sum
	prob_dunetts_syndrome['2'] = ds_severe / weight_sum
	prob_trimono_hts_gene['1'] = gene / weight_sum
	prob_trimono_hts_gene['0'] = 1 - prob_trimono_hts_gene['1']
	prob_sloepnea['110'] = s_top[1][0] / s_bot[1][0]
	prob_sloepnea['010'] = 1 - prob_sloepnea['110']
	prob_sloepnea['111'] = s_top[1][1] / s_bot[1][1]
	prob_sloepnea['011'] = 1 - prob_sloepnea['111']
	prob_sloepnea['112'] = s_top[1][2] / s_bot[1][2]
	prob_sloepnea['012'] = 1 - prob_sloepnea['112']
	prob_sloepnea['100'] = s_top[0][0] / s_bot[0][0]
	prob_sloepnea['000'] = 1 - prob_sloepnea['100']
	prob_sloepnea['101'] = s_top[0][1] / s_bot[0][1]
	prob_sloepnea['001'] = 1 - prob_sloepnea['101']
	prob_sloepnea['102'] = s_top[0][2] / s_bot[0][2]
	prob_sloepnea['002'] = 1 - prob_sloepnea['102']
	prob_foriennditis['10'] = f_top[0] / f_bot[0]
	prob_foriennditis['00'] = 1 - prob_foriennditis['10']
	prob_foriennditis['11'] = f_top[1] / f_bot[1]
	prob_foriennditis['01'] = 1 - prob_foriennditis['11']
	prob_foriennditis['12'] = f_top[2] / f_bot[2]
	prob_foriennditis['02'] = 1 - prob_foriennditis['12']
	prob_degar_spots['10'] = d_top[0] / d_bot[0]
	prob_degar_spots['00'] = 1 - prob_degar_spots['10']
	prob_degar_spots['11'] = d_top[1] / d_bot[1]
	prob_degar_spots['01'] = 1 - prob_degar_spots['11']
	prob_degar_spots['12'] = d_top[2] / d_bot[2]
	prob_degar_spots['02'] = 1 - prob_degar_spots['12']

	diff = abs(prob_sum - prev)
	prev = prob_sum

	print prob_dunetts_syndrome
	# print prob_trimono_hts_gene
	# print prob_sloepnea
	# print prob_foriennditis
	# print prob_degar_spots
