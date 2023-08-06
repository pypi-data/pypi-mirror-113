class datatypes:
    def __init__(self,x):
        for (columnName, n) in x.iteritems():
            t = 0
            h = 0
            i = 0
            r = 0
            u = 0
            s = 0
            id = 0
            d = 0
            ha = 0
            rth = 0
            n = n.to_list()
            print()
            print('column name:  ','[',columnName,']')
            for ur in n:
                if type(ur) == int:
                    t += 1
                if type(ur) == str:
                    h += 1
                if type(ur) == float:
                    i += 1
                if type(ur) == complex:
                    r += 1
                if type(ur) == bool:
                    u += 1
                if type(ur) == tuple:
                    s += 1
                if type(ur) == list:
                    id += 1
                if type(ur) == dict:
                    d += 1
                if type(ur) == set:
                    ha += 1
                if ur != ur:
                    rth += 1
            print('integer:        ',t)
            print('string:         ',h)
            print('float:          ',i)
            print('complex_number: ',r)
            print('boolean:        ',u)
            print('tuple:          ',s)
            print('list:           ',id)
            print('dictionary:     ',d)
            print('set:            ',ha)
            print('null:           ',rth)