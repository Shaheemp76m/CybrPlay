import subprocess

def start():
    cava = subprocess.Popen(
        ["cava"],
        stdout=subprocess.PIPE,
        text=True
    )
    return cava
    
def read_frame(cava):
    frame = cava.stdout.readline()
    frame = frame.strip()
    frame = frame.split(";")
    
    bars = []
    frame.pop()
    for bar in frame:
        bar = int(bar)
        bars.append(bar)
    return bars

