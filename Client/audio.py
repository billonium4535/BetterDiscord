import pyaudio


def get_audio_input_devices():
    p = pyaudio.PyAudio()
    input_devices = []

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info['name']
        device_index = device_info['index']

        if device_info['maxInputChannels'] > 0:
            input_devices.append((device_name, device_index))

    p.terminate()
    return input_devices


def get_audio_output_devices():
    p = pyaudio.PyAudio()
    output_devices = []

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info['name']
        device_index = device_info['index']

        if device_info['maxOutputChannels'] > 0:
            output_devices.append((device_name, device_index))

    p.terminate()
    return output_devices
