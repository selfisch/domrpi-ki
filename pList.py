import csv
import os.path
import sys

class pList:
	def __init__(self):
		self.path = os.path.dirname(os.path.realpath(__file__))
		self.pList = self.readList()

	def readList(self):
		with open(self.path + '/pList.csv', mode='r') as infile:
			reader = csv.reader(infile)
			cardList = {rows[0]:rows[1] for rows in reader}
			infile.close()
		return pList

	def getPlaylist(self,plist_id):
		self.pList = self.readList()
		try:
			return self.pList[plist_id]
		except:
			print 'ID %s is not plist' % plist_id
			return ''

	def addPlaylist(self, plist_id, plist_uri):
		try:
			if plist_id not in self.pList.keys():
				f = open(self.path + '/pList.csv', 'a')
				f.write(plist_id + ',' + plist_uri + '\n')
				self.pList[plist_id] = plist
			else:
				print 'ID %s is already used' % plist_id
		except:
			print 'Could not write file'
			if not os.path.isfile(self.path + '/pList.csv'):
				print 'File pList.csv does not exist'
				print 'lege Datei an'
				os.system("touch pList.csv")
