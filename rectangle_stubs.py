#!/usr/bin/env python3
"""
Generate detailed stubs for Rectangle and RectangleF.
Based on Microsoft .NET documentation + runtime introspection.
Skips 'inflate' and 'intersect' which crash the .NET wrapper.
"""
from pathlib import Path

RECTANGLE_STUB = '''class Rectangle:
    """
    Stores the location and size of a rectangular region.
    Wraps System.Drawing.Rectangle.

    See: https://learn.microsoft.com/en-us/dotnet/api/system.drawing.rectangle
    """

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Initialize a Rectangle with location and size.

        Args:
            x: The x-coordinate of the upper-left corner.
            y: The y-coordinate of the upper-left corner.
            width: The width of the rectangle.
            height: The height of the rectangle.
        """
        ...

    # Class methods / Static methods
    @staticmethod
    def empty() -> 'Rectangle':
        """Returns an empty Rectangle (all values zero)."""
        ...

    @staticmethod
    def from_ltrb(left: int, top: int, right: int, bottom: int) -> 'Rectangle':
        """
        Creates a Rectangle from left, top, right, and bottom coordinates.

        Args:
            left: The x-coordinate of the upper-left corner.
            top: The y-coordinate of the upper-left corner.
            right: The x-coordinate of the lower-right corner.
            bottom: The y-coordinate of the lower-right corner.
        """
        ...

    @staticmethod
    def ceiling(rect: 'RectangleF') -> 'Rectangle':
        """Converts a RectangleF to Rectangle by rounding up all values."""
        ...

    @staticmethod
    def truncate(rect: 'RectangleF') -> 'Rectangle':
        """Converts a RectangleF to Rectangle by truncating all values."""
        ...

    @staticmethod
    def round(rect: 'RectangleF') -> 'Rectangle':
        """Converts a RectangleF to Rectangle by rounding all values."""
        ...

    @staticmethod
    def union(a: 'Rectangle', b: 'Rectangle') -> 'Rectangle':
        """Returns the smallest rectangle that contains both input rectangles."""
        ...

    # Properties
    @property
    def x(self) -> int:
        """Gets or sets the x-coordinate of the upper-left corner."""
        ...

    @x.setter
    def x(self, value: int) -> None: ...

    @property
    def y(self) -> int:
        """Gets or sets the y-coordinate of the upper-left corner."""
        ...

    @y.setter
    def y(self, value: int) -> None: ...

    @property
    def width(self) -> int:
        """Gets or sets the width of the rectangle."""
        ...

    @width.setter
    def width(self, value: int) -> None: ...

    @property
    def height(self) -> int:
        """Gets or sets the height of the rectangle."""
        ...

    @height.setter
    def height(self, value: int) -> None: ...

    @property
    def left(self) -> int:
        """Gets the x-coordinate of the left edge. Same as X."""
        ...

    @property
    def top(self) -> int:
        """Gets the y-coordinate of the top edge. Same as Y."""
        ...

    @property
    def right(self) -> int:
        """Gets the x-coordinate of the right edge (X + Width)."""
        ...

    @property
    def bottom(self) -> int:
        """Gets the y-coordinate of the bottom edge (Y + Height)."""
        ...

    @property
    def location(self) -> 'Point':
        """Gets or sets the upper-left corner as a Point."""
        ...

    @location.setter
    def location(self, value: 'Point') -> None: ...

    @property
    def size(self) -> 'Size':
        """Gets or sets the size as a Size object."""
        ...

    @size.setter
    def size(self, value: 'Size') -> None: ...

    @property
    def is_empty(self) -> bool:
        """Returns True if all values are zero."""
        ...

    # Instance methods
    def contains(self, x: int, y: int) -> bool:
        """
        Determines if the specified point is within this rectangle.

        Overloads:
        - contains(x: int, y: int) -> bool
        - contains(pt: Point) -> bool
        - contains(rect: Rectangle) -> bool
        """
        ...

    def intersects_with(self, rect: 'Rectangle') -> bool:
        """Determines if this rectangle intersects with another."""
        ...

    def offset(self, x: int, y: int) -> None:
        """
        Adjusts the location by the specified amounts.

        Overloads:
        - offset(x: int, y: int) -> None
        - offset(pos: Point) -> None
        """
        ...

    def get_type(self) -> Any:
        """Returns the .NET Type object for Rectangle."""
        ...

    # NOTE: inflate() and intersect() crash the Python wrapper - use static alternatives
    # def inflate(self, width: int, height: int) -> None: ...
    # def intersect(self, rect: Rectangle) -> None: ...

'''

RECTANGLEF_STUB = '''class RectangleF:
    """
    Stores the location and size of a rectangular region using floats.
    Wraps System.Drawing.RectangleF.

    See: https://learn.microsoft.com/en-us/dotnet/api/system.drawing.rectanglef
    """

    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """
        Initialize a RectangleF with location and size.

        Args:
            x: The x-coordinate of the upper-left corner.
            y: The y-coordinate of the upper-left corner.
            width: The width of the rectangle.
            height: The height of the rectangle.
        """
        ...

    # Class methods / Static methods
    @staticmethod
    def empty() -> 'RectangleF':
        """Returns an empty RectangleF (all values zero)."""
        ...

    @staticmethod
    def from_ltrb(left: float, top: float, right: float, bottom: float) -> 'RectangleF':
        """
        Creates a RectangleF from left, top, right, and bottom coordinates.
        """
        ...

    @staticmethod
    def union(a: 'RectangleF', b: 'RectangleF') -> 'RectangleF':
        """Returns the smallest rectangle that contains both input rectangles."""
        ...

    # Properties
    @property
    def x(self) -> float:
        """Gets or sets the x-coordinate of the upper-left corner."""
        ...

    @x.setter
    def x(self, value: float) -> None: ...

    @property
    def y(self) -> float:
        """Gets or sets the y-coordinate of the upper-left corner."""
        ...

    @y.setter
    def y(self, value: float) -> None: ...

    @property
    def width(self) -> float:
        """Gets or sets the width of the rectangle."""
        ...

    @width.setter
    def width(self, value: float) -> None: ...

    @property
    def height(self) -> float:
        """Gets or sets the height of the rectangle."""
        ...

    @height.setter
    def height(self, value: float) -> None: ...

    @property
    def left(self) -> float:
        """Gets the x-coordinate of the left edge."""
        ...

    @property
    def top(self) -> float:
        """Gets the y-coordinate of the top edge."""
        ...

    @property
    def right(self) -> float:
        """Gets the x-coordinate of the right edge."""
        ...

    @property
    def bottom(self) -> float:
        """Gets the y-coordinate of the bottom edge."""
        ...

    @property
    def location(self) -> 'PointF':
        """Gets or sets the upper-left corner as a PointF."""
        ...

    @location.setter
    def location(self, value: 'PointF') -> None: ...

    @property
    def size(self) -> 'SizeF':
        """Gets or sets the size as a SizeF object."""
        ...

    @size.setter
    def size(self, value: 'SizeF') -> None: ...

    @property
    def is_empty(self) -> bool:
        """Returns True if all values are zero."""
        ...

    # Instance methods
    def contains(self, x: float, y: float) -> bool:
        """
        Determines if the specified point is within this rectangle.

        Overloads:
        - contains(x: float, y: float) -> bool
        - contains(pt: PointF) -> bool
        - contains(rect: RectangleF) -> bool
        """
        ...

    def intersects_with(self, rect: 'RectangleF') -> bool:
        """Determines if this rectangle intersects with another."""
        ...

    def offset(self, x: float, y: float) -> None:
        """Adjusts the location by the specified amounts."""
        ...

    def get_type(self) -> Any:
        """Returns the .NET Type object for RectangleF."""
        ...

    # NOTE: inflate() and intersect() crash the Python wrapper
    # def inflate(self, width: float, height: float) -> None: ...
    # def intersect(self, rect: RectangleF) -> None: ...

'''


def main():
    output_path = Path(__file__).parent / "generated_stubs" / "aspose" / "pydrawing" / "__init__.pyi"

    current = output_path.read_text()

    # Replace the simple Rectangle stub
    old_rect = """class Rectangle:
    '''Wrapper for System.Drawing.Rectangle'''
    def __init__(self, *args, **kwargs) -> None: ..."""

    old_rectf = """class RectangleF:
    '''Wrapper for System.Drawing.RectangleF'''
    def __init__(self, *args, **kwargs) -> None: ..."""

    current = current.replace(old_rect, RECTANGLE_STUB)
    current = current.replace(old_rectf, RECTANGLEF_STUB)

    output_path.write_text(current)
    print(f"Updated: {output_path}")

    # Count lines
    lines = len(current.splitlines())
    print(f"Total lines: {lines}")


if __name__ == "__main__":
    main()
