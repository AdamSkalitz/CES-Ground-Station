#!usr/bin/env python  
from datetime import date, datetime, timedelta

class satellite(object):
	name=""
	AOS=None
	LOS=None

	def __init__(self,name,AOS,LOS):
		self.name = name
		self.AOS = AOS
		self.LOS = LOS

	def __str__(self):
		return self.name

	def __repr__(self):
		return str(self)

#class FitnessFunction():
		
def fitnessFunction(satList):

	satListConflictGroups = findConflictingGroups(satList)

	print(" unmerged conflict groups")
	print(satListConflictGroups)

	mergedGroups = mergeLists(satListConflictGroups)
	
	print ("mergedGroups")
	print(mergedGroups)

	reorderedConflictGroups=[]
	for group in mergedGroups:
		#print("sdfsd")
		reordered= [x for x in satList if x in group]
		reorderedConflictGroups.append(reordered)

	print("conflict groups")
	print(reorderedConflictGroups)

	nextPass = findSchedulableSatellites(reorderedConflictGroups)

	return nextPass

def findConflictingGroups(satList):
	satListConflicts=[]
	for i in range(len(satList)):
		conflicts=[]
		for j in range(i+1, len(satList)):
			if satList[i].AOS <= satList[j].LOS and satList[i].LOS >= satList[j].AOS:
				#they conflict
				#print('{} conflicts with {}'.format(satList[i],satList[j]))
				if satList[i] and satList[j] not in conflicts:
					conflicts.append(satList[i])
					conflicts.append(satList[j])

		if len(conflicts)>0:
			satListConflicts.append(list(set(conflicts)))

	#print(satListConflicts) 
	#blah = mergeLists(satListConflicts)

	return satListConflicts

def mergeLists(satListConflicts):
	#def finalListConflicts():
	#what happens if 2nd list is bigger than the first
	# satListConflicts = [['sat1', 'sat4', 'sat2', 'sat6'], ['sat6', 'sat7', 'sat4', 'sat2', 'sat5'],
	# 				   ['sat3', 'sat11', 'sat10'], ['sat6', 'sat7', 'sat4'], ['sat6', 'sat7'], ['sat9', 'sat8'],
	# 				   ['sat11', 'sat10']]
	# satListConflicts = [['sat2', 'sat1', 'sat6', 'sat7', 'sat8', 'sat9', 'sat4'], 
	# 					['sat2', 'sat6', 'sat7', 'sat5', 'sat8', 'sat9', 'sat4'], 
	# 					['sat11', 'sat3', 'sat10'], ['sat8', 'sat6', 'sat7', 'sat9', 'sat4'], 
	# 					['sat7', 'sat8', 'sat9', 'sat6'], ['sat8', 'sat9', 'sat7'], 
	# 					['sat8', 'sat9'], ['sat11', 'sat10']]
	#print(satListConflictssatListConflicts)
	finaListsConflicts = []
	finaListsConflictsTrimmed=[]
	for i in range(len(satListConflicts) - 1):
		subList = satListConflicts[i]
		#c2 = satListConflicts
		#c3 = [list(filter(lambda x: x in c1, sublist)) for sublist in c2]
		#function = lambda x: x in c1
		#iterable = satListConflicts[j] (list)
		c3 = [list(filter(lambda x: x in subList, satListConflicts[subListIndex])) for subListIndex in range(len(satListConflicts))]
		#return an iterator from the elements of iterable where function return true
		#http://stackoverflow.com/questions/642763/python-intersection-of-two-lists
		
		#print("if c3  {} is in {}".format(c3,subList))
		c4 = []
		# print(c1)
		# print(c2)
		# print(c3)
		# #print(c4)
		for z in range(len(c3)):
			if (c3[z] != []):
				c4 = list(set(satListConflicts[z]) | set(subList))
		#        print('{} | {} = {}'.format(list(set(satListConflicts[z])),set(subList),c4))
				subList = c4
		#print(c1)
		#print("FInalproduct {}".format(subList))
		finaListsConflicts.append(subList)


	for i in finaListsConflicts:
		if i not in finaListsConflictsTrimmed:
			finaListsConflictsTrimmed.append(i)

	#print(finaListsConflictsTrimmed)
	return finaListsConflictsTrimmed

def findSchedulableSatellites(satListConflictGroups):

	transactionTime = timedelta(minutes=3)
	nextPassList = []
	unScheduledSats = []
	for group in satListConflictGroups:
		passes=0
		blackList=[]
		scheduledSats=[]
		unScheduledSatFromGroup = []
		for sat in group:
			#print(sat.name)
			conflicts=False
			thisSatPassStart = 0
			thisSatPassEnd = 0
			for time in blackList:
				if sat.AOS <= time[1] and sat.LOS >= time[0]:
					#print('{} conflicts with {} {}'.format(sat.name,time[0],time[1]))
				#sat conflicts with one of the times in blackList
					#in i=1 sat is sat2 and blacklist is sat 1
					endGap = sat.LOS - (time[0]+transactionTime)
					if endGap<timedelta(0):
						endGap = endGap*-1
					frontGap = time[0] - sat.AOS
					if frontGap<timedelta(0):
						frontGap = frontGap*-1

					#if frontGap and endGap both >= tt and we can
					#fit in either, pick one at random
					if endGap>=transactionTime:
						#can be fit in end gap
						#fit in some random place in end gap
						#print("fit in end gap")

						thisSatPassStart = sat.LOS-transactionTime
						thisSatPassEnd = sat.LOS
						conflicts=False
					elif frontGap >= transactionTime:
						#can be fit in start gap
						#fit in some random place in front gap
						#print("fit in front gap")
						conflicts=False
						thisSatPassStart = sat.AOS
						thisSatPassEnd = sat.AOS + transactionTime
					else:
						#can't fit in and we need another pass
						passes+=1
						#print("adding")
						#unScheduledSats.append(sat.name)
						conflicts=True
						break

				else:
					thisSatPassStart = sat.AOS
					thisSatPassEnd = sat.AOS + transactionTime
					conflicts=False

			if len(blackList)==0:
				#print(sat.name)
				thisSatPassStart=sat.AOS
				thisSatPassEnd = sat.AOS + transactionTime
			if conflicts is False:
				#Sat doesn't conflict with any times made so far
				tempTime = [thisSatPassStart,thisSatPassEnd]

				if tempTime not in blackList:
					scheduledSats.append(sat)
					blackList.append(tempTime)	
		
		unScheduledSatFromGroup = [sat for sat in group if sat not in scheduledSats]
		unScheduledSats.append(unScheduledSatFromGroup)
		nextPassList.append(scheduledSats)

	print("nextpasslist")
	print(nextPassList)
	print("unScheduledSats")
	print(unScheduledSats)
	score=0
	for satList in unScheduledSats:
		score +=len(satList)
	print(score) # want lowest0.
	return nextPassList

def test_findSchedulableSatellites_many_sats():


	catAOS = datetime(2017,1,25,0,52,59)
	catLOS = datetime(2017,1,25,1,04,28)
	sixtysevenCAOS = datetime(2017,1,25,0,6,52)
	sixtysevenCLOS = datetime(2017,1,25,0,14,42)
	sixtysevenDAOS = datetime(2017,1,25,0,8,37)
	sixtysevenDLOS = datetime(2017,1,25,0,16,18)
	aistAOS = datetime(2017,1,25,0,35,21)
	aistLOS = datetime(2017,1,25,0,48,8)
	beesatAOS = datetime(2017,1,25,0,46,48)
	beesatLOS = datetime(2017,1,25,1,0,4) 
	briteAOS = datetime(2017,1,25,0,19,39)
	briteLOS = datetime(2017,1,25,0,30,4)
	cubebugAOS = datetime(2017,1,25,0,41,54)
	cubebugLOS = datetime(2017,1,25,0,52,49)
	sailAOS = datetime(2017,1,25,0,41,17)
	sailLOS = datetime(2017,1,25,0,53,28)
	eagleAOS = datetime(2017,1,25,0,53,13)
	eagleLOS = datetime(2017,1,25,1,2,56)	
	exoAOS = datetime(2017,1,25,0,57,27)
	exoLOS = datetime(2017,1,25,1,05,27)
	fconeAOS = datetime(2017,1,25,0,17,14)
	fconeLOS = datetime(2017,1,25,0,30,6)
	fcthreeAOS = datetime(2017,1,25,0,11,3)
	fcthreeLOS = datetime(2017,1,25,0,23,54)
	fcfiveAOS = datetime(2017,1,25,0,8,47)
	fcfiveLOS = datetime(2017,1,25,0,21,37)
	fceightAOS = datetime(2017,1,25,0,52,35)
	fceightLOS = datetime(2017,1,25,1,5,21)
	fcnineAOS = datetime(2017,1,25,0,50,43)
	fcnineLOS = datetime(2017,1,25,1,3,31)
	fctenAOS = datetime(2017,1,25,0,53,57)
	fctenLOS = datetime(2017,1,25,1,6,40)
	fcelevenAOS = datetime(2017,1,25,0,59,45)
	fcelevenLOS = datetime(2017,1,25,1,12,25)	
	fethirteenAOS = datetime(2017,1,25,1,7,32)
	fethirteenLOS = datetime(2017,1,25,1,15,6)	
	fefourteenAOS = datetime(2017,1,25,0,0,33)
	fefourteenLOS = datetime(2017,1,25,0,8,13)	
	itupAOS = datetime(2017,1,25,0,22,12)
	itupLOS = datetime(2017,1,25,0,34,49)	

	#09 

	cat = satellite("cat",catAOS, catLOS)
	sixtysevenC = satellite("sixtysevenC",sixtysevenCAOS, sixtysevenCLOS)
	sixtysevenD = satellite("sixtysevenD",sixtysevenDAOS, sixtysevenDLOS)
	aist = satellite("aist",aistAOS, aistLOS)
	beesat = satellite("beesat",beesatAOS, beesatLOS)
	brite = satellite("brite",briteAOS, briteLOS)
	cubebug = satellite("cubebug",cubebugAOS, cubebugLOS)
	sail = satellite("sail",sailAOS, sailLOS)
	eagle = satellite("eagle",eagleAOS, eagleLOS)
	exo = satellite("exo",exoAOS,exoLOS)
	fcone = satellite("fcone",fconeAOS,fconeLOS)
	fcthree = satellite("fcthree",fcthreeAOS, fcthreeLOS)
	fcfive = satellite("fcfive",fcfiveAOS, fcfiveLOS)
	fceight = satellite("fceight",fceightAOS,fceightLOS)
	fcnine = satellite("fcnine",fcnineAOS,fcnineLOS)
	fcten = satellite("fcten",fctenAOS, fctenLOS)
	fceleven = satellite("fceleven",fcelevenAOS, fcelevenLOS)
	fethirteen = satellite("fethirteen",fethirteenAOS,fethirteenLOS)
	fefourteen = satellite("fefourteen",fefourteenAOS,fefourteenLOS)
	itup = satellite("itup",itupAOS, itupLOS)




	#satList=[sat1,sat2,sat3,sat5]
	satList=[cat,sixtysevenC,sixtysevenD,aist,beesat,brite,cubebug,sail,eagle,
	exo,fcone,fcthree,fcfive,fcfive,fceight,fcnine,fcten,fceleven,fethirteen,fefourteen,
	itup]
		#self.assertIs(shouldBe == ,)


	fitnessFunction(satList)

# clas = fit.FitnessFunction()
# clas.test_findSchedulableSatellites_many_sats()

test_findSchedulableSatellites_many_sats()

# sat1AOS = datetime(2017,1,25,12,2,0)
# sat1LOS = datetime(2017,1,25,12,5,0)
# sat2AOS = datetime(2017,1,25,12,0,0)
# sat2LOS = datetime(2017,1,25,12,8,0)
# sat3AOS = datetime(2017,1,25,12,25,0)
# sat3LOS = datetime(2017,1,25,12,30,0)
# sat4AOS = datetime(2017,1,25,11,57,0)
# sat4LOS = datetime(2017,1,25,12,3,0)
# sat5AOS = datetime(2017,1,25,12,7,0)
# sat5LOS = datetime(2017,1,25,12,10,0)
# sat6AOS = datetime(2017,1,25,11,57,0)
# sat6LOS = datetime(2017,1,25,12,4,0)
# sat7AOS = datetime(2017,1,25,11,57,0)
# sat7LOS = datetime(2017,1,25,12,4,0)
# sat8AOS = datetime(2017,1,25,11,57,0)
# sat8LOS = datetime(2017,1,25,12,4,0)
# sat9AOS = datetime(2017,1,25,13,0,0)
# sat9LOS = datetime(2017,1,25,13,4,0)
# sat10AOS = datetime(2017,1,25,12,27,0)
# sat10LOS = datetime(2017,1,25,12,31,0)
# sat11AOS = datetime(2017,1,25,12,28,0)
# sat11LOS = datetime(2017,1,25,12,34,0)

# sat1AOS = datetime(2017,1,25,12,2,0)
# sat1LOS = datetime(2017,1,25,12,5,0)
# sat2AOS = datetime(2017,1,25,12,0,0)
# sat2LOS = datetime(2017,1,25,12,8,0)
# sat3AOS = datetime(2017,1,25,12,25,0)
# sat3LOS = datetime(2017,1,25,12,30,0)
# sat4AOS = datetime(2017,1,25,11,57,0)
# sat4LOS = datetime(2017,1,25,12,3,0)
# sat5AOS = datetime(2017,1,25,12,7,0)
# sat5LOS = datetime(2017,1,25,12,10,0)
# sat6AOS = datetime(2017,1,25,11,57,0)
# sat6LOS = datetime(2017,1,25,12,4,0)
# sat7AOS = datetime(2017,1,25,11,57,0)
# sat7LOS = datetime(2017,1,25,12,4,0)
# sat8AOS = datetime(2017,1,25,12,59,0)
# sat8LOS = datetime(2017,1,25,13,3,0)
# sat9AOS = datetime(2017,1,25,13,0,0)
# sat9LOS = datetime(2017,1,25,13,4,0)
# sat10AOS = datetime(2017,1,25,12,27,0)
# sat10LOS = datetime(2017,1,25,12,31,0)
# sat11AOS = datetime(2017,1,25,12,28,0)
# sat11LOS = datetime(2017,1,25,12,34,0)

# sat1 = satellite("sat1",sat1AOS, sat1LOS)
# sat2 = satellite("sat2",sat2AOS, sat2LOS)
# sat3 = satellite("sat3",sat3AOS, sat3LOS)
# sat4 = satellite("sat4",sat4AOS, sat4LOS)
# sat5 = satellite("sat5",sat5AOS, sat5LOS)
# sat6 = satellite("sat6",sat6AOS, sat6LOS)
# sat7 = satellite("sat7",sat7AOS, sat7LOS)
# sat8 = satellite("sat8",sat8AOS, sat8LOS)
# sat9 = satellite("sat9",sat9AOS, sat9LOS)
# sat10 = satellite("sat10",sat10AOS,sat10LOS)
# sat11 = satellite("sat11",sat11AOS,sat11LOS)

# #satList=[sat1,sat2,sat3,sat5]
# satList=[sat1,sat2,sat3,sat4,sat5,sat6,sat7,sat8,sat9,sat10,sat11]

# #satListConflictGroups =  [satList,[sat8]]
# satListConflictsGroup = findConflictingGroups(satList)#findConflictingSats(sat1,satList)


# reorderedConflictGroups=[]
# for group in satListConflictsGroup:
# 	#print("sdfsd")
# 	reordered= [x for x in satList if x in group]
# 	reorderedConflictGroups.append(reordered)
# 	#print(reordered)

# print(reorderedConflictGroups)
# findSchedulableSatellites(reorderedConflictGroups)





list2=[2,3]
list1=[3,2]

if list1 in list2:
	?
