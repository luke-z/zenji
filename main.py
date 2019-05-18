import numpy as np


class Field():

    # 3: blocked flow, 2: outgoing flow, 1: incoming flow
    def __init__(self, u, r, d, l, rotations=0, parent=None, position=None):
        # directions with flow numbers up, right, down, left
        self.u = u
        self.r = r
        self.d = d
        self.l = l

        self.parent = parent
        # position in the grid as a tuple
        self.position = position
        # amount of rotations
        self.rotations = rotations

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.u == other.u and self.r == other.r and self.d == other.d and self.l == other.l and \
               self.position == other.position and self.rotations == other.rotations and self.parent == other.parent


def rotate(node, n):
    urdl = [node.u, node.r, node.d, node.l]
    # rotate the 4 directions right n times
    rotated = urdl[-n:] + urdl[:-n]
    return Field(rotated[0], rotated[1], rotated[2], rotated[3], rotations=n, parent=node.parent, position=node.position)


def astar(grid, start, end):

    # set the start node g, h and f
    start_node = start
    start_node.g = start_node.h = start_node.f = 0

    # set the end node g, h and f
    end_node = end
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    # create all rotations of the start node
    for rotation in range(4):
        rotated = rotate(start_node, rotation)

        # if the field has no exit downwards or to the right, skip it
        if rotated.r != 2 and rotated.d != 2:
            continue

        if rotated.d == 3 and rotated.r == 3:
            continue

        open_list.append(rotated)

    while len(open_list) > 0:

        # set the current_node to the the first open_list element from the left
        current_node = open_list[0]
        current_index = 0

        # check whether the f value of another open list node is smaller
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # mvoe the current_node to the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # check if the goal has been reached
        the_end = False
        if current_node.parent is not None:
            # calculate the previous move: (1,0) is a downwards move, (0,1) is a rightwards move
            previous_move = tuple(np.subtract(
                (current_node.position), (current_node.parent.position)))

            # the parent needs to have a 2 pipe going to a 1 pipe of the current node
            if previous_move == (1, 0):
                the_end = current_node.u == 1 and current_node.parent.d == 2
            if previous_move == (0, 1):
                the_end = current_node.l == 1 and current_node.parent.r == 2

        # if the end of the grid has been reached and the check above is true
        if current_node.position == end_node.position and the_end:
            path = []
            current = current_node
            # append the goal node
            path.append('Goal reached at position %s, rotated %s-times' %
                        (str(current.position), current.rotations))
            while current is not None:
                if current.parent is not None:
                    previous_move = tuple(np.subtract(
                        (current.position), (current.parent.position)))
                    # check previous move to create according string
                    if previous_move == (1, 0):
                        path.append('Rotate position %s %s-time(s), then go down' %
                                    (str(current.parent.position), current.parent.rotations))
                    if previous_move == (0, 1):
                        path.append('Rotate position %s %s-time(s), then go right' %
                                    (str(current.parent.position), current.parent.rotations))
                current = current.parent
            # invert path to have the correct order
            return path[::-1]

        children = []

        # each possible move (0,1) = right, (1,0) = down
        for new_position in [(0, 1), (1, 0)]:

            # calculate the new x, y coordinates using the current node
            new_position_x = current_node.position[0] + new_position[0]
            new_position_y = current_node.position[1] + new_position[1]

            # check if the new position is still in the grid
            if new_position_x > (len(grid) - 1) or new_position_x < 0 or new_position_y > (len(grid[len(grid) - 1]) - 1) or new_position_y < 0:
                continue

            # get the node at the calculated position
            node_new_pos = grid[new_position_x][new_position_y]

            # rotate the node in all directions
            for rotation in range(4):
                rotation_node = rotate(node_new_pos, rotation)

                # if the rotation node has no incoming flow from top or left, skip
                if rotation_node.l != 1 and rotation_node.u != 1:
                    continue

                # if the rotation node has no outgoing flow from bottom or right, skip
                if rotation_node.r != 2 and rotation_node.d != 2:
                    continue

                # if moved to the right, check if the left node has an outgoing flow to the right
                if new_position == (0, 1):
                    if current_node.r != 2:
                        continue

                # if moved to down, check if the top node has an outgoing flow to the bottom
                if new_position == (1, 0):
                    if current_node.d != 2:
                        continue

                # add the current_node as parent to the rotation node
                rotation_node.parent = current_node

                # append the rotated node to the list of children
                children.append(rotation_node)

        # iterate through each child
        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # the g value is increment by one
            child.g = current_node.g + 1
            # the h value consists of the sum of the x, y and amount of rotations of the child
            child.h = child.position[0] + child.position[1] + child.rotations
            # set f to be the sum of g and h
            child.f = child.g + child.h

            # if the child is already in the open node and has a greater g value, skip
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # add the child to the open list
            open_list.append(child)


def main():
    # 2x2 Field
    # fieldtl = Field(2, 1, 3, 2)
    # fieldtr = Field(2, 2, 1, 1)
    # fieldbl = Field(3, 1, 2, 3)
    # fieldbr = Field(2, 2, 3, 1)

    # grid = [[fieldtl, fieldtr],
    #         [fieldbl, fieldbr]]

    # 4x4 Field
    field00 = Field(2, 3, 3, 3)
    field01 = Field(2, 3, 1, 3)
    field02 = Field(2, 1, 3, 3)
    field03 = Field(3, 3, 3, 3)
    field10 = Field(3, 3, 3, 3)
    field11 = Field(3, 3, 3, 3)
    field12 = Field(2, 3, 3, 1)
    field13 = Field(3, 2, 1, 3)
    field20 = Field(3, 3, 3, 3)
    field21 = Field(3, 3, 3, 3)
    field22 = Field(3, 3, 3, 3)
    field23 = Field(3, 1, 3, 2)
    field30 = Field(3, 3, 3, 3)
    field31 = Field(3, 3, 3, 3)
    field32 = Field(3, 3, 3, 3)
    field33 = Field(2, 3, 3, 1)

    grid = [[field00, field01, field02, field03],
            [field10, field11, field12, field13],
            [field20, field21, field22, field23],
            [field30, field31, field32, field33]]

    # add all positions to the fields
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].position = (i, j)

    # set the start node to the node at (0,0)
    start = grid[0][0]
    # set the end node to the node at (m, n)
    end = grid[len(grid)-1][len(grid[len(grid) - 1]) - 1]

    # start the algorithm
    path = astar(grid, start, end)

    # print path
    for element in path:
        print(element)


# launcher
if __name__ == '__main__':
    main()
