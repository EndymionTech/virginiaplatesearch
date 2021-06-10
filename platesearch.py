from selenium import webdriver
import time
import smtplib, ssl

#Open plate list file and import into content variable
platelist = open("platelist.txt", "r")
content = platelist.read()

#Split content variable on commas into content_list array
content_list = content.split(",")

#Close plate list file
platelist.close()

#Open browser to VA DMV page
web = webdriver.Chrome()
web.get("https://www.dmv.virginia.gov/dmvnet/plate_purchase/select_plate.asp")

#Change to frame containing plate type list
web.switch_to.frame('s2plttype')

#Search list and select the proper option
#The option text can be changed if you wish to have a different plate style
#Change the option.text comparison value to the text found in the list
el = web.find_element_by_name('plttype')
for option in el.find_elements_by_tag_name('option'):
    if option.text == 'Passenger Standard Issue':
        option.click()
        break

#Begin outer loop for each plate
wordIndex = 0
resultsEmail = []
for i in range(len(content_list)):
	s = content_list[wordIndex]
	l = list(s)

	#Move back to parent frame
	web.switch_to.parent_frame()
	web.switch_to.frame('s2end')

	#Begin inner loop for each letter
	letNum = "Let1"
	index = 0
	for i in range(len(l)):
		c = web.find_element_by_name(letNum)
		c.send_keys(l[index])
		index += 1
		letNum = "Let" + str(1 + index)

	#Click the "View Plate" button
	submit = web.find_element_by_xpath('/html/body/table/tbody/tr/td/table[1]/tbody/tr[5]/td[2]/table/tbody/tr/td[9]/input[2]')
	submit.click()

	#Pause
	time.sleep(1)

	#Look through text to determine results
	#Print results in terminal
	#Store results in resultsEmail array
	results = web.find_element_by_xpath('/html/body/table/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/font')
	if results.text == "Personalized message already taken. You can only purchase it if you already reserved this message or it is on a vehicle you own.":
		print(content_list[wordIndex] + "\t - Not available")
		resultsEmail.append(str(content_list[wordIndex]) + " - Not available")
	elif results.text == "Personalized message requested is not available. Please try another message.":
		print(content_list[wordIndex] + "\t - Invalid combination")
		resultsEmail.append(str(content_list[wordIndex]) + " - Invalid combination")
	else:
		print(content_list[wordIndex] + "\t - AVAILABLE!!!")
		resultsEmail.append(str(content_list[wordIndex]) + " - AVAILABLE!!!")

	#Clear form for each plate
	submit = web.find_element_by_xpath('/html/body/table/tbody/tr/td/table[1]/tbody/tr[5]/td[2]/table/tbody/tr/td[9]/input[1]')
	submit.click()

	wordIndex += 1

#Send results through email
sender_email = "<SENDER_EMAIL>"
receiver_email = "<RECIPIENT_EMAIL>"
message = """\
Subject: Daily Plate Search Results
"""

index = 0
for i in range(len(content_list)):
	message += resultsEmail[index] + "\n"
	index += 1

#Password for the sender mailbox
port = 465  # For SSL
password = "<PASSWORD>"

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("<SENDER_EMAIL>", password)
    server.sendmail(sender_email, receiver_email, message)

#Close browser, mark search complete, quit Python
web.close()
print("---------------\nSEARCH COMPLETE")
quit()