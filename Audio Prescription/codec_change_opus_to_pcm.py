import subprocess

def codecChange():
    # specify the input and output files
    input_file = "sample.wav"
    output_file = "sample_output.wav"

    # use ffmpeg to convert the file
    # subprocess.call(['C:\\ffmpeg\\bin\\ffmpeg.exe', '-i', input_file, '-f', 's16le', '-acodec', 'pcm_s16le', output_file])

    command = ['C:\\ffmpeg\\bin\\ffmpeg.exe', '-i', input_file, '-c:a', 'pcm_s16le', output_file]

    subprocess.run(command)