from pathlib import Path

class TelemetrySession:
    def __init__(self,time,speed,rpm,throttle,brake,temp):
        self.speed = speed 
        self.time = time 
        self.rpm = rpm 
        self.throttle = throttle 
        self.brake = brake 
        self.temp = temp 
    def get_max_speed(self):
         return getmax(self.speed)
    def get_avg_speed(self):
         return getavg(self.speed)
    def get_max_rpm(self):
         return getmax(self.rpm)
    def get_avg_rpm(self):
         return getavg(self.rpm)
    def get_max_temp(self):
        return getmax(self.temp)
    def get_avg_temp(self):
         return getavg(self.temp)
    def calculate_acceleration(self):
        accelerations = []

        for i in range(len(self.speed) - 1):
            delta_speed = (self.speed[i + 1] - self.speed[i]) / 3.6
            delta_time = self.time[i + 1] - self.time[i]

            acceleration = delta_speed / delta_time

            accelerations.append(acceleration)

        return accelerations      
    def get_max_accel(self):
         return getmax(self.calculate_acceleration())
    def get_min_accel(self):
         return getmin(self.calculate_acceleration())
    def get_summary(self):
        print("========== TELEMETRY ANALYSIS ==========")
        print()

        # GENERAL
        print("GENERAL")
        print("-" * 40)
        print(f"Total Measurements    : {len(self.speed)}")
        print()

        # SPEED
        print("SPEED")
        print("-" * 40)
        print(f"Maximum Speed         : {self.get_max_speed():.2f} km/h")
        print(f"Average Speed         : {self.get_avg_speed():.2f} km/h")
        print()

        # ENGINE
        print("ENGINE")
        print("-" * 40)
        print(f"Maximum RPM           : {self.get_max_rpm():.2f}")
        print(f"Average RPM           : {self.get_avg_rpm():.2f}")
        print()

        # TEMPERATURE
        print("TEMPERATURE")
        print("-" * 40)
        print(f"Maximum Temperature   : {self.get_max_temp():.2f} °C")
        print(f"Average Temperature   : {self.get_avg_temp():.2f} °C")
        print()

        # ACCELERATION
        print("ACCELERATION")
        print("-" * 40)
        print(f"Maximum Acceleration  : {self.get_max_accel():.2f} m/s²")
        print(f"Maximum Deceleration  : {self.get_min_accel():.2f} m/s²")
        print()

        # BRAKING ANALYSIS
        print("BRAKING ANALYSIS")
        print("-" * 40)
        print(f"Braking Measurements  : {len(self.detect_braking())}")
        print(f"Maximum Brake Decel   : {self.get_peak_braking_deceleration():.2f} m/s²")
        print(f"Throttle-Brake Overlap: {len(self.detect_overlap())}")
        print()

        print("=" * 40)

        
    def detect_braking(self):
        output = []
        for i,value in enumerate(self.brake):
            if value != 0:
                 output.append(i)
        return output           
    def brake_deccel(self):
        output = []
        accelerations = self.calculate_acceleration()

        for i in self.detect_braking():
            if i > 0:
                output.append(accelerations[i-1])

        return output
    def get_peak_braking_deceleration(self):
         return getmin(self.brake_deccel())
    def detect_overlap(self):
        index = []
        for i,(b,t) in enumerate(zip(self.brake,self.throttle)):
            if b!=0 and t!=0:
                index.append(i)
        return index

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
session1.get_summary()
