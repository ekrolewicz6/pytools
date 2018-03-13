from pyhunter import PyHunter
import helpers as h
import csv

# 1) Get list of Domains from file
# 2) Use Hunter to get list of  email addresses
# 3) Write domains to CSV


hunter = PyHunter('$HUNTER_API_KEY')
filename = 'Portland100+'
# Read file & return a domains dictionary: {'company':{'domain':domain}}
file = open(filename+'.txt','r')
domains = h.get_domains(file)

#Returns a new copy of domains with unverified emails for each company
# verified = h.get_verified_emails(domains, hunter)

# print 'verified: \n', verified

# Write domains to a csv
with open('../results/'+filename+'.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    # fieldnames = ['Company', 'Domain', 'Verified_Emails']
    fieldnames = ['Company', 'Domain']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()

    for company in domains:
	    w.writerow({'Company': company, 'Domain': domains[company]['domain']})









