from celery.task.schedules import crontab
from celery import shared_task
from celery.decorators import periodic_task
from time import sleep
from scheduler.schedulerQueue import SchedulerQ
from scheduler.tweet import tweet_on_rotator_start
from scheduler.models import TLE, AzEl, NextPass, Mission
from random import randint
from scheduler.rotatorController import rotator_controller


schedulerQ = SchedulerQ()


from celery.signals import celeryd_init

@celeryd_init.connect
def configure_worker1(sender=None, conf=None, **kwargs):
    print("Init celery")


@shared_task()
def SchedulerThread():
	print ("Starting Scheduler") 
	try:
		mission_list = Mission.objects.filter(status="NEW")
	except Mission.DoesNotExist as e:
		print("No Missions")
		mission_list = None
	for i in mission_list:
		print(i.name)
	print("Exiting Scheduler")
	return mission_list
	
	


@shared_task()
def RotatorsThread(nextPass):
	print ("Starting Rotators") 
	arduinoRotator = rotator_controller(nextPass)
	while(1):
		tweet_on_rotator_start()
		arduinoRotator.sketchy_arduino_move()
		sleep(2)
	print("Exiting Rotators")


# @periodic_task(
# 	run_every=(crontab(minute='*/1')),
# 	name ="repeating_task",
# 	ignore_result=True)
@shared_task()
def repeatingTask():
	myId = randint(0, 10)
	print("Started task: " + str(myId))
	sleep(10)

	#tle = TLE.objects.all()
	#index = randint(0, len(tle))
	#print("Got TLE: " + tle[index].name)
	print("Ended task: " + str(myId))

@shared_task()
def setSchedulerQ(schedulerQueue):
	schedulerQ = schedulerQueue

@shared_task()
def getSchedulerQ():
	return schedulerQ
