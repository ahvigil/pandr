import pandr.io.utils

def test_decode_version():
    # 3.3.1 packed as integer
    assert pandr.io.utils.decode_version(197377) == (3,3,1)
    # 2.15.2 packed as integer
    assert pandr.io.utils.decode_version(134914) == (2,15,2)
