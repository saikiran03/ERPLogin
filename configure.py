import sqlite3
from selenium import webdriver
import erpscrape
import time

# ========================================================================= #
# Database Operations

# initializes the database and table for data storage.
def initTable():

	conn = sqlite3.connect('ERPUserData.db')
	c = conn.cursor()

	sql = '''CREATE TABLE DATA (roll text primary key, pwd text, q1 text, q2 text, q3 text, a1 text, a2 text, a3 text)'''
	c.execute(sql)

	conn.commit()
	conn.close()

# inserts userdata into table if user doesn't exist else raises an error.
def insert(roll, pwd, secq, seca):
	conn = sqlite3.connect('ERPUserData.db')
	c = conn.cursor()

	# sql = '''SELECT * FROM DATA WHERE roll = ?'''
	# res = c.execute(sql, roll)
	# if len(res) > 0:
	# 	raise ValueError('User Already exists in the database.')

	# XXX NOTE : Very vulnerable piece. XXX
	sql = 'INSERT INTO DATA VALUES ("%s","%s","%s","%s","%s","%s","%s","%s")' % (roll, pwd, secq[0], secq[1], secq[2], seca[0], seca[1], seca[2])
	c.execute(sql)

	conn.commit()
	conn.close()

def select(roll):
	conn = sqlite3.connect('ERPUserData.db')
	c = conn.cursor()

	sql = 'SELECT * FROM DATA WHERE roll = "%s"' % (roll)
	res = c.execute(sql)
	row = res.fetchone()

	conn.commit()
	conn.close()
	return row
# ========================================================================= #

# ========================================================================= #
# webdriver operations

# fetches security questions from erp.
def fetch_security_ques(driver, rollno, pwd):
	qlist = [] # Questions list
	while len(qlist)<3:
		
		erpscrape.fillData(driver, 'user_id', rollno)
		erpscrape.fillData(driver, 'password', pwd)
		time.sleep(2)
		
		ques = driver.find_element_by_id('question').text
		if (not (ques in qlist)) and (ques != "") :
			qlist.append(ques)
			print "========================================="
			print "Found new question => %s" % (ques)
			print "========================================="
		
		driver.refresh()
	
	return qlist


def configure(driver):
	print "==========* WELCOME TO ERP LOGIN *==========\n\n"
	rollno = raw_input("Please enter your Roll Number : ")
	pwd = raw_input("Please enter your Password : ")
	print "\n\n"
	sec_ques = fetch_security_ques(driver, rollno, pwd)
	sec_answ = []

	print "\nPlease answer the following questions.\n"
	for ques in sec_ques:
		print ques
		ch = 'o'
		while ch.upper() != 'C':
			ans = raw_input("Answer : ")
			ch = raw_input("Enter C to confirm, or any other key to correct your answer.")
		sec_answ.append(ans)

	# Save Data to database to access in future.
	insert(rollno, pwd, sec_ques, sec_answ)

# ========================================================================= #

if __name__=='__main__':

	driver = webdriver.Firefox()

	driver.get('http://erp.iitkgp.ernet.in/')
	driver.get(driver.current_url)
	try:
		configure(driver)
	except:
		driver.close()

	driver.close()	