import time,datetime
import asyncio
from datetime import datetime
import re



def delta_time_from_now(hour,date=None):
    def add_date_to_hour(hour,date):
        hour=datetime.strptime(hour,'%H:%M:%S.%f')
        target=hour.replace(year=date.year,month=date.month,day=date.day)
        
        return target

    def format_in_milisec(format):
        if len(re.findall(r"\d{1,2}:\d{1,2}:\d{1,2}", format))<1:
            return format+":00.00"
        if len(re.findall(r"\.[0-9]+$", format)) < 1:
            return format+".00"
        return  format

    def is_contain_hour(format):
        return len(re.findall(r"[0-9]{1,2}:[0-9]{1,2}(:\d{1,2}(\.\d+)?)?", format))>0 

    def is_contain_date(format):
        return len(re.findall(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]+", format))>0
    
    now=time.time()
    hour=format_in_milisec(hour)
    if is_contain_date(hour):
        
        date_time_obj = datetime.strptime(hour,
                            '%d/%m/%Y %H:%M:%S.%f')
        target = date_time_obj.timestamp() 

    else:
        if type(date) == str:
            date=datetime.strptime(date,'%d/%m/%Y')
        
        date_time_obj=add_date_to_hour(hour,date)
 
        target = date_time_obj.timestamp()
    
    
    return target-now

    



class Schedule:
    def __init__(self):
        self.tasks=[]

    async def __to_do_after(self,fnc,delay):
        await asyncio.sleep(delay)
        await fnc

    def add_event(self,task,hour,date=None,name=None):
        delay=delta_time_from_now(hour,date)
        self.tasks.append(self.__to_do_after(task,delay))
    def start(self ):
        async def main():
            concurrent_tasks=[]
            for task in self.tasks:
                concurrent_tasks.append(asyncio.create_task(task))
            for task in concurrent_tasks:
                await task
            
        asyncio.run(main())

async def say_after(what):
    print(what)
    

async def to_do_after(task,delay):
        await asyncio.sleep(delay)
        await task

async def main():
    
    task1 = asyncio.create_task(to_do_after(say_after("2"),2))
    task2 = asyncio.create_task(to_do_after(say_after("3"),3))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task2
    await task1

    print(f"finished at {time.strftime('%X')}")


if  __name__=="__main__":
    schedule=Schedule()
    schedule.add_event(task=say_after("badr"),hour="00:19:50",date=datetime.now())
    schedule.add_event(task=say_after("badr2"),hour="00:19:55",date="17/07/2021")
    schedule.start()