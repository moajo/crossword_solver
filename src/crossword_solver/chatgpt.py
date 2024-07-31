import openai
import os
from crossword_solver.types import Line, Crossword

# 環境変数からAPIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")


def word_post_process(word: str):
    a = "ャュョェィ"
    b = "ヤユヨエイ"
    for aa, bb in zip(a, b):
        word = word.replace(aa, bb)
    return word.strip()


def predict1(problem: Crossword, lines: list[Line]):
    prompts = [
        f"Q{i+1}:「{line.hint}」カタカナ{line.length}文字でいうと何でしょう？ ヒント: {line.get_current_answer(problem.cells).replace('*','○')}"
        for i, line in enumerate(lines)
    ]
    prompt = "\n".join(prompts)

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
複数の質問への回答を1問1行で、簡潔にカタカナ1単語で回答してください。
# 回答例
## input
Q1: 「赤くて丸い果物」カタカナ3文字でいうと何でしょう？ ヒント: ○○ゴ
Q2: 「計算する装置」カタカナ6文字でいうと何でしょう？ ヒント: ○ンピュ○○○
## output
Q1: リンゴ
Q2: コンピュータ
                """,
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    text = response.choices[0].message.content
    if text is None:
        raise ValueError("No answer")
    answers = text.split("\n")
    if len(answers) != len(lines):
        raise ValueError("Number of answers does not match the number of lines.")
    a: list[str] = []
    for i, ans in enumerate(answers):
        if not ans.startswith(f"Q{i+1}: "):
            raise ValueError(f"Answer format is invalid: {ans}")
        a.append(ans[len(f"Q{i}: ") :])
    return [word_post_process(aa) for aa in a]


if __name__ == "__main__":
    prompt = """
f"Q1:「遠くの地で大事業をしようという計画のこと。○○○の翼」ヒント: ト○ン"
    """
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
説明に当てはまる単語を1問1行で、カタカナ1単語で回答してください。
# 回答例
## input
Q1: 「赤くて丸い果物」ヒント: ○○ゴ
Q2: 「計算する装置」ヒント: ○ンピュ○○○
Q4: 「光を反射する板」ヒント: カ○ミ
## output
Q1: リンゴ
Q2: コンピュータ
Q3: カガミ
            """,
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    text = response.choices[0].message.content
    print(text)
