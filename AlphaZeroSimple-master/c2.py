from __future__ import annotations
import numpy as np


class Cube:

    def __init__(self, full_info=False):
        self.full_info = full_info
        self._data = [np.int8(x if full_info else np.floor(x/9.))
                      for x in range(0, 54)]
        # print("init data:", self._data)
        self.total_moves = 0

    # Front

    def _rot_face(self, cube_face):
        self.total_moves += 1
        old_left = self.get_strip(cube_face, "col", 0)
        self.set_strip(cube_face, "col", 0,
                       self.get_strip(cube_face, "row", 2))
        self.set_strip(cube_face, "row", 2, list(
            reversed(self.get_strip(cube_face, "col", 2))
        ))
        self.set_strip(cube_face, "col", 2,
                       self.get_strip(cube_face, "row", 0))
        self.set_strip(cube_face, "row", 0, list(
            reversed(old_left)
        ))

    def _rot_face_p(self, cube_face):
        self.total_moves += 1
        old_left = self.get_strip(cube_face, "col", 0)
        self.set_strip(cube_face, "col", 0, list(
            reversed(self.get_strip(cube_face, "row", 0))
        ))
        self.set_strip(cube_face, "row", 0,
                       self.get_strip(cube_face, "col", 2))
        self.set_strip(cube_face, "col", 2, list(
            reversed(self.get_strip(cube_face, "row", 2))
        ))
        self.set_strip(cube_face, "row", 2, old_left)

    def F(self) -> Cube:
        self._rot_face("front")
        old_left = self.get_strip("left", "col", 2)
        # Left rightmost col becomes what bottom topmost row was
        self.set_strip("left", "col", 2, self.get_strip("bottom", "row", 0))
        self.set_strip("bottom", "row", 0, list(
            reversed(self.get_strip("right", "col", 0))))
        self.set_strip("right", "col", 0, self.get_strip("top", "row", 2))
        self.set_strip("top", "row", 2, list(reversed(old_left)))
        return self

    def FP(self) -> Cube:
        self._rot_face_p("front")
        old_left = self.get_strip("left", "col", 2)
        # Left rightmost col becomes what top topmost row was
        self.set_strip("left", "col", 2, list(
            reversed(self.get_strip("top", "row", 2))))
        self.set_strip("top", "row", 2, self.get_strip("right", "col", 0))
        self.set_strip("right", "col", 0, list(
            reversed(self.get_strip("bottom", "row", 0))))
        self.set_strip("bottom", "row", 0, old_left)
        return self

    # Back
    def B(self) -> Cube:
        self._rot_face("back")
        old_left = self.get_strip("left", "col", 0)
        # Left rightmost col becomes what top topmost row was
        self.set_strip("left", "col", 0, list(
            reversed(self.get_strip("top", "row", 0))))
        self.set_strip("top", "row", 0, self.get_strip("right", "col", 2))
        self.set_strip("right", "col", 2, list(
            reversed(self.get_strip("bottom", "row", 2))))
        self.set_strip("bottom", "row", 2, old_left)
        return self

    def BP(self) -> Cube:
        self._rot_face_p("back")
        old_left = self.get_strip("left", "col", 0)
        # Left rightmost col becomes what bottom topmost row was
        self.set_strip("left", "col", 0, self.get_strip("bottom", "row", 2))
        self.set_strip("bottom", "row", 2, list(
            reversed(self.get_strip("right", "col", 2))))
        self.set_strip("right", "col", 2, self.get_strip("top", "row", 0))
        self.set_strip("top", "row", 0, list(reversed(old_left)))
        return self

    # Top
    def U(self) -> Cube:
        self._rot_face("up")
        old_front = self.get_strip("front", "row", 0)
        # Front topmost row becomes what right topmost row was
        self.set_strip("front", "row", 0, self.get_strip("right", "row", 0))
        self.set_strip("right", "row", 0, list(
            reversed(self.get_strip("back", "row", 2))))
        self.set_strip("back", "row", 2, list(
            reversed(self.get_strip("left", "row", 0))))
        self.set_strip("left", "row", 0, old_front)
        return self

    def UP(self) -> Cube:
        self._rot_face_p("up")
        old_front = self.get_strip("front", "row", 0)
        # Front topmost row becomes what right topmost row was
        self.set_strip("front", "row", 0, self.get_strip("left", "row", 0))
        self.set_strip("left", "row", 0, list(
            reversed(self.get_strip("back", "row", 2))))
        self.set_strip("back", "row", 2, list(
            reversed(self.get_strip("right", "row", 0))))
        self.set_strip("right", "row", 0, old_front)
        return self

    # Down
    def D(self) -> Cube:
        self._rot_face("down")
        old_front = self.get_strip("front", "row", 2)
        # Front bottommost row becomes what right bottommost row was
        self.set_strip("front", "row", 2, self.get_strip("left", "row", 2))
        self.set_strip("left", "row", 2, list(
            reversed(self.get_strip("back", "row", 0))))
        self.set_strip("back", "row", 0, list(
            reversed(self.get_strip("right", "row", 2))))
        self.set_strip("right", "row", 2, old_front)
        return self

    def DP(self) -> Cube:
        self._rot_face_p("down")
        old_front = self.get_strip("front", "row", 2)
        # Front topmost row becomes what right topmost row was
        self.set_strip("front", "row", 2, self.get_strip("right", "row", 2))
        self.set_strip("right", "row", 2, list(
            reversed(self.get_strip("back", "row", 0))))
        self.set_strip("back", "row", 0, list(
            reversed(self.get_strip("left", "row", 2))))
        self.set_strip("left", "row", 2, old_front)
        return self

    # Right
    def R(self) -> Cube:
        self._rot_face("right")
        old_top = self.get_strip("top", "col", 2)
        # Top rightmost column becomes what front rightmost column was
        self.set_strip("top", "col", 2, self.get_strip("front", "col", 2))
        self.set_strip("front", "col", 2, self.get_strip("bottom", "col", 2))
        self.set_strip("bottom", "col", 2, self.get_strip("back", "col", 2))
        self.set_strip("back", "col", 2, old_top)
        return self

    def RP(self) -> Cube:
        self._rot_face_p("right")
        old_top = self.get_strip("top", "col", 2)
        self.set_strip("top", "col", 2, self.get_strip("back", "col", 2))
        self.set_strip("back", "col", 2, self.get_strip("bottom", "col", 2))
        self.set_strip("bottom", "col", 2, self.get_strip("front", "col", 2))
        self.set_strip("front", "col", 2, old_top)
        return self

    # Left
    def L(self) -> Cube:
        self._rot_face("left")
        old_top = self.get_strip("top", "col", 0)
        self.set_strip("top", "col", 0, self.get_strip("back", "col", 0))
        self.set_strip("back", "col", 0, self.get_strip("bottom", "col", 0))
        self.set_strip("bottom", "col", 0, self.get_strip("front", "col", 0))
        self.set_strip("front", "col", 0, old_top)
        return self

    def LP(self) -> Cube:
        self._rot_face_p("left")
        old_top = self.get_strip("top", "col", 0)
        # Top leftmost column becomes what front leftmost column was
        self.set_strip("top", "col", 0, self.get_strip("front", "col", 0))
        self.set_strip("front", "col", 0, self.get_strip("bottom", "col", 0))
        self.set_strip("bottom", "col", 0, self.get_strip("back", "col", 0))
        self.set_strip("back", "col", 0, old_top)
        return self

    def get_color(self, n) -> str:
        if self.full_info:
            if n < 9:
                return "Y"
            elif n < 18:
                return "O"
            elif n < 27:
                return "G"
            elif n < 36:
                return "R"
            elif n < 45:
                return "B"
            elif n < 54:
                return "W"
        else:
            if n == 0:
                return "Y"
            elif n == 1:
                return "O"
            elif n == 2:
                return "G"
            elif n == 3:
                return "R"
            elif n == 4:
                return "B"
            elif n == 5:
                return "W"

    def print(self, colors: bool | str = True) -> None:
        space = 17
        if colors == True:
            space = 15

        print(self._inset_fmt(self.format_cube_face(0, colors), space), end="")
        print(
            self._stitch_fmt(
                self._stitch_fmt(
                    self._stitch_fmt(self.format_cube_face(1, colors),
                                     self.format_cube_face(2, colors)),
                    self.format_cube_face(3, colors)
                ),
                self.format_cube_face(4, colors)
            ),
            end="")

        print(self._inset_fmt(self.format_cube_face(5, colors), space))

    def _cube_face_name_to_index(self, cube_face: str | int) -> int:
        index = cube_face
        if type(cube_face) == str:
            matchDict = {
                "top": 0,
                "up": 0,
                "left": 1,
                "back": 2,
                "right": 3,
                "front": 4,
                "down": 5,
                "bottom": 5
            }
            index = matchDict[cube_face.strip().lower()]

        return index

    def _cube_face_index_to_name(self, cube_face: int) -> str:
        name = ""
        if (type(cube_face) == int):

            matchDict = {
                0: "Up   ",
                1: "Left ",
                2: "Back ",
                3: "Right",
                4: "Front",
                5: "Down "
            }
            name = matchDict[cube_face]
        return name

    def _inset_fmt(self, L, amt) -> str:
        return ("".join([" "]*amt)+L.replace("\n", "\n"+"".join([" "]*amt)))[:-amt]

    def _stitch_fmt(self, L1, L2) -> str:
        sL1 = L1.split("\n")
        sL2 = L2.split("\n")
        nL = ""
        for n in range(0, len(sL1)-1):
            nL += sL1[n] + " " + sL2[n] + "\n"

        return nL

    def format_cube_face(self, n: int | str, show_colors: bool | str = True) -> str:
        show_both = False
        if show_colors == "both":
            show_both = True
            show_colors = False
        L = self.cube_face(n)
        # len(str(max(L))) if not show_colors else 1
        maxL = 1 if show_colors else 2

        def spaces(x): return " ".join(
            [""]*(
                maxL-len(str(x))+2 if not show_colors else 2
            )
        )

        ret = "║ " + \
            self._cube_face_index_to_name(n) + \
            " ".join([""]*(6 if show_colors else 7))+spaces(maxL) + "║" + \
            "\n"+"┌"+"──".join([""]*(7 if show_colors else 8))+"┐"+"\n"

        def id_both_transform(x):
            return self.get_color(x) + str(x % 9)

        id_transform = id_both_transform if show_both else self.get_color if show_colors else lambda x: str(
            x)

        for x in range(0, 3):
            id1 = id_transform(L[3*x])
            id2 = id_transform(L[3*x+1])
            id3 = id_transform(L[3*x+2])

            ret += "│ " + id1 + spaces(id1) + \
                "│ " + id2 + spaces(id2) + \
                "│ " + id3 + spaces(id3) + (" " if show_colors else "") + "│\n"

        ret += "└" + "──".join([""]*(7 if show_colors else 8)) + "┘\n"
        return ret

    def cube_face(self, n: int | str) -> list[int]:
        n = self._cube_face_name_to_index(n)
        ret = []
        for x in range((n+1)*9-9, (n+1)*9):
            ret.append(self._data[x])
        return ret

    def set(self, cube_face: int | str, index: int, val: int) -> None:
        cube_face = self._cube_face_name_to_index(cube_face)

        self._data[(cube_face+1)*9-9+index] = val

    def get(self, cube_face: int | str, index: int) -> None:
        cube_face = self._cube_face_name_to_index(cube_face)

        return self._data[(cube_face+1)*9-9+index]

    def _column_to_bool(self, column: bool | str) -> bool:
        if type(column) == str:
            if column == "row":
                column = False
            elif column == "col":
                column = True
            elif column == "column":
                column = True
            else:
                column = False
        return column

    def get_strip(self, cube_face: int | str, column: bool | str, index: int) -> list[int]:
        column = self._column_to_bool(column)
        cube_face = self._cube_face_name_to_index(cube_face)

        L_offset = (cube_face+1)*9-9

        if not column:
            return self._data[L_offset + 3*(index+1) - 3: L_offset + 3*(index+1)]
        else:
            return [self._data[L_offset+3*x+index] for x in range(0, 3)]

    def set_strip(self, cube_face: int | str, column: bool | str, index: int, values: list[int]) -> None:
        column = self._column_to_bool(column)
        cube_face = self._cube_face_name_to_index(cube_face)

        L_offset = (cube_face+1)*9-9

        if not column:
            self._data[
                L_offset + 3*(index+1) - 3: L_offset + 3*(index+1)
            ] = values
        else:
            for x in range(0, 3):
                self._data[L_offset+3*x+index] = values[x]

    def moves(self, moveset: str) -> Cube:
        for m in moveset.split(" "):
            m = m.strip().lower()
            if m == "m'":
                self.L().RP()
            if m == "m":
                self.LP().R()
            elif m == "m2":
                self.L().L().R().R()

            elif m == "u":
                self.U()
            elif m == "u'":
                self.UP()
            elif m == "u2":
                self.U().U()

            elif m == "l":
                self.L()
            elif m == "l'":
                self.LP()
            elif m == "l2":
                self.L().L()

            elif m == "b":
                self.B()
            elif m == "b'":
                self.BP()
            elif m == "b2":
                self.B().B()

            elif m == "r":
                self.R()
            elif m == "r'":
                self.RP()
            elif m == "r2":
                self.R().R()

            elif m == "f":
                self.F()
            elif m == "f'":
                self.FP()
            elif m == "f2":
                self.F().F()

            elif m == "d":
                self.D()
            elif m == "d'":
                self.DP()
            elif m == "d2":
                self.D().D()

        return self


def main():
    cube = Cube()

    print("data:", cube._data)
    cube.BP().DP().R().R().L().BP().R().U().L().RP().BP().DP().FP().R().R().BP(
    ).RP().D().F().F().BP().DP().F().F().B().B().L().L().F().F().L().U().U()

    cube.print()


if __name__ == "__main__":
    main()
