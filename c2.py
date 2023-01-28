from __future__ import annotations
import numpy as np


class Cube:
    _data = []

    def __init__(self):
        self._data = [np.int8(x) for x in range(0, 54)]
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
        if n < 9:
            return "Y"
        if n < 18:
            return "O"
        if n < 27:
            return "G"
        if n < 36:
            return "R"
        if n < 45:
            return "B"
        if n < 54:
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
            match cube_face.strip().lower():
                case "top":
                    index = 0
                case "up":
                    index = 0
                case "left":
                    index = 1
                case "back":
                    index = 2
                case "right":
                    index = 3
                case "front":
                    index = 4
                case "down":
                    index = 5
                case "bottom":
                    index = 5
        return index

    def _cube_face_index_to_name(self, cube_face: int) -> str:
        name = ""
        if (type(cube_face) == int):
            match cube_face:
                case 0:
                    name = "Up   "
                case 1:
                    name = "Left "
                case 2:
                    name = "Back "
                case 3:
                    name = "Right"
                case 4:
                    name = "Front"
                case 5:
                    name = "Down "
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
            match m.strip().lower():

                case "m'":
                    self.L().RP()
                case "m":
                    self.LP().R()
                case "m2":
                    self.L().L().R().R()

                case "u":
                    self.U()
                case "u'":
                    self.UP()
                case "u2":
                    self.U().U()

                case "l":
                    self.L()
                case "l'":
                    self.LP()
                case "l2":
                    self.L().L()

                case "b":
                    self.B()
                case "b'":
                    self.BP()
                case "b2":
                    self.B().B()

                case "r":
                    self.R()
                case "r'":
                    self.RP()
                case "r2":
                    self.R().R()

                case "f":
                    self.F()
                case "f'":
                    self.FP()
                case "f2":
                    self.F().F()

                case "d":
                    self.D()
                case "d'":
                    self.DP()
                case "d2":
                    self.D().D()

        return self


def main():
    cube = Cube()

    cube.BP().DP().R().R().L().BP().R().U().L().RP().BP().DP().FP().R().R().BP(
    ).RP().D().F().F().BP().DP().F().F().B().B().L().L().F().F().L().U().U()

    cube.print()


if __name__ == "__main__":
    main()
