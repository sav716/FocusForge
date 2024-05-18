import tkinter as tk
from tkinter import ttk

hosts_path = "C:/Windows/System32/drivers/etc/hosts"
redirect = "127.0.0.1"
blocked_sites = []
root = tk.Tk()
root.title("Focus Forge")
root.resizable(True, True)
root.attributes("-topmost", True)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
# create timer frame and place widgets in it
timer_frame = ttk.Frame()
timer_frame.grid(row=0, column=0, sticky="news")
timer_frame.rowconfigure((0,1), weight=1)
timer_frame.columnconfigure((0,1,2), weight=1)

minute_label = ttk.Label(timer_frame, justify='center', font=("Arial", 16))
colon_label = ttk.Label(timer_frame, text=":", justify='center', font=("Arial", 16))
second_label = ttk.Label(timer_frame, justify='center', font=("Arial", 16))
no_internet_label = ttk.Label(timer_frame, justify='center', font=("Arial", 40))
start_button = ttk.Button(timer_frame, text="Start Pomodoro", 
                          command=lambda: pomo_timer())


minute_label.grid(row=0, column=0, sticky="news")
colon_label.grid(row=0, column=1, sticky="news")
second_label.grid(row=0, column=2, sticky="news")
start_button.grid(row=1, column=0, columnspan=3, sticky="news")
no_internet_label.grid(row=2, column=0, columnspan=3, sticky="news")

# website blocker GUI
website_blocker_frame = ttk.Frame()
website_blocker_frame.grid(row=0, column=0, sticky="news")
block_entry = ttk.Entry(website_blocker_frame, )
block_button = ttk.Button(website_blocker_frame, 
                          command=lambda: block(block_entry.get()), text="Block Site")
unblockall_button = ttk.Button(website_blocker_frame, command=lambda: unblockall(), 
                               text="Unblock All Sites")
blocked_sites_label = ttk.Label(website_blocker_frame)

block_entry.grid(row=0, column=0, sticky="news", columnspan=2)
block_button.grid(row=1, column=0, sticky="news")
unblockall_button.grid(row=1, column=1, sticky="news")
blocked_sites_label.grid(row=2, column=0, columnspan=2, sticky="news")

website_blocker_frame.rowconfigure((0,1,2), weight=1)
website_blocker_frame.columnconfigure((0,1), weight=1)

# notebook for GUI
notebook = ttk.Notebook()
notebook.add(timer_frame, text="Pomodoro Timer")
notebook.add(website_blocker_frame, text="Website Blocker")
notebook.grid(row=0,column=0, sticky="news")

# show this authorization frame
timer_frame.tkraise()
website_blocker_frame.tkraise()

def pomo_timer():
  # time is in minutes
  time_elapsed = 0
  pomos_elapsed = 0
  num_pomos = 4
  pomo_length = 1
  short_break_length = 1
  long_break_length = 30
  current = 'work' # can be work, sbreak, or lbreak    
  def pomo(length):
    nonlocal time_elapsed
    if time_elapsed < length * 60:
        # schedule next update 1 second later
        time_elapsed += 1
        if second_label.cget('text') == "0":
          minute_label.configure(text=str(int(minute_label.cget('text')) - 1))
          second_label.configure(text="59")
          root.after(1000, pomo, length)
        else:
          second_label.configure(text=str(int(second_label.cget('text')) - 1))
          root.after(1000, pomo, length)
    else:
      nonlocal current, pomos_elapsed, num_pomos
      time_elapsed = 0
      if current == 'work':
        pomos_elapsed += 1
        root.attributes('-fullscreen', True)
        if pomos_elapsed == num_pomos:
          no_internet_label.configure(text='Go read a book, or take a walk!')
          current = 'lbreak'
          minute_label.configure(text=str(long_break_length), font=("Arial", 54)) 
          second_label.configure(text="0", font=("Arial", 54))
          colon_label.configure(font=("Arial", 54))
          root.after(1000, pomo, long_break_length)
        else:
          no_internet_label.configure(text='Go read a book!')
          current = 'sbreak'
          minute_label.configure(text=str(short_break_length), font=("Arial", 54)) 
          second_label.configure(text="0", font=("Arial", 54))
          colon_label.configure(font=("Arial", 54))
          root.after(1000, pomo, short_break_length)

      elif current == 'sbreak':
        current = 'work'
        root.attributes('-fullscreen', False)
        no_internet_label.configure(text='')
        minute_label.configure(text=str(pomo_length), font=("Arial", 16))
        colon_label.configure(font=("Arial", 16))
        second_label.configure(text="0", font=("Arial", 16))
        root.after(1000, pomo, pomo_length)
        
      else:
        minute_label.configure(text="") 
        second_label.configure(text="")
        no_internet_label.configure(text="")
        start_button.grid()
        root.attributes('-fullscreen', False)
        

  start_button.grid_remove()
  minute_label.configure(text=str(pomo_length)) 
  second_label.configure(text="0")
  pomo(pomo_length)

def block(site):
  if site not in blocked_sites:
    blocked_sites.append(site)
  with open(hosts_path, 'r+') as file:
    content = file.read()
    for website in blocked_sites:
        if website in content:
            pass
        else:
            file.write(redirect + " " + website + "\n")
  blocked_sites_label.configure(text="\n".join(blocked_sites))

def unblockall():
  global blocked_sites
  with open(hosts_path, 'r+') as file:
      content = file.readlines()
      file.seek(0)
      for line in content:
          if not any(website in line for website in blocked_sites):
              file.write(line)
      file.truncate()

  blocked_sites = []
  blocked_sites_label.configure(text="")
  
root.mainloop()
