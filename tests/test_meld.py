from yconf import Meld


# TODO: error on duplicate tokens
def test_meld_flat():
    m = Meld('foo: bar')
    assert m.foo == 'bar'

    m = Meld('''
      foo: FOO
      bar: 1
    ''')
    assert m.foo == 'FOO'
    assert m.bar == 1
