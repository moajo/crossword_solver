import json
import sys
from crossword_solver.types import (
    Cell,
    CellConstraint,
    Crossword,
    CrosswordDefinition,
    Direction,
    Line,
)
from crossword_solver.chatgpt import predict1


def parse_crossword_definition(definition: CrosswordDefinition):
    cells_raw = [cell_line.split(",") for cell_line in definition.cells]
    h = len(cells_raw)
    ls = [len(cl) for cl in cells_raw]
    w = ls[0]
    for l in ls:
        if l != ls[0]:
            raise ValueError("All cell lines must have the same length.")
    cells: list[list[Cell]] = []
    for l in cells_raw:
        line: list[Cell] = []
        for c in l:
            if c == "x" or c == ".":
                line.append(Cell(cell_type=c))
                continue
            if c.isdecimal():
                line.append(Cell(cell_type=int(c)))
                continue
            raise ValueError("All cell lines must consist of 'x', '.', or a number.")
        cells.append(line)

    # 扱いやすくするために右端と下端にxを追加
    for l in cells:
        l.append(Cell(cell_type="x"))
    cells.append([Cell(cell_type="x") for _ in range(w + 1)])

    # cell_constraints: list[list[list[CellConstraint]]] = [
    #     [[] for _ in range(w)] for _ in range(h)
    # ]
    lines = []
    for direction in [Direction.V, Direction.H]:
        key = definition.key_tate if direction == Direction.V else definition.key_yoko
        if direction == Direction.V:
            dx, dy = 0, 1
        elif direction == Direction.H:
            dx, dy = 1, 0
        for num, hint_text in key.items():
            line_id = f"{direction.value}{num}"
            if not num.isdecimal():
                raise ValueError("The key_tate keys must be a number.")
            num_int = int(num)
            y, x = _find_position(cells, num_int)
            start_position = (y, x)
            length = 0
            while True:
                cells[y][x].constraints.append(
                    CellConstraint(
                        line_id=line_id,
                        position=length,
                    )
                )
                x += dx
                y += dy
                length += 1
                v = cells[y][x]
                if v.cell_type == "x":
                    break
            lines.append(
                Line(
                    id=line_id,
                    start_position=start_position,
                    hint=hint_text,
                    length=length,
                    predicted_word="",
                )
            )
    return Crossword(
        h=h,
        w=w,
        cells=cells,
        lines=lines,
    )


def _find_position(
    cells: list[list[Cell]],
    num: int,
):
    for y, line in enumerate(cells):
        for x, value in enumerate(line):
            if value.cell_type == num:
                return y, x
    raise ValueError(f"Number {num} not found in cells.")


if __name__ == "__main__":
    try:
        input = json.loads(sys.stdin.read())
        definition = CrosswordDefinition(**input)
    except json.JSONDecodeError:
        print("stdin is not json")

    problem = parse_crossword_definition(definition)
    print(problem)
    print("processing...\n")
    for i in range(10):
        # print(f"################イテレーション:{i+1}")
        problem.clear_memo()
        # print(problem.state())
        # print("完了済みライン")
        # for l in problem.lines:
        #     if l.is_finalized(problem.cells):
        #         print("⭐" + l.get_hint(problem.cells))
        #         continue
        # print("予測")
        unfinalized_lines = [
            l for l in problem.lines if not l.is_finalized(problem.cells)
        ]
        pred = predict1(problem, unfinalized_lines)
        for p, line in zip(pred, unfinalized_lines):
            # print(f"{line.get_hint(problem.cells)}: {p}")
            line.fill_cells(problem.cells, p)
        # print(problem.state())
        problem.fill_answer()
        # print(problem.state())
        if problem.is_finished():
            print("completed")
            print(problem.state())
            break
        # print("-----未完了ライン")
        # for l in problem.lines:
        #     if l.is_finalized(problem.cells):
        #         continue
        #     print(l.get_hint(problem.cells))
