from nlp_zero import *

t = Tokenizer()
t.tokenize(u'扫描二维码，关注公众号')

class D:
    def __iter__(self):
        with open('text.txt') as f:
            for l in f:
                yield l.strip() # python2.x还需要转编码