import subprocess

def start():
    cava = subprocess.Popen(
        ["cava"],
        stdout=subprocess.PIPE,
        text=True
    )
    return cava
    
def read_frame(cava):
    frame = cava.stdout.readline().strip().split(";")
    return [int(bar) for bar in frame[:-1]]
