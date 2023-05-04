import subprocess
import datetime

def codecChange(filename):
    # specify the input and output files
    input_file = filename
    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"sample_output_{time_stamp}.wav"
    output_file = f"audio/working_audio/sample_output_{time_stamp}.wav"

    # output_file = "sample_output.wav"

    command = ['C:\\ffmpeg\\bin\\ffmpeg.exe', '-i', input_file, '-c:a', 'pcm_s16le', output_file]

    subprocess.run(command)

    return output_file

# codecChange("audio/input_audio/20230121_174620_audio.wav")