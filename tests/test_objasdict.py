"""
Test sigfoxapi._objdict()

"""

from sigfoxapi import _dictasobj

DICT =  {'strkey': 'strvalue',
         'intkey': 1,
         'floatkey': 1.0,
         'boolkey': True,
         'listkey': [
                        'strvalue2',
                         2,
                         2.0,
                         False,
                         {
                             'strkey3': 'strvalue4',
                             'intkey3': 4,
                             'boolkey3': True
                         }
                    ],
         'dictkey': {
                        'strkey2': 'strvalue3',
                        'intkey2': 3,
                        'floatkey2': 3.0,
                        'boolkey2': True,
                        'listkey2': [
                                        'strvalue5',
                                        5,
                                        5.0,
                                        False
                                    ],
                    }
         }

OBJ = _dictasobj(DICT)

class TestObjcDict(object):

    def test_nested0(self):
        assert OBJ.strkey == DICT['strkey']
        assert OBJ.intkey == DICT['intkey']
        assert OBJ.floatkey == DICT['floatkey']
        assert OBJ.boolkey == DICT['boolkey']
        assert OBJ.listkey[0] == DICT['listkey'][0]
        assert OBJ.listkey[1] == DICT['listkey'][1]
        assert OBJ.listkey[2] == DICT['listkey'][2]
        assert OBJ.listkey[3] == DICT['listkey'][3]

    def test_nested1(self):
        assert OBJ.dictkey.strkey2 == DICT['dictkey']['strkey2']
        assert OBJ.dictkey.intkey2 == DICT['dictkey']['intkey2']
        assert OBJ.dictkey.floatkey2 == DICT['dictkey']['floatkey2']
        assert OBJ.dictkey.boolkey2 == DICT['dictkey']['boolkey2']
        assert OBJ.dictkey.listkey2[0] == DICT['dictkey']['listkey2'][0]
        assert OBJ.dictkey.listkey2[1] == DICT['dictkey']['listkey2'][1]
        assert OBJ.dictkey.listkey2[2] == DICT['dictkey']['listkey2'][2]
        assert OBJ.dictkey.listkey2[3] == DICT['dictkey']['listkey2'][3]

    def test_nested2(self):
        assert OBJ.listkey[4].strkey3 == DICT['listkey'][4]['strkey3']
        assert OBJ.listkey[4].intkey3 == DICT['listkey'][4]['intkey3']
        assert OBJ.listkey[4].boolkey3 == DICT['listkey'][4]['boolkey3']
