import datetime

def update_time(self):
    current_time = datetime.datetime.now().strftime("%d-%m-%Y\n%H:%M:%S")
    self.date_time_label.config(text=current_time)
    self.after(1000, self.update_time)