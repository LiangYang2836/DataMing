
import os

def parse_data(source_file_path, destination_file_path):

	f_w = open(os.path.join(destination_file_path), 'w')
	with open(os.path.join(source_file_path), 'r') as f:
		for line in f:
			tmp_str = ''
			#print('line', line.split())
			line_details = line.split()
			temperature = line_details[0].replace(',', '.')
			'''
			nausea = line_details[1]
			lumbar_pain = line_details[2]
			urine_pushing = line_details[3]
			micturition_pains = line_details[4]
			burning_of_urethra = line_details[5]
			inflammation_of_urinary_bladder = line_details[6]
			nephritis_of_renal_pelvis_origin  = line_details[7]
			'''

			'''
			if float(temperature) <= 36:
				tmp_str += 'temperature_1'
			elif float(temperature) > 36 and float(temperature) <= 37:
				tmp_str += 'temperature_2'
			elif float(temperature) > 37 and float(temperature) <= 38:
				tmp_str += 'temperature_3'
			elif float(temperature) > 38 and float(temperature) <= 39:
				tmp_str += 'temperature_4'
			elif float(temperature) > 39 and float(temperature) <= 40:
				tmp_str += 'temperature_5'
			elif float(temperature) > 40 and float(temperature) <= 41:
				tmp_str += 'temperature_6'
			else:
				tmp_str += 'temperature_7'
			'''
			
			if float(temperature) >= 37.5:
				tmp_str += 'fever'
				tmp_str += ','
			#else:
				#tmp_str += 'fever_n'
			#tmp_str += ','

			for i in range(1, 8):
				if line_details[i] == 'yes':
					tmp_str += 'symptom_' + str(i)# + '_y'
					tmp_str += ','
				#else:
					#tmp_str += 'symptom_' + str(i) + '_n'
					#tmp_str += ','
				#tmp_str += ','
			if tmp_str[-1] == ',':
				tmp_str = tmp_str[:-1]
			tmp_str += '\n'
			#print('tmp_str', tmp_str)
			f_w.write(tmp_str)

			'''
			if line_details[1] == 'yes':
				tmp_str += 'symptom_1_y'
			else:
				tmp_str += 'symptom_1_n'
			tmp_str += ','

			if line_details[2] == 'yes':
				tmp_str += 'symptom_2_y'
			else:
				tmp_str += 'symptom_2_n'
			tmp_str += ','

			if line_details[3] == 'yes':
				tmp_str += 'symptom_3_y'
			else:
				tmp_str += 'symptom_3_n'
			tmp_str += ','

			if line_details[4] == 'yes':
				tmp_str += 'symptom_4_y'
			else:
				tmp_str += 'symptom_4_n'
			tmp_str += ','

			if line_details[5] == 'yes':
				tmp_str += 'symptom_5_y'
			else:
				tmp_str += 'symptom_5_n'
			tmp_str += ','

			if line_details[6] == 'yes':
				tmp_str += 'symptom_6_y'
			else:
				tmp_str += 'symptom_6_n'
			tmp_str += ','

			if line_details[7] == 'yes':
				tmp_str += 'symptom_7_y'
			else:
				tmp_str += 'symptom_7_n'

			#if tmp_str[-1] == ',':
				#tmp_str = tmp_str[:-1]

			tmp_str += '\n'

			#print('tmp_str', tmp_str)

			f_w.write(tmp_str)
			'''

	f.close()
	f_w.close()

if __name__ == '__main__':

	source_file_path = 'diagnosis.txt'
	destination_file_path = 'diagnosis_parsed.txt'
	parse_data(source_file_path, destination_file_path)