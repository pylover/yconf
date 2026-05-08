from yconf import load


def test_load(mktmpfile, fileio):
    file = mktmpfile(content='''
      foo: bar
      bar:
        - baz
        - baz
    ''')

    m = load(file)
    assert m.foo == 'bar'
    assert m.bar == ['baz', 'baz']

    file = fileio(content='''
      foo:
        - bar
        - baz
    ''')
    m = load(file)
    assert m.foo == ['bar', 'baz']
