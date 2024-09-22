import os

if os.name == 'nt':  # Windows
    import threading
    import time
    from time import sleep
    from msvcrt import kbhit
    import pywinusb.hid as hid
    
elif os.name == 'posix':  # Unix/Linux/Mac
    import module_unix as my_module
else:
    raise ImportError("Unsupported operating system")


class Controller:
    def __init__(self, controller_name="",vid="",pid=""):
        if os.name == 'nt':  # Windows
            self.connector = WinController(controller_name,vid,pid)#WinController(controller_name="",vid="",pid="") 
        elif os.name == 'posix':  # Unix/Linux/Mac
            print("TODO")
    
    def init(self,name,vid,pid):
        self.connector.init(name,vid,pid)
    
    def get_devices(self):
        return self.connector.get_devices()
        
    def connect(self):
        self.connector.connect()
    
    def _read_data(self):
        self.connector._read_data()

    def sample_handler(self,data):
        self.connector.sample_handler(data)

    def get_data(self,index):
        return self.connector.get_data(index)

    def get_raw_data(self):
        return self.connector.get_raw_data()

    def data_available(self):
        return self.connector.data_available()
    
    def close(self):
        self.connector.close()
        
    def extract_vid_pid(self,hid_list,_vid,_pid):
        self.connector.extract_vid_pid(hid_list,_vid,_pid)

class WinController:
    def __init__(self, controller_name,vid="asd",pid=""):
        # Speichert den Controller in einem Dictionary
        self.controller_info = {
            'name': controller_name,
            'connected': False,
            'vid': vid,        
            'pid': pid,    
            'hid_device': None,  
            'hid_list': None,              
            'lpad_h':None,
            'data_available':None,
            'raw_data':None,            
            'flag':None,                
        }
        self._stop_thread = False
        self._thread = None
        #print("Info: ",self.controller_info)

    def init(self,name,vid,pid):
        self.controller_info['name'] = name
        self.controller_info['vid'] = vid
        self.controller_info['pid'] = pid
    
    def get_devices(self):     
        self.controller_info["hid_list"] = hid.find_all_hid_devices()
        return self.controller_info["hid_list"] 
        
    def connect(self):
        self.controller_info["hid_device"] = self.extract_vid_pid(self.get_devices(),self.controller_info["vid"],self.controller_info["pid"])
        self.controller_info['connected'] = True
        self._stop_thread = False
        self._thread = threading.Thread(target=self._read_data)
        self._thread.start()

    
    def _read_data(self):

        while not self._stop_thread:
            
            try:
                self.controller_info["hid_device"].open()
                self.controller_info["hid_device"].set_raw_data_handler(self.sample_handler)          
                #print("\nWaiting for data...\n")
                self.controller_info["data_available"] = True
                while not kbhit() and self.controller_info["hid_device"].is_plugged() and not self._stop_thread:
                    # Das Gerät offen halten, um Ereignisse zu empfangen
                    sleep(0.5)
            finally:
                self.controller_info["data_available"] = False
                self.controller_info["hid_device"].close()

    def sample_handler(self,data):
        self.controller_info["raw_data"] = data

    def get_data(self,index):
        if(self.controller_info["data_available"]):
            return self.controller_info["raw_data"][index]
        else:
            print("device sleeping?")
            return None

    def get_raw_data(self):
        if(self.controller_info["data_available"]):
            if(self.controller_info["raw_data"] == None):
                print("wakeup your device")
            return self.controller_info["raw_data"]
        else:
            print("device sleeping?")
            return None    

    def data_available(self):
        if(self.controller_info["data_available"]):
            return True
        else:
            return False    

    
    def close(self):
        print("Close connection")
        self.controller_info["data_available"]=False
        self._stop_thread = True
        if self._thread:
            self._thread.join()  # Warten, bis der Thread beendet ist
        self.controller_info['connected'] = False
        print(f"Verbindung zu {self.controller_info['name']} geschlossen.")
        
    def extract_vid_pid(self,hid_list,_vid,_pid):
        index = -1
        for device in hid_list:
            index=index+1
            #print("Device in for loop",device)
            device_string = str(device)  
            # Extrahiere die vID
            vid_start = device_string.find("vID=") + 4
            vid_end = device_string.find(",", vid_start)
            vid = device_string[vid_start:vid_end]
            # Extrahiere die pID
            pid_start = device_string.find("pID=") + 4
            pid_end = device_string.find(",", pid_start)
            pid = device_string[pid_start:pid_end]
            #print("search for",f"vID: {_vid}, pID: {_pid}")
            #print("found",f"vID: {vid}, pID: {pid}")
            if (_vid == vid and _pid == pid):
                print("found device")
                return device#,_vid,_pid
