# input Key (K0):
# Hex 0123456789ABCDEF
#
# Hexadecimal notation: 0 1 2 3 4 5 6 7 8 9 A B C D E F
#
# Binary notation: 	0000 0001 0010 0011 0100 0101 0110 0111
# 1000 1001 1010 1011 1100 1101 1110 1111
#
# We will use a single 64-bit block containing the ASCII text “MESSAGES” as the plaintext.
#
#
#     1. Derive the round 1 key K1. This involves the following steps:
#         a)  Reduce the initial 64-bit key input to the requisite 56-bit key by mapping the bits of
# the initial key through the Permuted Choice 1 (PC-1) box.   (64 bits excluding every 8th bit = 56 bits.
 # These removed 8-bits are sometimes used as parity bits).
hex_key = "0123456789ABCDEF"


binary_string = bin(int(hex_key, 16))[2:].zfill(64)


print(binary_string)






############################map pc1
def mapper(pc, binary_string):
    bit_mapping = ""
    for pos in pc:
        bit_mapping+=(binary_string[pos-1])
    return bit_mapping

PC1 = [57,   49,    41,   33,    25,    17,    9,
        1, 58, 50, 42, 34, 26,
        18,10,  2, 59, 51, 43, 35,
        27,19, 11,  3, 60, 52, 44,
        36,63, 55, 47, 39, 31, 23,
        15, 7, 62, 54, 46, 38, 30, 22,
        14,  6, 61, 53, 45, 37, 29,21,
        13,  5, 28, 20, 12,  4]

pca1_mapped = mapper(PC1, binary_string)
print(pca1_mapped)









#####################leftshifts
def halver(arr):
    half_idx = int(len(arr)/2)
    return (arr[:half_idx], arr[half_idx:])

left_half, right_half = halver(pca1_mapped)

key_of_left_shifts = list( {"l": "", "r":""} for _ in range(16) )

print(key_of_left_shifts)

shift_amount = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

for idx, key_pairs in enumerate(key_of_left_shifts):
    left_half = left_half[shift_amount[idx]:] + left_half[:shift_amount[idx]]
    right_half = right_half[shift_amount[idx]:] + right_half[:shift_amount[idx]]
    key_pairs["l"] = left_half
    key_pairs["r"] = right_half

print(key_of_left_shifts[0])




##############map pc2
PC2 =  [ 14,    17,   11, 24,  1,  5,
          3,    28,   15,  6, 21, 10,
         23,    19,   12,  4, 26,  8,
         16,     7,   27, 20, 13,  2,
         41,    52,   31, 37, 47, 55,
         30,    40,   51, 45, 33, 48,
         44,    49,   39, 56, 34, 53,
         46,    42,   50, 36, 29, 32]

pc2_mapped_keys = []

for left_right_shifts in key_of_left_shifts:
    combined = left_right_shifts["l"] + left_right_shifts["r"]
    len(combined)
    pc2_mapped_keys.append(mapper(PC2, combined))

print(pc2_mapped_keys[0])


#############################################################################part 2

################ change plain text ot  binary_string
M = bin(int.from_bytes('MESSAGES'.encode(), 'big'))[2:].zfill(64)
print(M)



################ apply initial permutation and break into halves
IP =   [58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17,  9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7]

ip_mapped = mapper(IP, M)

left_ip, right_ip = halver(ip_mapped)
print(left_ip, right_ip)


################# Get emapped
E = [32,     1,    2,     3,     4,    5,
      4,     5,    6,     7,     8,    9,
      8,     9,   10,    11,    12,   13,
     12,    13,   14,    15,    16,   17,
     16,    17,   18,    19,    20,   21,
     20,    21,   22,    23,    24,   25,
     24,    25,   26,    27,    28,   29,
     28,    29,   30,    31,    32,   1 ]

e_mapped = mapper(E, right_ip)
print(emapped)



########calcualate A
A = int( pc2_mapped_keys[0],2) ^ int(e_mapped,2)
A = ('{0:b}'.format(A))
A = A.zfill(48)
print(A)



#group into 6 and sbox substitute
s_sets     = [A[i:i + 6] for i in range(0, len(A), 6)]
len(s_sets)

sbox_addressor = [[14,  4,  13,  1,   2, 15,  11,  8,   3, 10,   6, 12,   5,  9,   0,  7],
                  [ 0, 15,   7,  4,  14,  2,  13,  1,  10,  6,  12, 11,   9,  5,   3,  8],
                  [ 4,  1,  14,  8,  13,  6,   2, 11,  15, 12,   9,  7,   3, 10,   5,  0],
                  [15, 12,   8,  2,   4,  9,   1,  7,   5, 11,   3, 14,  10,  0,   6, 13]]
B_nums = []
for addr in s_sets:
    row = int(addr[:2],2)
    col = int(addr[2:],2)
    B_nums.append(sbox_addressor[row][col])
print(B_nums)




#get 32 bit result concatanate
B = ""
for num in B_nums:
    B += str(bin(num))[2:].zfill(4)
P = [16,   7,  20,  21,
     29,  12,  28,  17,
      1,  15,  23,  26,
      5,  18,  31,  10,
      2,   8,  24,  14,
     32,  27,   3,   9,
     19,  13,  30,   6,
     22,  11,   4,  25]
print(B)

# apply permutation
PB = mapper(P, B)
print(PB)


#calculate l
R1 = int( PB ,2) ^ int(left_ip,2)
R1 = ('{0:b}'.format(R1))
print(R1)
