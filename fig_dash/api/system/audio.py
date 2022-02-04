# import subprocess
# # call(["amixer", "-D", "pulse", "sset", "Master", "0%"])

# # call(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
# def set_volume():
#     valid = False

#     while not valid:
#         volume = input('What volume? > ')

#         try:
#             volume = int(volume)

#             if (volume <= 100) and (volume >= 0):
#                 subprocess.call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
#                 valid = True

#         except ValueError:
#             pass
import chime
import pulsectl


class PulseController:
    '''convenience wrapper around pulsectl, which itself is a pyton wrapper around libpulse (I think)'''
    def __init__(self, client_name: str='my-client-name'):
        self.pulse = pulsectl.Pulse(client_name)
        self.pre_mute_vol = None
        self._is_muted = False

    def set_volume(self, volume=1):
        for sink in self.sinks:
            self.pulse.volume_set_all_chans(sink, volume)
            self.pre_mute_vol = volume

    def mute(self):
        for sink in self.sinks:
            self.pulse.volume_set_all_chans(sink, 0)
        self._is_muted = True

    def increase(self):
        self.set_volume(self.get_volume()[0]+0.1)
        chime.info()

    def decrease(self):
        self.set_volume(self.get_volume()[0]-0.1)
        chime.info()

    def unmute(self):
        for sink in self.sinks:
            self.pulse.volume_set_all_chans(sink, self.pre_mute_vol)
        self._is_muted = False

    def toggle_mute(self):
        if self._is_muted:
            self.unmute()
        else:
            self.mute()

    def get_volume(self):
        sink_volumes = []
        for sink in self.sinks:
            sink_volumes.append(self.pulse.volume_get_all_chans(sink))

        return sink_volumes

    @property
    def sink_inputs(self):
        return self.pulse.sink_input_list()

    @property 
    def sinks(self):
        return self.pulse.sink_list()

    def __del__(self):
        print("closing lib pulse")
        self.pulse.close()

def test_volume():
    pass


if __name__ == "__main__":
    test_volume()