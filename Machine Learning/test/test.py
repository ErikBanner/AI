#!/usr/bin/python
import sqlite3
import operator
import random
from datetime import datetime, timedelta
from random import randint, choice

# Constants
DATABASE_FILE_NAME = "test.db"
SORTING_PERIOD = 30
LETTERS = "abcdefghijklmnopqrstuvwxyz"
PREFIX = "x"
SUFFIX = ".ca"

# Since the mailing table will initially be empty and new addresses will be added on a daily basis,
# and the script is used to update a table which holds a daily count of email addresses, the code
# should be run once on a daily basis as well.


def update_daily_added_emails(update_date):
	connection = sqlite3.connect(DATABASE_FILE_NAME)
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()
	cur_date_str = datetime.strftime(update_date, "%Y-%m-%d")
	with connection:
		# create a table for daily update
		sql_cmd = """
			CREATE TABLE IF NOT EXISTS daily(Domain TEXT, CountDaily INT, CountTotal INT, ThirtyDayCount TEXT);
			UPDATE daily SET CountDaily = 0;
			"""
		cursor.executescript(sql_cmd)
		cursor.execute("SELECT * FROM mailing WHERE DateAdded=?", [cur_date_str]) # get all emails that are added at current date
		entries_in_mailing = cursor.fetchall()
		for entry in entries_in_mailing:
			at_index = entry["Addr"].find("@")
			domain_name = entry["Addr"][at_index : ] # the domain name for each newly added email
			cursor.execute("SELECT * FROM daily WHERE Domain=?", [domain_name])
			data = cursor.fetchone()
			if data != None: # the domain has shown before
				cursor.execute("UPDATE daily SET CountDaily = CountDaily + 1, CountTotal = CountTotal + 1 WHERE Domain = ?", [domain_name]) # update daily count and total count
			else: # the domain has not shown until now
				cursor.execute("INSERT INTO daily (Domain, CountDaily, CountTotal, ThirtyDayCount) VALUES (?,?,?,?)", (domain_name, 1, 1, "")) # insert new entry

		cursor.execute("SELECT * FROM daily")
		entries_in_daily = cursor.fetchall()
		for entry in entries_in_daily:
			domain_name = entry["Domain"]
			# deal with the empty string created when first inserting the entry to daily table
			if entry['ThirtyDayCount'] == "" :
				thirty_day_count = []
			else:
				thirty_day_count = str(entry['ThirtyDayCount']).split(',')

			if len(thirty_day_count) == SORTING_PERIOD: # if there are 30 days count, add new daily count and pop the 30th count
				new_thirty_day_count = [str(entry['CountDaily'])] + thirty_day_count
				new_thirty_day_count.pop()
				new_thirty_day_count_str = ",".join(new_thirty_day_count)
				cursor.execute("UPDATE daily SET ThirtyDayCount = ? WHERE Domain = ?", (new_thirty_day_count_str, domain_name))
			else: # if the history is not 30 days long, just insert the new daily count to the queue
				new_thirty_day_count_str = ",".join([str(entry['CountDaily'])] + thirty_day_count)
				cursor.execute("UPDATE daily SET ThirtyDayCount = ? WHERE Domain = ?", (new_thirty_day_count_str, domain_name))
#---------------------------------------------------------------------------------------------------------
def get_top_50():
	connection = sqlite3.connect(DATABASE_FILE_NAME)
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	with connection:
		cursor.execute("SELECT * FROM daily ORDER BY CountTotal DESC LIMIT 50")
		return cursor.fetchall()
#---------------------------------------------------------------------------------------------------------
def sort_top_50(top_50): # sort based on past 30 days growth rate
	top_50_dict = {}
	for item in top_50:
		thirty_day_count = str(item['ThirtyDayCount']).split(',')
		thirty_day_count = map(int, thirty_day_count)
		top_50_dict[str(item['Domain'])] = sum(thirty_day_count) / float(item['CountTotal']) # 30 days count / total count
	return sorted(top_50_dict.items(), key=operator.itemgetter(1), reverse = True)
#---------------------------------------------------------------------------------------------------------
def report(report_date):
	update_daily_added_emails(report_date)
	top_50 = get_top_50()
	top_50_sorted = sort_top_50(top_50)
	for entry in top_50_sorted:
		print entry[0] + " | " + str(entry[1]*100) + '%'
#---------------------------------------------------------------------------------------------------------
def generate_email():
	domain_name = "@" + random.choice(LETTERS) + random.choice(LETTERS) + SUFFIX # 26^2 many domains
	email_addr = PREFIX + domain_name
	return email_addr
#---------------------------------------------------------------------------------------------------------
def simulate():
	start_date = datetime(2015,7,1)
	adding_date = start_date
	connection = sqlite3.connect(DATABASE_FILE_NAME)
	cursor = connection.cursor()
	with connection:
		cursor.execute("CREATE TABLE IF NOT EXISTS mailing(Addr TEXT, DateAdded TEXT)")
	for i in range(1, 41): # number of days to simulate
		number_of_daily_new_emails = 2000
		for j in range(1, number_of_daily_new_emails):
			with connection:
				# adding it to the mailing table
				cursor.execute("INSERT INTO mailing (Addr, DateAdded) VALUES (?,?)", (generate_email(), datetime.strftime(adding_date, "%Y-%m-%d")))
		timer_start = datetime.now()
		print "Day: " + str(i)
		report(adding_date)
		timer_end = datetime.now()
		# the timer can roughly show performance
		# print "report time cost: " + str(timer_end - timer_start) 
		adding_date += timedelta(days = 1) # go to the next day
#-------------------------------------------------main----------------------------------------------------
simulate()

