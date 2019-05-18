# Zenji - AI

This is a project for the AI module at BFH.
The goal was to solve a Zenji puzzle either iterative or with an A* algorithm.

This solution was implemented with an A* search.

## Nodes
A node represents one field on the grid, with the following flow capabilities:
  - 1: Flow is incoming
  - 2: Flow is outgoing
  - 3: Flow is blocked

Each node on the grid has the following attributes:
  - u (type of flow going up)
  - r (type of flow going right)
  - d (type of flow going down)
  - l (type of flow going left)
  - parent (previous node)
  - position (position on the grid, represented as a tuple)
  - rotations (amount node rotations to the right)
  - g
  - h
  - f