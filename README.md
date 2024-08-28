# usage

Set your own key:

```bash
export OPENAI_API_KEY="sk-xxxxxx"
```

Enjoy!

```bash
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
