
class AttrDict(dict):
    '''dictionary where keys can be accessed via attributes (dict.atr)'''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self