import io

def load(filename):
    f = io.RFile(filename)
    data = list(f)

    if len(data) == 1:
        data = data[0]



    return data
