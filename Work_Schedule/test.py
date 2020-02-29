from datetime import datetime

date = "02/24"
start = "12:15a"
end = "10:15a"
year = "2020"

def apTo24Hour(time):
    #if a time does not have 4 digits add a zero to front
    if len(time)<6:
        time = "0"+time
    #if hour is midnight (which it won't be) hour is 00
    if(time[-1:] == 'a' and time[:2]=="12"):
        return "00"+time[2:-1]
    #remove am and leave as is
    elif(time[-1] == 'a'):
        return time[:-1]
    #check if noon
    elif(time[-1]=='p' and time[:2] =="12"):
        return time[:-1]
    #otherwise add 12 hours and remove pm
    else:
        return str(int(time[:(time.find(':'))])+12) + time[time.find(':'):-1]
    
def makeISO8601(date,time,year="2020"):
    time = apTo24Hour(time)
    iso = year+'-'+date[:2]+'-'+date[3:]+'T'+time[:2]+':'+time[3:]+':'+"00"
    return iso

print(makeISO8601(date,start))
target = "2018-12-24T00:00:00+01:00"


