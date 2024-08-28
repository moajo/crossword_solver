# usage

Set your own key:

```bash
export OPENAI_API_KEY="sk-xxxxxx"
```

Enjoy!

```bash
# easy problem: almost correct! 😊😊😊
❯ cat sample_problem2.json|rye run python src/crossword_solver/crossword.py
 1|  | 2|■■| 3| 4|
  |■■| 5|  |  |  |■■
 6| 7|  |■■| 8|  | 9
■■|10|  |11|  |■■|
12|  |■■|  |■■|13|
14|  |15|  |16|  |■■
17|  |  |■■|18|  |
processing...

completed
 1サ|  ク| 2ラ|■■■■| 3エ| 4イ|  コ
  カ|■■■■| 5イ|  チ|  ジ|  ク|■■■■
 6ナ| 7タ|  ネ|■■■■| 8ソ|  ラ| 9ミ
■■■■|10カ|  ン|11カ|  ン|■■■■|  ツ
12メ|  シ|■■■■|  エ|■■■■|13タ|  イ
14キ|  ー|15ホ|  ル|16ダ|  ー|■■■■
17キ|  ド|  ウ|■■■■|18シ|  ン|  シ
```

```bash
# hard problem: answer might be wrong...😭😭😭
❯ cat sample_problem1.json|rye run python src/crossword_solver/crossword.py
 1| 2|  | 3|■■| 4| 5
 6|  |■■| 7|  |  |
 8|  | 9|  |■■|10|
11|  |  |  |12|  |
13|  |  |■■|  |■■|
  |■■|14|  |  |15|
16|  |  |■■|17|  |
processing...

completed
 1エ| 2オ|  ル| 3ス|■■■■| 4ア| 5ヨ
 6ク|  ー|■■■■| 7イ|  オ|  ン|  カ
 8ロ|  ウ| 9カ|  ク|■■■■|10ト|  ラ
11ジ|  エ|  ー|  ン|12グ|  レ|  イ
13ヤ|  ン|  マ|■■■■|  ア|■■■■|  チ
  イ|■■■■|14イ|  サ|  ナ|15ト|  リ
16ト|  ビ|  ン|■■■■|17コ|  キ|  ン
```

# ref

https://repri.jp/%E3%83%91%E3%82%BA%E3%83%AB%E3%83%BB%E3%82%AF%E3%83%AD%E3%82%B9%E3%83%AF%E3%83%BC%E3%83%89/%E3%82%AF%E3%83%AD%E3%82%B9%E3%83%AF%E3%83%BC%E3%83%89%E3%83%91%E3%82%BA%E3%83%AB/
