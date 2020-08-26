import urllib.request
import random
import re
import os
import datetime as dt
import time


def urlGrabber(theDay, address):	
	site = address + "/" + str(theDay.year) + "/" + str(theDay.month).zfill(2) + "/" + str(theDay.day).zfill(2) + ""

	page = urllib.request.urlopen(site).read().decode('utf-8')
	img = re.findall(r'https://assets.amuniversal.com/\w*', page)[0]

	return img

def downloader(iter, address, target):	
	
	imgUrl = urlGrabber(iter, address)

	comicName = os.path.basename(target)
	
	imgName = str(iter.year) + "-" + str(iter.month).zfill(2) + "-" + str(iter.day).zfill(2) + " - " + comicName + ".png"
	
	urllib.request.urlretrieve(imgUrl, target+"/"+str(iter.year)+"/"+ str(iter.month).zfill(2) +"/"+ imgName)


def organize(first , last, target):	
	inc = dt.timedelta(weeks=4)

	ind = first	
	while ind < last:
		folder = target+"/"+str(ind.year)+"/"+str(ind.month).zfill(2)+"/"
		os.makedirs(os.path.dirname(folder), exist_ok=True)
		ind += inc

	folder = target+"/"+str(last.year)+"/"+str(last.month).zfill(2)+"/"
	os.makedirs(os.path.dirname(folder), exist_ok=True)

def validate(date01):
	try:
		dt.datetime.strptime(date01, '%m/%d/%Y')
	except ValueError:
		print("This is the incorrect date format. It should be MM/DD/YYYY.\n")
		return False
	
	return True

def valisite(site01):
	try:
		urllib.request.urlopen(site01).read().decode('utf-8')
	except ValueError:
		print("Please enter a valid GoComics address.\n")
		return False

	return True

def flip(target):
	return target.replace("\\","/")
	
def main():

	source = input("GoComics address : ")
	while not valisite(source):
		source = input("GoComics address : ")

	location = input("\nDownload target location : ")
	location = flip(location)

	startStr = input("\nStart date (MM/DD/YYYY) :  ")
	while not validate(startStr):
		startStr = input("\nStart date (MM/DD/YYYY) :  ")
	start = dt.datetime.strptime(startStr, '%m/%d/%Y')

	endStr = input("End date (MM/DD/YYYY) :  ")
	while not validate(endStr):
		endStr = input("End date (MM/DD/YYYY) :  ")
	end = dt.datetime.strptime(endStr, '%m/%d/%Y')

	#start_time = time.time()

	day = dt.timedelta(days=1)

	organize(start, end, location)

	iter = start
	while iter <= end:    
		downloader(iter, source, location)
		iter += day

	#print("\nMy program took %.2f seconds to run\n" %(time.time() - start_time))
	input("Press ENTER to continue.")

main()