# # i hate these types of problems
#
# # found it using "pen and paper", parsed the instructions to:
#
#
# inp w
# z = d0 + 13
#
# inp w
# z%26 + 13 == d1
# else: z= z*26 + d1 + 10
#
# inp w
# z%26 + 13 == d2
# else: z = z*26 + d2 + 3
#
# inp w
# z //= 26
# z % 26 - 11 == d3
# else: z = z*26 + d3 + 1
#
# inp w
# z % 26 + 11 == d4
# else: z = z*26 + d4 + 9
#
# inp w
# z //= 26
# z % 26 - 4 == d5
# else: z = z*26 + d5 + 3
#
# inp w
# z % 26 + 12 == d6
# else: z = z*26 + d6 + 5
#
# inp w
# z % 26 + 12 == d7
# else: z = z*26 + d7 + 1
#
# inp w
# z % 26 + 15 == d8
# else: z = z*26 + d8 + 0
#
# inp w
# z //= 26
# z % 26 - 2 == d9
# else: z = z*26 + d9 + 13
#
# inp w
# z //= 26
# z % 26 - 5 == d10
# else: z = z*26 + d10 + 7
#
# inp w
# z //= 26
# z % 26 - 11 == d11
# else: z = z*26 + d11 + 15
#
# inp w
# z //= 26
# z % 26 - 13 == d12
# else: z = z*26 + d12 + 12
#
# inp w
# z //= 26
# z % 26 - 10 == d13
# else: z = z*26 + d13 + 8


# which works to
#
# d0 + 13
# d1 + 10
# xd2 + 3
# d3 == d2 + 3 - 11
# pop
# xd4 + 9
# d5 == d4 + 9 - 4
# pop
# xd6 + 5
# xd7 + 1
# xd8 + 0
# d9 == d8 + 0 - 2
# pop
# d10 == d7 + 1 - 5
# pop
# d11 == d6 + 5 - 11
# pop
# d12 == d1 + 10 - 13
# pop
# d13 == d0 + 13 - 10
# pop
#
#
# d13 = d0 + 3
# d12 = d1 - 3
# d11 = d6 - 6
# d10 = d7 - 4
# d9 = d8 - 2
# d8
# d7
# d6
# d5 = d4 + 5
# d4
# d3 = d2 - 8
# d2
# d1
# d0
#
# 69914999975369