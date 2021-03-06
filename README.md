# virginiaplatesearch
I wrote this to automate the process of searching for a list of vanity plates I want in Virginia. The trick is to check every day to grab the plate as soon as is becomes available. I did not want to do this manually each day and the APIs I found charged way too much money. This is my solution, which sends an email with the results.

Although I have not done this yet, I'd like to host the app as an Azure Function to run twice a day without the need for a dedicated virtual machine. There exist many other solutions to host and execute this on a schedule.

Plate values are stored as comma separated values in a txt file. The program logic will allow for up to any number of characters, but be aware that the website form will only allow 7 consecutive characters and 8 total characters if it includes a hyphen. If changes are made to the custom plate design within the program logic, be aware that some plates allow only 5 or 6 characters. In this case, if a string longer than the max number of available of characters is attempted, the program will hang. I will try to resolve this in future builds.

This program is not designed to function with all types of custom plate designs, but I will expand it to support that functionality in some way.

*********PLEASE NOTE************
Entering your email credentials in the program really is not secure, so please do it at your own risk. I strongly recommend creating a brand new mailbox solely for the purpose of sending this information to a mailbox of your choosing. The port can be changed if desired, although 465 is recommended.
