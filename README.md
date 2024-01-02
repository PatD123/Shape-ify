# **Shape-ify**
A cool way to draw shapes (only rectangles at the moment) using just your hands!

Project relies on MediaPipe mainly to track the location of hands. From there, OpenCV is used to display all those
other kinds of shapes that the user wants (again, rectangles at the moment).

## About them Shapes
1. Each shape has it's own class that keeps track of its own coordinates, colors, line width, etc.
2. Once the shape is created, it can then be further selected by a certain hand gesture. When selected,
   the shape can be moved around, while updating its own states.

## Other features
1. Delete Button - After creating too many shapes, it allows the user to delete all the shapes created by them.