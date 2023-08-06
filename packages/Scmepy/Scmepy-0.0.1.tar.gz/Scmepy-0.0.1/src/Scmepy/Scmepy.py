class Scmepy():
    #função para converter celcius em fahrenheit:
    def Cf(c):
        f=c*(9.0/5.0)+32
        return f

    #função para converter fahrenheit em celcius:
    def Fc(f):
        c=5.0*(f-32)/9
        return c

    #função para converter kelvin em celcius:
    def Kc(k):
        c=k-273.15
        return c

    #função para converter celcius em kelvin:
    def Ck(c):
        k=c+273.15
        return k

    #função para converter quilometros em metros por segundo:
    def KmM(k):
        ms = k/3.6
        return ms

    #função para converter metros por segundo em quilometros:
    def MsK(ms):
        kh = ms*3.6
        return kh

    #função para converter milhas em quilometros:
    def Mkm(m):
        km = m*1.61
        return km

    #função para converter quilometros em  milhas:
    def Kmmi(k):
        m = k/1.61
        return m

    #função para converter graus em  radianos:
    def Gr(g):
        pi=3.14
        r=g*pi/180
        return r

    #função para converter radianos em graus:
    def Rg(r):
        pi=3.14
        g=r*180/pi
        return g

    #função para converter polegadas em centimetros:
    def Pc(p):
        c=p*2.54
        return c

    #função para converter centimetros em polegadas:
    def Cp(c):
        p=c/2.54
        return p

    #função para converter metros cubicos em litros:
    def M3l(m):
        l = m*1000
        return l

    #função para converter litros em metros cubicos:
    def Lm3(l):
        m=l/1000
        return m

    #função para converter quilograms em libras:
    def Kgl(k):
        l = k/0.45
        return l

    #função para converter libras em quilogramas:
    def Lkg(l):
        k = l*0.45
        return k

    #função para converter jardas em metros:
    def Jm(j):
        m = j*0.91
        return m

    #função para converter metros em jardas:
    def Mj(m):
        j = m/0.91
        return j

    #função para converter metros quadrados em acres:
    def M2a(m2):
        ac = m2*0.000247
        return ac

    #função para converter acres em metros quadrados:
    def Acm(ac):
        m2 = ac*4048.58
        return m2

    #função para converter metros quadrados em hectares:
    def M2h(m2):
        he = m2*0.0001
        return he

    #função para converter hectares em metros quadrados:
    def Hem(he):
        m2 = he*0.10000
        return m2