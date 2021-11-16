wn = ['通碧','断魄','坠明','荧焰','折镜']
wd = {'通碧':50,'断魄':50,'坠明':50,'荧焰':50,'折镜':50}
def show():
    print(
'''{} {} {} {} {}
 {}  {}'''.format(wn[0],wn[1],wn[2],wn[3],wn[4]
          ,wd[wn[0]],wd[wn[1]]))
    
def N():
    wn[0],wn[2],wn[3],wn[4] = wn[2],wn[3],wn[4],wn[0]
    wd[wn[4]] = 50

def A():
    num = wd[wn[0]]
    wd[wn[0]] = num - 1
    if num == 1:
        N()

def Q():
    num = wd[wn[0]]
    if num <= 10:
        N()
    else:
        wd[wn[0]] = num - 10

def W():
    wn[0],wn[1] = wn[1],wn[0]

show()
while 1:
    k = input()
    if k == 'a':
        A()
    if k == 'w':
        W()
    if k == 'q':
        Q()
    if k == 'm':
        break
    show()
