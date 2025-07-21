WIDTH = 16
HEIGHT = 17

original_layout = [
    33,
    34,
    98,
    2,
    3,
    4,
    5,
    6,
    22,
    38,
    54,
    55,
    71,
    87,
    103,
    119,
    118,
    117,
    116,
    100,
    99,
    98,
    82,
    81,
    65,
    49,
    68,
    36,
    18,
]

new_layout = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
for num in original_layout:
    new_layout[num // WIDTH][num % WIDTH] = 1

for row in new_layout:
    print(row)
