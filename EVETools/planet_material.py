pm = {'sghj':1268,'jmhj':1900,'dyfhw':1635,'gjs':1200,'fyjs':6500,'gzhj':2665}

if __name__ == "__main__":
    a = {'sghj':351.2,'jmhj':250.6,'dyfhw':380.1,'gjs':376.32,'fyjs':6.31,'gzhj':338.52}
    value = 0
    for m,n in a.items():
        value += n* pm[m]
    print(value*24)