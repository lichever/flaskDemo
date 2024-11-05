def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!'


# foo('0')
foo('1')
#python3 -O assertDemo.py   close assert
