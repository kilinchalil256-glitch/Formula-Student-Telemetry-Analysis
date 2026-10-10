from pathlib import Path

class TelemetrySession:
    def __init__(self,time,speed,rpm,throttle,brake,temp):
        self.speed = speed 
        self.time = time 
        self.rpm = rpm 
        self.throttle = throttle 
        self.brake = brake 
        self.temp = temp 
    def getmaxspeed(self):
         return getmax(self.speed)
    def getavgspeed(self):
         return (round(getavg(self.speed),2))
    def getmaxrpm(self):
         return getmax(self.rpm)
    def getavgrpm(self):
         return(round(getavg(self.rpm),2))
    def getmaxtemp(self):
        return getmax(self.temp)
    def getavgtemp(self):
         return (round(getavg(self.temp),2))
    def calculate_acceleration(self):
        acceleration = []
        tempspeed = self.speed
        temptime = self.time
        for i in range (len(tempspeed)-1):
             currentacc = ((tempspeed[i+1]-tempspeed[i])/3.6)/(temptime[i+1]-temptime[i])
             acceleration.append(round(currentacc,2))
        return acceleration      
    def getmaxaccel(self):
         return getmax(self.calculate_acceleration())
    def getminaccel(self):
         return getmin(self.calculate_acceleration())
    def getsummary(self):
        print(f'========== TELEMETRY ANALYSIS ==========\n\n')
        print(f'GENERAL\n----------------------------------------\n')
        print(f'Total Measurements : {len(self.speed)}\n\n')
        print(f'SPEED\n----------------------------------------\n')
        print(f'Maximum Speed      : {self.getmaxspeed()} km/h\nAverage Speed      : {self.getavgspeed()} km/h\n\n')
        print(f'ENGINE\n----------------------------------------\n')
        print(f'Maximum RPM        : {self.getmaxrpm()}\nAverage RPM        : {self.getavgrpm()}\n\n')
        print(f'TEMPERATURE\n----------------------------------------\n')
        print(f'Maximum Temp       : {self.getmaxtemp()} °C\nAverage Temp       : {self.getavgtemp()} °C\n\n')
        print(f'ACCELERATİON\n----------------------------------------\n')
        print(f'Maximum Accel      : {self.getmaxaccel()} m/s²\nMaximum Decel      : {self.getminaccel()} m/s²\n\n========================================')

def append_data(a,b):
    for i in range(len(b)):
        b[i].append(float(a[i]))

def load_session(path):

    with open (path, 'r') as f:
        raw_data = f.readlines()

    time,speed,rpm,throttle,brake,temp = [],[],[],[],[],[]
    datatypes = [time,speed,rpm,throttle,brake,temp]

    all_datas = raw_data[1 :]
    for data in all_datas:
        cur_data = data.strip().split(',')
        append_data(cur_data,datatypes)

    return TelemetrySession(*datatypes)

def getmax(a):
        max_value = a[0]
        for data in a:
            if data>max_value:
                max_value = data
        return max_value
def getmin(a):
        max_value = a[0]
        for data in a:
            if data<max_value:
                max_value = data
        return max_value
def getavg(a):
        total = 0
        count = 0
        for data in a:
            total += data
            count += 1
        return (total/count)



path = Path(__file__).resolve().parent / "telemetry.csv"

session1 = load_session(path)
session1.getsummary()
