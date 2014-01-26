# image_array.py
# Dexter Kozen (dck10) and Walker White (wmw2)
# October 26, 2012
"""This module provides the Model for our application.

It contains a single class.  Instances of this class support an
image that can be modified."""
from kivy.graphics.texture import Texture

import Image


class ImageArray(object):
    """An instance maintains a row-major order array of pixels for an image.

    Use the methods `getPixel` and `setPixel` to get and set the various
    pixels in this image.  Pixels are represented as 3-element tuples,
    with each element in the range 0..255.  For example, red is (255,0,0).

    These pixels are not RGB objects, like in Assignment 3.  They are tuples,
    which are lists that cannot be modified (so you can slice them to get new
    tuples, but not assign or append to them)."""

    # Fields
    _rows = 0     # Number of rows
    _cols = 0     # Number of columns
    _data = None  # List with image data

    # Immutable properties

    @property
    def rows(self):
        """The number of rows in this image

        *This attribute is set by the constructor and may not be altered*"""
        return self._rows

    @property
    def cols(self):
        """The number of columns in this image

        *This attribute is set by the constructor and may not be altered*"""
        return self._cols

    @property
    def len(self):
        """Length of pixel array

        *This attribute is set by the constructor and may not be altered*"""
        return len(self._data)

    @property
    def texture(self):
        """An OpenGL texture for this image (used for rendering)

        *This attribute is recomputed each time by the getter and may not be
        altered directly.*"""
        texture = Texture.create((self.cols,self.rows))
        buf = bytearray(0)
        for r in xrange(self.rows-1,-1,-1):
            for c in xrange(self.cols):
                pixel = self.getPixel(r,c)
                pixel = (pixel[0],pixel[1],pixel[2],255)
                buf.extend(pixel)
        buf = ''.join(map(chr, buf))
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @property
    def image(self):
        """An Image object for this ImageArray. Used to save results.

        *This attribute is recomputed each time by the getter and may not be
        altered directly.*"""
        im = Image.new('RGBA',(self.cols,self.rows))
        im.putdata(self._data)
        return im

    # Alternate Constructors

    @classmethod
    def LoadFile(cls,filename):
        """**Constructor** (alternate): Create an ImageArray for the given image file

            :param filename: image file to initialize array
            **Precondition**: a string representing an image file.

        If filename is not the name of a valid image file, this constructor will raise
        an exception."""
        assert type(filename) == str, `filename`+' is not a string'
        im = Image.open(filename)
        (c,r) = im.size
        self = cls(rows=r,cols=c,data=list(im.getdata()))
        return self

    @classmethod
    def Copy(cls,data):
        """**Constructor** (alternate): Create a copy of the given ImageArray

            :param data: image array to copy
            **Precondition**: an ImageArray object

        Once the copy is created, changes to the original will not affect
        this instance."""
        assert isinstance(data,ImageArray), `data`+' is not an ImageArray'
        self = ImageArray(rows=data.rows,cols=data.cols,data=data._data[:])
        return self

    # Built-in Methods

    def __init__(self, rows=0,cols=0,data=None):
        """**Constructor**: Create an ImageArray of the given size.

            :param rows: The number of rows in this image.
            **Precondition**: an int >= 0

            :param cols: The number of columns in this image.
            **Precondition**: an int >= 0

            :param data: The pixel array for this image.
            **Precondition**: an array of pixels (i.e. 3-element tuples,
            each element an int in 0..255) of size rows*cols

        In general, you should leave the parameter `data` as `None`. If
        you wish to initialize the image with some data, use one of the
        alternate constructors like `Copy` or `LoadFile`."""
        assert type(rows) == int and rows >= 0, `rows`+' is an invalid argument'
        assert type(cols) == int and cols >= 0, `cols`+' is an invalid argument'
        assert data is None or type(data) == list, `data`+' is an invalid buffer'
        if not data is None:
            assert len(data) == rows*cols, `data`+' is an invalid size'

        self._rows = rows
        self._cols = cols
        if data is None:
            self._data = [(0,0,0)]*(rows*cols)
        else:
            self._data = data

    # Normal Methods

    def getPixel(self, row, col):
        """**Returns**: The pixel value at (row, col)

            :param row: The pixel row
            **Precondition**: an int for a valid pixel row

            :param col: The pixel col
            **Precondition**: an int for a valid pixel column

        Value returned is an 3-element tuple (r,g,b).

        This method does not enforce the preconditions; that
        is the responsibility of the user."""
        #assert type(row) == int and row >= 0 and row < self._rows, `row`+' is an invalid row'
        #assert type(col) == int and col >= 0 and col < self._cols, `col`+' is an invalid column'
        return self._data[row*self.cols + col]

    def setPixel(self, row, col, pixel):
        """Sets the pixel value at (row, col) to pixel

            :param row: The pixel row
            **Precondition**: an int for a valid pixel row

            :param col: The pixel column
            **Precondition**: an int for a valid pixel column

            :param pixel: The pixel value
            **Precondition**: a 3-element tuple (r,g,b) where each
            value is 0..255

        This method does not enforce the preconditions; that
        is the responsibility of the user."""
        #assert type(row) == int and row >= 0 and row < self._rows, `row`+' is an invalid row'
        #assert type(col) == int and col >= 0 and col < self._cols, `col`+' is an invalid column'
        #assert type(pixel) == tuple and len(tuple) == 3, `pixel`+' is not a 3-element tuple'
        #assert type(pixel[0]) == int and 0 <= pixel[0] and pixel[0] < 256, `pixel[0]`+' is an invalid red value'
        #assert type(pixel[1]) == int and 0 <= pixel[1] and pixel[1] < 256, `pixel[1]`+' is an invalid green value'
        #assert type(pixel[2]) == int and 0 <= pixel[2] and pixel[2] < 256, `pixel[2]`+' is an invalid blue value'
        self._data[row*self.cols + col] = pixel

    def swapPixels(self, row1, col1, row2, col2):
        """Swaps the pixel at (row1, col1) with the pixel at (row2, col2)

            :param row1: The pixel row to swap from
            **Precondition**: an int for a valid pixel row

            :param row2: The pixel row to swap to
            **Precondition**: an int for a valid pixel row

            :param col1: The pixel column to swap from
            **Precondition**: an int for a valid pixel column

            :param col2: The pixel column to swap to
            **Precondition**: an int for a valid pixel column

        Preconditions are enforced only if enforced in `getPixel`, `setPixel`."""
        temp = self.getPixel(row1, col1)
        self.setPixel(row1, col1, self.getPixel(row2, col2))
        self.setPixel(row2, col2, temp)

    def getFlatPixel(self, n):
        """**Returns**: Pixel number n of the image (in row major order)

            :param n: The pixel number to access
            **Precondition**: an int in 0..(length of the image buffer - 1)

        This method is used when you want to treat an image as a flat,
        one-dimensional list rather than a 2-dimensional image.  It is useful
        for the steganography part of the assignment.

        Value returned is a 3-element tuple (r,g,b).

        This method does not enforce the preconditions; that
        is the responsibility of the user."""
        assert type(n) == int and n >=0 and n < self.len, `n`+' is an invalid pixel position'
        return self._data[n]

    def setFlatPixel(self, n, pixel):
        """Sets pixel number n of the image (in row major order) to pixel

            :param n: The pixel number to access
            **Precondition**: an int in 0..(length of the image buffer - 1)

            :param pixel: The pixel value
            **Precondition**: a 3-element tuple (r,g,b) where each
            value is 0..255

        This method is used when you want to treat an image as a flat,
        one-dimensional list rather than a 2-dimensional image.  It is useful
        for the steganography part of the assignment.

        This method does not enforce the preconditions; that
        is the responsibility of the user."""
        #assert type(n) == int and n >=0 and n < self.len, `n`+' is an invalid pixel position'
        #assert type(pixel) == tuple and len(tuple) == 3, `pixel`+' is not a 3-element tuple'
        #assert type(pixel[0]) == int and 0 <= pixel[0] and pixel[0] < 256, `pixel[0]`+' is an invalid red value'
        #assert type(pixel[1]) == int and 0 <= pixel[1] and pixel[1] < 256, `pixel[1]`+' is an invalid green value'
        #assert type(pixel[2]) == int and 0 <= pixel[2] and pixel[2] < 256, `pixel[2]`+' is an invalid blue value'
        self._data[n] = pixel
