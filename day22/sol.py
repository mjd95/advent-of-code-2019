from functools import lru_cache

num_cards = 119315717514047
num_rounds = 101741582076661

with open("input", "r") as f:
    lines = [line.strip() for line in f if line.strip()]

lines.reverse()

# find the position that shuffles to the provided position in one full pass through the rules
@lru_cache(maxsize=None)
def shuffle(pos):
    for line in lines:
        if line.startswith("deal with increment "):
            arg = int(line.lstrip("deal with increment "))
            pos = deal_with_increment(pos, arg)
        elif line.startswith("cut "):
            arg = int(line.lstrip("cut "))
            pos = cut(pos, arg)
        elif line.startswith("deal into new stack"):
            pos = deal_into_new_stack(pos)
    
    return pos

@lru_cache(maxsize=None)
def get_inverse(arg):
    inv = 1
    while True:
        if (inv*num_cards)%arg==1:
            break
        inv += 1
    return inv

# work out the thing that gets mapped to pos under deal with increment move
def deal_with_increment(pos, arg):
    inv = get_inverse(arg)
    # find gen s.t. gen*num_cards + pos % arg == 0.
    # i.e. find gen s.t. gen*num_cards = -pos mod arg
    # i.e. find gen s.t. gen = (-pos_*num_cards^{-1}) mod arg
    gen = (-pos * inv)%arg 
    return (gen*num_cards+pos)//arg

# work out the thing that gets mapped to pos under cut move
def cut(pos, arg):
    return (arg+pos)%num_cards

# work out the thing that gets mapped to pos under this move
def deal_into_new_stack(pos):
    return num_cards-1 - pos

# if y = ax+b, then b = 18997631927023 and a+18997631927023=110539374978353=> a=27773974462717
a = 27773974462717
b = 82765400515636 

def modular_exponent(a, b, N):
    # raise a to the power of b modulo N
    bits = list(bin(b)[2:])
    bits.reverse()
    ret = 1
    pw = a
    for i in range(len(bits)):
        if int(bits[i])==1:
            ret = (ret*pw)%N
        pw = (pw**2)%N
    return ret

def modular_inverse(a, N):
    # one of those math theorems says that a^phi(N) is 1 mod N
    # N is prime here, so a^(N-1) is 1 mod N
    # hence a^(N-2) is the inverse
    return modular_exponent(a, N-2, N)

# a^n*x + b(1-a^n)/(1-a)
x = 2020
print((modular_exponent(a, num_rounds, num_cards)*x + b*(1-modular_exponent(a, num_rounds, num_cards)) * modular_inverse(1-a, num_cards))%num_cards)

