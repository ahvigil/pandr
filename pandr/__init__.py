import io

def load(filename):
    data = list(io.RFile(filename))
    data = [d.value for d in data]
    if len(data) == 1:
        data = data[0]

    return data
