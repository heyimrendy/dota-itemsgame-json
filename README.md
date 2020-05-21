# dota-itemsgame-json
My personal project for vanilla dota mod. Convert `items_game.txt` into proper JSON.

Duplicate keys converted into list. Doesn't support comments, will be broken if you try to parse KeyValues with comments. Only tested with dota2 `items_game.txt` that acquire directly through VPK, will be broken if you try the one from Dotabuff VPK because they strip `/r`

Required Python 3.7 or at least Python version that support static typing.