import io

def load(filename):
    data = list(io.RFile(filename))
    if len(data) == 1:
        data = data[0]

    return data
