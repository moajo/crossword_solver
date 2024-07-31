from dataclasses import dataclass
import dataclasses
from pydantic import BaseModel
from typing import Literal
from enum import Enum

# キー番号なら数値、空白は"."、壁は"x"で表現
CellType = int | Literal["."] | Literal["x"]


def cell_type_to_str(cell: CellType):
    if cell == "x":
        return "■■"
    if cell == ".":
        return "  "
    return f"{cell: >2}"


class Direction(Enum):
    H = "h"
    V = "v"

    @property
    def inverse(self):
        if self == Direction.H:
            return Direction.V
        else:
            return Direction.H


# @dataclass
# class Constraint:
#     position: int
#     target_line_id: str
#     target_position: int


@dataclass
class CellConstraint:
    line_id: str
    position: int


@dataclass
class Cell:
    cell_type: CellType
    constraints: list[CellConstraint]
    current_predictions: list[str]  # 仮予測文字のリスト
    answer: str  # 暫定予測

    def __init__(self, cell_type: CellType):
        self.cell_type = cell_type
        self.constraints = []
        self.current_predictions = []
        self.answer = ""

    def is_certainly(self):
        """確実っぽいかどうか。予測が2文字入ってどちらも一致してたら確実っぽいとみなす"""
        if len(self.current_predictions) < 2:
            return False
        return len(set(self.current_predictions)) == 1

    def get_lines(self, board: "Crossword"):
        return [board.get_line(c.line_id) for c in self.constraints]


@dataclass
class Line:
    id: str  # "h1", "v2", ...
    start_position: tuple[int, int]
    hint: str
    length: int

    predicted_word: str

    def iterate_cell_index(self):
        direction = Direction.H if self.id[0] == "h" else Direction.V
        if direction == Direction.V:
            dx, dy = 0, 1
        elif direction == Direction.H:
            dx, dy = 1, 0

        y, x = self.start_position
        for i in range(self.length):
            yield y, x
            x += dx
            y += dy

    def is_finalized(self, cells: list[list[Cell]]):
        for i, (y, x) in enumerate(self.iterate_cell_index()):
            if cells[y][x].answer == "":
                return False
        return True

    def get_current_answer(self, cells: list[list[Cell]]):
        direction = Direction.H if self.id[0] == "h" else Direction.V
        if direction == Direction.V:
            dx, dy = 0, 1
        elif direction == Direction.H:
            dx, dy = 1, 0

        y, x = self.start_position
        answer = ""
        for i in range(self.length):
            if len(cells[y][x].answer) > 0:
                answer += cells[y][x].answer
            else:
                answer += "*"
            x += dx
            y += dy
        return answer

    def get_hint(self, cells: list[list[Cell]]):
        a = self.get_current_answer(cells)
        return f"{self.id}:{a} 「{self.hint}」"

    def fill_cells(self, cells: list[list[Cell]], answer: str):
        """仮回答を入れる"""
        # 長さが違うやつは絶対に入らないので拒否する
        if self.length != len(answer):
            # print("\twarning: length mismatch")
            return
        # 確定マスとの一致が2マス以上あったら確定させる
        match_count = 0
        for i, (y, x) in enumerate(self.iterate_cell_index()):
            if cells[y][x].answer == answer[i]:
                match_count += 1
        self.predicted_word = answer

        if match_count >= 2:
            print("予測が確定マスと2点以上一致しているので確定させます")
            self.finalize(cells)
            return

        # この時点では確定しないので、仮予測を入れる
        print(f"仮回答:{answer} {self.get_hint(cells)}")
        for i, (y, x) in enumerate(self.iterate_cell_index()):
            cells[y][x].current_predictions.append(answer[i])

    def finalize(self, cells: list[list[Cell]]):
        if self.is_finalized(cells):
            return
        print(":", self.id, self.length, self.predicted_word)
        for i, (y, x) in enumerate(self.iterate_cell_index()):
            cells[y][x].answer = self.predicted_word[i]


def cell_expression(cell: Cell):
    t = cell_type_to_str(cell.cell_type)
    if cell.cell_type == "x":
        return "■■■■"
    if cell.answer != "":
        return t + f"{cell.answer}"
    return t + f"({''.join(cell.current_predictions)})"


@dataclass
class Crossword:
    h: int
    w: int
    cells: list[list[Cell]]
    lines: list[Line]

    def __str__(self):
        # ┌──┬──┬──┬──┬──┬──┬──┐
        #  1│ 2│  │ 3│■■│ 4│ 5
        # └──┴──┴──┴──┴──┴──┴──┘

        return "\n".join(
            [
                "|".join([cell_type_to_str(cell.cell_type) for cell in line[:-1]])
                for line in self.cells[:-1]
            ]
        )

    def get_line(self, line_id: str):
        for line in self.lines:
            if line.id == line_id:
                return line
        raise ValueError(f"Line {line_id} not found.")

    def state(self):  # ちょっと詳細な状態を表示。debug用
        return "\n".join(
            [
                "|".join([cell_expression(cell) for cell in line[:-1]])
                for line in self.cells[:-1]
            ]
        )

    def fill_answer(self):
        """確からしい回答を確定させる"""
        for l in self.cells:
            for cell in l:
                if not cell.is_certainly():
                    continue
                for line in cell.get_lines(self):
                    line.finalize(self.cells)

    def is_finished(self):
        for l in self.lines:
            if not l.is_finalized(self.cells):
                return False
        return True

    def clear_memo(self):
        for l in self.lines:
            if not l.is_finalized(self.cells):
                l.predicted_word = ""
        for cells in self.cells:
            for cell in cells:
                cell.current_predictions = []


class CrosswordDefinition(BaseModel):
    cells: list[str]
    key_tate: dict[str, str]
    key_yoko: dict[str, str]
