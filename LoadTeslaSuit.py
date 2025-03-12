from teslasuit_sdk import ts_api


class LoadTeslaSuit:
    def __init__(self, lib_path=None):
        print("Connecting teslasuit device...")
        self.api = ts_api.TsApi(lib_path)
        self.device = self.api.get_device_manager().get_or_wait_last_device_attached()
        self.mocap = self.device.mocap
        self.emg = self.device.emg
        self.ppg = self.device.ppg
        self.temperature = self.device.temperature
        self.magnetic_encoder = self.device.magnetic_encoder
        self.haptic = self.device.haptic
        self.bia = self.device.bia
        print("Device connected.")
    
    def get_mocap(self):
        return self.mocap
    
    def get_emg(self):
        return self.emg
    
    def get_ppg(self):
        return self.ppg
    
    def get_temperature(self):
        return self.temperature

    def get_magnetic_encoder(self):
        return self.magnetic_encoder
    
    def get_haptic(self):
        return self.haptic
    
    def get_bia(self):
        return self.bia
    
    def __del__(self):
        # Evitar la destrucción automática del API
        pass
