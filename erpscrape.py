from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import configure

def fillData(driver, name, data):
	# print "Filling", name, "with", data
	for att in xrange(15):
		try:
			dn = driver.find_element_by_name(name)
			dn.clear()
			dn.send_keys(data)
			break
		except:
			pass
			# print "Attempt failed, retrying..."


def clickLink(driver, linkText):
	print "Rendering click on", linkText
	for att in xrange(15):
		try:
			driver.find_element_by_partial_link_text(linkText).click()
			break
		except:
			# print "Attempt failed, retrying..."
			time.sleep(1)


def fillForm(driver, roll):
	data = configure.select(roll)
	
	# User not configured.
	if data != None:

		fillData(driver, 'user_id', data[0])
		fillData(driver, 'password', data[1])
		
		# TODO: make this more robust. Ajax loading may take more than 1 second on slower connectinons.
		question = ""
		while question == "":
			time.sleep(1)
			question = driver.find_element_by_id('question').text

		# Answers to security questions
		if(question == data[2]):
			answer = data[5]
		elif(question == data[3]):
			answer = data[6]
		elif(question == data[4]):
			answer = data[7]
		else:
			answer = ""
		fillData(driver, 'answer', answer)
		print "Security Question answer = ", "*"*len(answer)
		print "Logging In ..."
		driver.find_element_by_name('user_id').send_keys(Keys.RETURN)

		time.sleep(5)
		try:
			driver.find_element_by_partial_link_text('Logout').text
			return True
		except:
			return False

	else:

		print "Please configure to use the login system."
		configure.configure(driver)
		fillForm(driver, roll)


if __name__ == '__main__':
	# Open and connect the driver to the url
	driver = webdriver.Firefox()
	driver.get('https://erp.iitkgp.ernet.in')
	driver.get(driver.current_url)

	# login
	roll = raw_input("Enter your roll : ").upper()
	is_logged_in = fillForm(driver, roll)

	if is_logged_in:
		# navigate to the notice board
		clickLink(driver, 'CDC')
		clickLink(driver, 'Student')
		clickLink(driver, 'Application')

		# close the window after 10 seconds.
		time.sleep(10)
		driver.find_element_by_partial_link_text('Logout').click()
		# driver.close()

	else:
		print "Login Failed. Invalid Credentials"
		driver.close()
