import re, sys
from directory.models import *

def zalivchik():

	file_path = '/home/mnmyasis/dev/fedor_app/files/basedirectory3.txt'
	#file_path = 'basedirectory.txt'
	file = open(file_path)
	print('start')
	for line in file:
		res = re.split('\t', line)
		try:
			umbrella_brand = res[1]
			source = res[20]
			tn_fv = res[21]
			registration_tm = res[2]
			corporation = res[22]
			manufacturer = res[3]
			full_corp = res[18]
			corp_rus = res[17]
			country = res[0]
			rx_otc = res[4]
			trade_name_rus = res[5]
			trade_name_eng = res[6]
			pack_key = res[7]
			fv_short = res[8]
			type_packing_fv = res[9]
			dosage = res[10]
			volwe = res[11]
			numero = res[12]
			tastes_and_parentheses_fv = res[13]
			vendor_code = res[14]
			divisible_packaging = res[19]
			size = res[15]
			age = res[16]

			print("{}".format(res))
			BaseDirectory.objects.create(
					umbrella_brand = umbrella_brand,
					source = source,
					tn_fv = tn_fv,
					registration_tm = registration_tm,
					corporation = corporation,
					manufacturer = manufacturer,
					full_corp = full_corp,
					corp_rus = corp_rus,
					country = country,
					rx_otc = rx_otc,
					trade_name_rus = trade_name_rus,
					trade_name_eng = trade_name_eng,
					pack_key = pack_key,
					fv_short = fv_short,
					type_packing_fv = type_packing_fv,
					dosage = dosage,
					volwe = volwe,
					numero = numero,
					tastes_and_parentheses_fv = tastes_and_parentheses_fv,
					vendor_code = vendor_code,
					#divisible_packaging = divisible_packaging,
					size = size,
					age = age,
					)
				#print(res)

		except IndexError:
			ss = open('error.txt', 'a')
			ss.write("{}\n".format(res))
			print("error - {}".format(res))

def zaliv_client_dict():
	file_path = '/home/mnmyasis/dev/fedor_app/files/asna2.txt'
	#file_path = 'asna2.txt'
	file = open(file_path)
	print('start')
	for line in file:
		res = re.split('\t', line)
		try:
			nnt = res[0]
			name = res[1]

			print("{}".format(res))
			ClientDirectory.objects.create(
				nnt=nnt,
				name=name,
				number_competitor=1
			)
		# print(res)

		except IndexError:
			ss = open('error.txt', 'a')
			ss.write("{}\n".format(res))
			print("error - {}".format(res))

def edit():
	#asna = BaseDirectory.objects.all()
	file_path = 'pharm_drugstore/baseinfo.txt'
	#file_path = 'baseinfo.txt'
	file = open(file_path)
	print('start')
	for line in file:
		res = re.split('\t', line)
		full_corp = res[5]
		corp_rus = res[6]
		pack_key = res[11]
		print('{} - {} - {}'.format(full_corp, corp_rus, pack_key))
		ss = BaseDirectory.objects.get(pack_key = pack_key)
		ss.corp_rus = corp_rus
		ss.full_corp = full_corp
		ss.save()
if __name__ == '__main__':
	#edit()
	zalivchik()
	#zaliv_client_dict()

