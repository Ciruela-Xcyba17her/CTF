from operator import mod
from functools import reduce
import binascii

"""
$ nc 2019shell1.picoctf.com 12275
c: 4988111922056790210926116185239919634433747583837155067043486180480325230231744881857523981466840037052774030693700049845638111823943084208668446048561785922157349809096068381633083520004357636792689610659752546731323326371550698419263646726901352526390552226388979109506451316519266743488456511216784429496342081584838418115886569260697005928
n: 8217807183455988010860519229338403314531150669864202541906520558261361433687608694651442440706426041599598892942776220880667716280817199717521598795599026393386268438829006975963705695732106834639417637991329315595598090932441468643877875749666730713504324102176951712130371248555465896297678755934279782875250020922706833313967236039811767241
e: 65537

# then factorized n by sympy.factorint
# factorizing takes several minutes...

$ pip install sympy
$ python
>>> import sympy
>>> n = 8217807183455988010860519229338403314531150669864202541906520558261361433687608694651442440706426041599598892942776220880667716280817199717521598795599026393386268438829006975963705695732106834639417637991329315595598090932441468643877875749666730713504324102176951712130371248555465896297678755934279782875250020922706833313967236039811767241
>>> sympy.factorint(n)
{15845014621: 1, 15479238319: 1, 13128674233: 1, 14650245017: 1, 9073864753: 1, 14704427893: 1, 8827684039: 1, 10057403611: 1, 13693904449: 1, 13814993039: 1, 16407392851: 1, 11569171241: 1, 11591615813: 1, 11654471629: 1, 9419843639: 1, 9502922423: 1, 14559991013: 1, 12339624551: 1, 9981803467: 1, 13857412123: 1, 12415359163: 1, 11608875709: 1, 11220021223: 1, 12115424887: 1, 14338550021: 1, 10730440549: 1, 12406295129: 1, 15944005079: 1, 9095847427: 1, 11308187101: 1, 9863685877: 1, 13390969831: 1, 13140921967: 1, 12799885223: 1}
"""

### Define Values
def define_values():

    # prime factors of n
    ps = [
        15845014621,
        15479238319,
        13128674233,
        14650245017,
        9073864753,
        14704427893,
        8827684039,
        10057403611,
        13693904449,
        13814993039,
        16407392851,
        11569171241,
        11591615813,
        11654471629,
        9419843639,
        9502922423,
        14559991013,
        12339624551,
        9981803467,
        13857412123,
        12415359163,
        11608875709,
        11220021223,
        12115424887,
        14338550021,
        10730440549,
        12406295129,
        15944005079,
        9095847427,
        11308187101,
        9863685877,
        13390969831,
        13140921967,
        12799885223
    ]
    e = 65537
    c = 4988111922056790210926116185239919634433747583837155067043486180480325230231744881857523981466840037052774030693700049845638111823943084208668446048561785922157349809096068381633083520004357636792689610659752546731323326371550698419263646726901352526390552226388979109506451316519266743488456511216784429496342081584838418115886569260697005928
    
    return ps, e, c



### Modular Inverse
# https://gist.github.com/ofaurax/6103869014c246f962ab30a513fb5b49
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m



### Chinese Remainder Theorem ()
# https://mail.python.org/pipermail/edu-sig/2001-August/001665.html
def eea(a,b):  
    """Extended Euclidean Algorithm for GCD"""
    v1 = [a,1,0]
    v2 = [b,0,1]
    while v2[0]!=0:
       p = v1[0]//v2[0] # floor division
       v2, v1 = list(map(lambda x, y: x-y,v1,[p*vi for vi in v2])), v2
    return v1

def inverse(m,k):  
     """
     Return b such that b*m mod k = 1, or 0 if no solution
     """
     v = eea(m,k)
     return (v[0]==1)*(v[1] % k)

def crt(ml,al):  
     """
     Chinese Remainder Theorem:
     ms = list of pairwise relatively prime integers
     as = remainders when x is divided by ms
     (ai is 'each in as', mi 'each in ms')

     The solution for x modulo M (M = product of ms) will be:
     x = a1*M1*y1 + a2*M2*y2 + ... + ar*Mr*yr (mod M),
     where Mi = M/mi and yi = (Mi)^-1 (mod mi) for 1 <= i <= r.
     """

     M  = reduce(lambda x, y: x*y,ml)        # multiply ml together
     Ms = [M//mi for mi in ml]   # list of all M/mi
     ys = [inverse(Mi, mi) for Mi,mi in zip(Ms,ml)] # uses inverse,eea
     return reduce(lambda x, y: x+y,[ai*Mi*yi for ai,Mi,yi in zip(al,Ms,ys)]) % M



def main():
    primes, e, c = define_values()

    n_list = []
    a_list = []

    # computation acceleration by Chinese Remainder Theorem
    for prime in primes:
        phi_p = prime - 1
        d = int(modinv(e, phi_p))
        m = pow(c, d, prime)
        n_list.append(prime)
        a_list.append(m)
    plaintext = crt(n_list, a_list)
    
    print("%x" % plaintext)
    print(binascii.unhexlify(format(plaintext, 'x')).decode())

if __name__ == '__main__':
    main()
    
