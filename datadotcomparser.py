import bs4
import csv

contacts = {}

for i in range(1,5):
	file_name = 'data%d.html' % i
	print file_name, "filename"
	file = open(file_name,'r') 
	content = file.read()
	soup = bs4.BeautifulSoup(content, 'lxml')
	for td in soup.find_all("td","td-name break-word name"):
		first_name = td.a.string.split(", ")[1]
		last_name = td.a.string.split(", ")[0]
		full_name = first_name + " " + last_name
		company = td.next_sibling.next_sibling.a.string
		title = td.next_sibling.next_sibling.next_sibling.next_sibling.string
		city = td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
		state = td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
		contacts[full_name] = {'company':company,'title':title,'city':city,'state':state}

print "Length of dictionary", len(contacts)
with open('data_com_contacts25+FacilitiesHR.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    # fieldnames = ['Company', 'Domain', 'Verified_Emails']
    fieldnames = ['Full Name', 'Company', 'Title','City','State']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()

    for contact in contacts:
	    try:
	    	w.writerow({'Full Name': contact, 
	    			'Company': contacts[contact]['company'],
	    			'Title': contacts[contact]['title'],
	    			'City': contacts[contact]['city'],
	    			'State': contacts[contact]['state'],
	    			})
	    except:
	    	continue
