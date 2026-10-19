import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TelemetrySession:
    def __init__(self,df):
        self.df = df
    def get_max_speed(self):
         return self.df['speed_kmh'].max()
    def get_avg_speed(self):
         return self.df['speed_kmh'].mean()
    def get_max_rpm(self):
         return self.df['rpm'].max()
    def get_avg_rpm(self):
         return self.df['rpm'].mean()
    def get_max_temp(self):
        return self.df['temp_c'].max()
    def get_avg_temp(self):
         return self.df['temp_c'].mean()
    def calculate_acceleration(self):
        #get speed difference
        speed_array = self.df['speed_kmh'].to_numpy()
        speed_diff = np.diff(speed_array)
        #convert speed to the right metric
        speed_diff = (speed_diff/3.6)
        #get time difference
        time_array = self.df['time_s'].to_numpy()
        time_diff = np.diff(time_array)

        #calculate acceleration
        accel = (speed_diff/time_diff)
        return accel

    def get_max_accel(self):
         return self.calculate_acceleration().max()
    def get_min_accel(self):
         return self.calculate_acceleration().min()
    def get_summary(self):
        print("========== TELEMETRY ANALYSIS ==========")
        print()

        # GENERAL
        print("GENERAL")
        print("-" * 40)
        print(f"Total Measurements    : {len(self.df['speed_kmh'])}")
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
        if self.get_peak_braking_deceleration() is None:
             print(f"Maximum Brake Decel   : N/A")
        else:
             print(f"Maximum Brake Decel   : {self.get_peak_braking_deceleration():.2f} m/s²")
        print(f"Throttle-Brake Overlap: {len(self.detect_overlap())}")
        print()

        print("=" * 40)

        
    def detect_braking(self):
        braking_mask = self.df['brake_pct']>0
        return np.flatnonzero(braking_mask)           
    def braking_accelerations(self):
        accelerations = self.calculate_acceleration()
        braking_mask = self.df['brake_pct'].to_numpy()[1:] > 0
        return accelerations[braking_mask]
        
    def get_peak_braking_deceleration(self):
         accelerations = self.braking_accelerations()
         decelerations = accelerations[accelerations < 0]
         if decelerations.size > 0:
            return decelerations.min()
        
         return None
    def detect_overlap(self):
        mask =  ((self.df['brake_pct']>0)
                &(self.df['throttle_pct']>0)
                )
        return np.flatnonzero(mask)       
    def validate_data(self):
        if self.df.empty:
             raise ValueError("Empty Telemetry Data")
        if (self.df['speed_kmh'] < 0).any():
             raise ValueError("Negative Speed Detected")     
        if ((self.df['time_s']).diff()<=0).any():
             raise ValueError("Invalid Timestamps")     
        if len(self.df['speed_kmh'])<2:
             raise ValueError("At least two measurements are required")
        if self.df.isna().any().any():
             raise ValueError("Missing Telemetry Data")

    def export_report(self,path):
         with open(path,"w",newline="") as file:
              writer = csv.writer(file)
              writer.writerow(["Metric","Value","Unit"])
              writer.writerow(["Maximum Speed",self.get_max_speed(),"km/h"])
              writer.writerow(["Average Speed",round(self.get_avg_speed(),2),"km/h"])
              writer.writerow(["Maximum Rpm",self.get_max_rpm(),"rpm"])
              writer.writerow(["Average Rpm",round(self.get_avg_rpm(),2),"rpm"])
              writer.writerow(["Maximum Temperature",self.get_max_temp(),"°C"])
              writer.writerow(["Average Temperature",round(self.get_avg_temp(),2),"°C"])
              writer.writerow(["Maximum Acceleration",round(self.get_max_accel(),2),"m/s²"])
              writer.writerow(["Maximum Deceleration",round(self.get_min_accel(),2),"m/s²"])
              writer.writerow(["Braking Measurements",len(self.detect_braking()),"count"])
              if self.get_peak_braking_deceleration() is None:
                   writer.writerow(["Peak Braking Deceleration","N/A","m/s²"])
              else:
                   writer.writerow(["Peak Braking Deceleration",round(self.get_peak_braking_deceleration(),2),"m/s²"])
              
              writer.writerow(["Throttle-Brake Overlap",len(self.detect_overlap()),"count"])

    def plot_dashboard(self):
         fig, ax = plt.subplots(2,2,figsize =(12,8))
         time = self.df['time_s']
         #speed graph
         ax[0,0].plot(time,self.df['speed_kmh'],'b')
         ax[0,0].set_title('Vehicle Speed (km/h)')
         ax[0,0].set_xlabel('Time')
         ax[0,0].set_ylabel('Speed')
         #rpm graph
         ax[0,1].plot(time,self.df['rpm'],'k')
         ax[0,1].set_title('Engine Speed (RPM)')
         ax[0,1].set_xlabel('Time')
         ax[0,1].set_ylabel('Rpm')
         #acceleration graph
         ax[1,0].plot(time.iloc[1:],self.calculate_acceleration(),'g')
         ax[1,0].set_title('Vehicle Acceleration (m/s²)')
         ax[1,0].set_xlabel('Time')
         ax[1,0].set_ylabel('Acceleration')
         #temperature graph
         ax[1,1].plot(time,self.df['temp_c'],'r')
         ax[1,1].set_title('Engine Temperature (°C)')
         ax[1,1].set_xlabel('Time')
         ax[1,1].set_ylabel('Temperature')

         for axis in ax.flat:
              axis.grid(True)
              axis.set_xlim(600,700)
         
         
         fig.tight_layout()
         fig.savefig("telemetry_dashboard.png", dpi=150)
         plt.show()

def load_session_pandas(file_path):
    telemetry_data = pd.read_csv(file_path)
    session = TelemetrySession(telemetry_data)
    return session




session1 = load_session_pandas("telemetry_endurance_60min.csv")
session1.validate_data()
session1.get_summary()
session1.export_report('report.csv')
session1.plot_dashboard()