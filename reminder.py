# -*- coding: UTF-8 -*-

from fbchat import log, Client
from fbchat.models import *
import re, time

def generateUserData(username):
	user = client.searchForUsers(username)[0]

	print('user ID: {}'.format(user.uid))
	print("user's name: {}".format(user.name))
	print("user's photo: {}".format(user.photo))
	print("Is user client's friend: {}".format(user.is_friend))

	client.send(Message(text='Receiver ID: {}'.format(user.uid)), thread_id=user.uid, thread_type=ThreadType.USER)
	client.send(Message(text="Receiver's name: {}".format(user.name)), thread_id=user.uid, thread_type=ThreadType.USER)
	client.send(Message(text="Receiver's photo: {}".format(user.photo)), thread_id=user.uid, thread_type=ThreadType.USER)
	client.send(Message(text="Is Receiver client's friend: {}".format(user.is_friend)), thread_id=user.uid, thread_type=ThreadType.USER)

def setReminder(user, message, time):
	global reminders, client
	reminders.append(tuple((user, message, time)))
	print('Reminder set!')
	#print(reminders)

# Subclass fbchat.Client and override required methods
class ReminderBot(Client):

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        #log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        regex = r"remind ([a-zA-Z]+) to (.+) in (\d+\.*\d*) hours"
        if re.match(regex, message_object.text.lower()): #and author_id != self.uid:
        	print('Reminder caught!')
        	m = re.match(regex, message_object.text.lower())
        	reminder = m.group(2)
        	delay = float(m.group(3))
        	if m.group(1) == 'me':
        		user = client.fetchUserInfo(author_id)
        		print("Receiver: " + user[author_id].name)
        		setReminder(user[author_id], reminder, time.time() + (3600*delay))
        	else:
        		user = client.searchForUsers(m.group(1))[0]
        		print("Receiver: " + user.name)
        		setReminder(user, reminder, time.time() + (3600*delay))

        	print("Reminder: " + reminder)
        	print("Sending message in: " + str(delay) + " hours.")

        #	for str1 in message_object.text.lower().split("to"):
        #		print(re.search(r"remind ([a-zA-Z]+)", str1))
        #		for str2 in str.split("in"):
        #			print(re.search(r"(\d+) hours", str2))
        else:
        	print('Message not Matched!')
        # If you're not the author, echo
        #if author_id != self.uid:
         #   self.send(message_object, thread_id=thread_id, thread_type=thread_type)

    def onListening(idk):
    	global reminders
    	global client

    	print('Listening...')
    	print(reminders)
    	for tup in reminders:
    		if(tup[2] < time.time()):
    			client.send(Message(text='Reminder!: {}'.format(tup[1])), thread_id=tup[0].uid, thread_type=ThreadType.USER)
    	reminders = [i for i in reminders if i[2] > time.time()]
    	time.sleep(5)
    	client.listen()

reminders = []
client = ReminderBot("<email>", "<password>")
client.listen()
