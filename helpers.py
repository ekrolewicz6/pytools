import bs4
import lxml
import urllib2
import re
import json
import pandas as pd
import csv
import time

from multiprocessing.dummy import Pool as ThreadPool

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def get_domains(file):
	domains = {}
	company_names = [line for line in file.read().splitlines()]
	for company in company_names:
		if company not in domains:	
			try:
				html_String = 'https://www.google.com/search?q=%s' % company
				html_String = html_String.replace(" ", "%20")
				# print html_String, "this is the string"
				req = urllib2.Request(html_String, headers=hdr)
				content = urllib2.urlopen(req).read()
				soup = bs4.BeautifulSoup(content, 'lxml')
				# print "This is the soup body \n\n\n\n", soup.find('h3', {'class': 'r'}).find('a').get('href')
				href = soup.find('h3', {'class': 'r'}).find('a').get('href')
				# print 'The Domain is: \n', href
				domains[company] = {'domain':href}
			except AttributeError:
				print "Skipped: %s" % company
		else:
			print "%s already in domain list" % company
	return domains

def get_verified_emails(domains, hunter):
	# Create regex to retrieve emails
	p = re.compile('[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+')
	# Get JSON response for the each domain
	for company in domains:
		print "The address is ", domains[company]['domain']
		json = str(hunter.domain_search(domains[company]['domain']))
		extracted = [email for email in p.findall(json)]
		domains[company]['verified'] = extracted
	return domains

def is_verified(hunter,email):
	data = hunter.email_verifier(email)
	return data["result"] == "deliverable"

def verify_addresses(csv_file):
	df = pd.read_csv(csv_file)
	saved_column = df.Address
	# validate_addresses = get_validated_addresses(saved_column)
	# make the pool of workers
	# for i in range(0,4):
	# 	pool = ThreadPool(i)
	# 	validate_addresses = pool.map(validate_address,saved_column)
	# 	pool.close()
	# 	pool.join()
	verified_name = 'verified_%s' % csv_file
	start = time.time()
	validate_addresses = map(validate_address,saved_column)
	end = time.time()
	# print (end - start)
	with open('results/' + verified_name, 'wb') as f:
	    writer = csv.writer(f)
	    for val in validate_addresses:
	        writer.writerow([val])
	return "File Created: %s" % verified_name

def get_validated_addresses(address_list):
	validated = []
	for i, address in enumerate(address_list):
		print "Line: %d" % i
		validated.append(validate_address(address))
	return validated

def validate_address(address):
	try:
		html_String = 'https://www.google.com/search?q=%s' % address
		html_String = html_String.replace(" ", "%20")
		req = urllib2.Request(html_String, headers=hdr)
		content = urllib2.urlopen(req).read()
		soup = bs4.BeautifulSoup(content, 'lxml')
		# print "This is the soup body \n\n\n\n", soup.find('h3', {'class': 'r'}).find('a').get('href')
		address = soup.find('div', {'class': 'vk_sh vk_bk'}).string
		return address
	except AttributeError:
		return "N/A"




