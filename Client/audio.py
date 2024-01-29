import pyaudio
import numpy as np

chunk_size = 1024
sample_format = pyaudio.paInt16
channels = 1
sample_rate = 44100


def get_audio_input_devices():
    p = pyaudio.PyAudio()
    input_devices = []

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info['name']
        device_index = device_info['index']

        if device_info['maxOutputChannels'] == 0 and device_info['maxInputChannels'] > 0 and device_info['hostApi'] == 0 and "Microsoft Sound Mapper" not in device_name:
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

        if device_info['maxInputChannels'] == 0 and device_info['maxOutputChannels'] > 0 and device_info['hostApi'] == 0 and "Microsoft Sound Mapper" not in device_name:
            output_devices.append((device_name, device_index))

    p.terminate()
    return output_devices


def get_default_audio_devices():
    p = pyaudio.PyAudio()
    default_devices = []

    default_input_device_name = p.get_default_input_device_info()['name']
    default_input_device_index = p.get_default_input_device_info()['index']
    default_devices.append((default_input_device_name, default_input_device_index))

    default_output_device_name = p.get_default_output_device_info()['name']
    default_output_device_index = p.get_default_output_device_info()['index']
    default_devices.append((default_output_device_name, default_output_device_index))

    p.terminate()
    return default_devices


def record_audio(raw_audio, threshold, input_device_index):
    p = pyaudio.PyAudio()
    stream_in = p.open(format=sample_format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size, input_device_index=input_device_index)
    input_data = stream_in.read(chunk_size)
    input_array = np.frombuffer(input_data, dtype=np.int16)

    audio_level = np.abs(input_array).mean()

    if raw_audio or (not raw_audio and audio_level > threshold):
        return input_data


def play_audio(output_data, output_device_index):
    p = pyaudio.PyAudio()
    stream_out = p.open(format=sample_format, channels=channels, rate=sample_rate, output=True, frames_per_buffer=chunk_size, output_device_index=output_device_index)
    stream_out.write(output_data)
