from subprocess import Popen,  PIPE

def start():
    cava = Popen(
        ["cava"],
        stdout=PIPE,
        text=True
    )
    return cava
    
def read_frame(cava: Popen[str]):
    assert cava.stdout is not None
    frame: list[str] = cava.stdout.readline().strip().split(";")
    return [int(bar) for bar in frame[:-1]]
