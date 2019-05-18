import numpy as np

class Field():

    def __init__(self, u, r, d, l, rotations=0, parent=None, position=None):
        self.u = u
        self.r = r
        self.d = d
        self.l = l

        self.parent = parent
        self.position = position
        self.rotations = rotations

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.u == other.u and self.r == other.r and self.d == other.d and self.l == other.l and self.position == other.position and self.rotations == other.rotations and self.parent == other.parent


def rotate(node, n):
    urdl = [node.u, node.r, node.d, node.l]
    rotated = urdl[-n:] + urdl[:-n]
    return Field(rotated[0], rotated[1], rotated[2], rotated[3], rotations=n, parent=node.parent, position=node.position)


def astar(grid, start, end):
    start_node = start
    start_node.g = start_node.h = start_node.f = 0

    end_node = end
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    for rotation in range(4):
        rotated = rotate(start_node, rotation)

        if rotated.r != 2 and rotated.d !=2:
            continue

        open_list.append(rotated)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        the_end = False
        if current_node.parent is not None:
            previous_move = tuple(np.subtract((current_node.position),(current_node.parent.position)))
            if previous_move == (1,0):
                the_end = current_node.u == 1 and current_node.parent.d == 2
            if previous_move == (0,1):
                the_end = current_node.l == 1 and current_node.parent.r == 2

        if current_node.position == end_node.position and the_end:
            path = []
            current = current_node
            path.append('Goal reached at position %s, rotated %s-times' % (str(current.position), current.rotations))
            while current is not None:
                if current.parent is not None:
                    previous_move = tuple(np.subtract((current.position),(current.parent.position)))
                    if previous_move == (1,0):
                        path.append('Rotate position %s %s-time(s), then go down' % (str(current.parent.position), current.parent.rotations))
                    if previous_move == (0,1):
                        path.append('Rotate position %s %s-time(s), then go right' % (str(current.parent.position), current.parent.rotations))
                current = current.parent

            return path[::-1]

        children = []

        for new_position in [(0, 1), (1, 0)]:

            new_position_x = current_node.position[0] + new_position[0]
            new_position_y = current_node.position[1] + new_position[1]

            if new_position_x > (len(grid) - 1) or new_position_x < 0 or new_position_y > (len(grid[len(grid) - 1]) - 1) or new_position_y < 0:
                continue

            node_new_pos = grid[new_position_x][new_position_y]

            for rotation in range(4):
                rotation_node = rotate(node_new_pos, rotation)

                if new_position == (0, 1) and rotation_node.l != 1 and current_node.r != 2:
                    continue

                if new_position == (1, 0) and rotation_node.u != 1 and current_node.d != 2:
                    continue

                rotation_node.parent=current_node

                # if new_position == (0, 1):
                #     if current_node.r == 3 or rotation_node.l == 3:
                #         continue
                #     print("right expansion: ", current_node.r, rotation_node.l)

                # if new_position == (0, 1):
                #     if current_node.d == 3 or rotation_node.u == 3:
                #         continue
                #     print("downwards expansion: ", current_node.d, rotation_node.u)

                children.append(rotation_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)


def main():
    ## 2x2 Field
    # fieldtl = Field(2, 1, 3, 2)
    # fieldtr = Field(2, 2, 1, 1)
    # fieldbl = Field(3, 1, 2, 3)
    # fieldbr = Field(2, 2, 3, 1)

    # grid = [[fieldtl, fieldtr],
    #         [fieldbl, fieldbr]]

    ## 4x4 Field
    field00 = Field(2,3,3,3)
    field01 = Field(2,3,1,3)
    field02 = Field(2,1,3,3)
    field03 = Field(3,3,3,3)
    field10 = Field(3,3,3,3)
    field11 = Field(3,3,3,3)
    field12 = Field(2,3,3,1)
    field13 = Field(3,2,1,3)
    field20 = Field(3,3,3,3)
    field21 = Field(3,3,3,3)
    field22 = Field(3,3,3,3)
    field23 = Field(3,1,3,2)
    field30 = Field(3,3,3,3)
    field31 = Field(3,3,3,3)
    field32 = Field(3,3,3,3)
    field33 = Field(2,3,3,1)

    grid = [[field00, field01, field02, field03],
            [field10, field11, field12, field13],
            [field20, field21, field22, field23],
            [field30, field31, field32, field33]]



    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].position = (i, j)

    start = grid[0][0]
    end = grid[len(grid)-1][len(grid[len(grid) - 1]) - 1]

    path = astar(grid, start, end)

    for element in path:
        print(element)


if __name__ == '__main__':
    main()
