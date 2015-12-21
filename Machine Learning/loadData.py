#!/usr/bin/python
import sqlite3
import linecache

DATABASE_FILE_NAME = "train.db"



def main():
	option = raw_input("Do you want to load training data into train.db? (yes/no) ")
	if option == "yes":
		load_train_data()
		load_train_label()
		load_words()

#----------------------------------------------------------main-------------------------------------------------------#
