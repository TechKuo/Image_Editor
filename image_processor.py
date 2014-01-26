# image_processor.py
# Charles Lai(cjl223) and Tech Kuo(thk42)
# 11-16-12
from image_array import ImageArray
from math import *
"""Secondary Controller module for Imager Application

This module provides all of the image processing operations that
are called whenever you press a button.  All other controller
functionality (loading files, etc.) is provided in imager.py"""

# GLOBAL CONSTANTS
GRAY = 0
SEPIA = 1


class ImageProcessor(object):
    """Instance is a collection of image transforms"""
    # Fields
    _current  = None # Current image being manipulated
    _original = None # Original image, may not be changed.

    # Immutable Attributes
    @property
    def original(self):
        """The original state of the image in this processor.

        *This attribute is set by the constructor and may not be altered*"""
        return self._original

    # Mutable Attributes
    @property
    def current(self):
        """The original state of the image in this processor.

        **Invariant**: Must be an ImageArray"""
        return self._current

    @current.setter
    def current(self,value):
        assert isinstance(value,ImageArray), `value`+' is not an ImageArray'
        self._current = value

    # Built-in Methods

    def __init__(self, image_array):
        """**Constructor**: Create an ImageProcessor for the given image.

            :param image: The image to process.
            **Precondition**: an ImageArray object

        Attribute `original` is a direct reference to `image_array`.
        However, attribute `current` is a copy of that ImageArray."""
        self._original = image_array
        self._current  = ImageArray.Copy(image_array)

    def restore(self):
        """Restore the original image"""
        self._current = ImageArray.Copy(self.original)

    def invert(self):
        """Invert the current image, replacing each element with its color
        complement"""
        n = 0
        # Invariant: pixels 0..n-1 have been inverted in self.current
        while n < self.current.len:
            rgb = self.current.getFlatPixel(n)
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue) # New pixel value
            self.current.setFlatPixel(n, rgb)
            n = n + 1 # Remember to increment

    def transpose(self):
        """Transpose the current image

        Follow this plan:

            Create a new ImageArray ia, which has no data (it is an empty
            image), but which has the number of rows and columns swapped
            from their current values in self.current

            Store the transpose of self.current in ia, using self.current's
            `getPixel` function and ia's `setPixel` function.

            Assign ia to self.current.

        The transposed image will be drawn on the screen immediately afterwards."""
        ia = ImageArray(rows=self.current.cols,cols=self.current.rows)
        r = 0
        # Invariant: rows 0..r-1 have been copied to ia[.., 0..r-1]
        while r < ia.rows:
            c = 0
            # Invariant: elements [r,0..c-1] have been copied to ia[0..c-1, r]
            while c < ia.cols:
                ia.setPixel(r, c, self.current.getPixel(c, r))
                c = c + 1 # Remember to increment
            r = r + 1 # Remember to increment

        # Replace the image
        self.current = ia

    def horizReflect(self):
        """ Reflect the current image around a vertical line through
        the middle of the image."""
        h = 0
        k = self.current.cols-1
        # Invariant: cols 0..h-1 and k+1.. have been swapped
        while h < k:
            r = 0
            # Invariant: pixels 0..r-1 of cols h and k have been swapped
            while r < self.current.rows:
                self.current.swapPixels(r, h, r, k)
                r = r + 1 # Remember to increment
            # Must change two variables to satisfy invariant
            h = h + 1 # Move h forward
            k = k - 1 # Move k backward

    def rotateLeft(self):
        """Rotate the image left via a transpose, followed by a vertical reflection."""
        self.transpose()
        self.vertReflect()

    def rotateRight(self):
        """Rotate the image right via a transpose, followed by a horizontal reflection."""
        self.transpose()
        self.horizReflect()

    # Student defined
    def vertReflect(self):
        """ Reflect the current image around a horizontal line through
        the middle of the image."""
        h = 0
        k = self.current.rows-1
        while h < k:
            c = 0
            while c < self.current.cols:
                self.current.swapPixels(h, c, k, c)
                c = c + 1 
            h = h + 1
            k = k - 1 

    def jail(self):
        """Put jail bars on the current image:

        Put 3-pixel-wide horizontal bars across top and bottom,

        Put 4-pixel vertical bars down left and right, and

        Put n 4-pixel vertical bars inside, where n is (number of columns - 8) / 50.

        The n+2 vertical bars should be as evenly spaced as possible."""
        #draw horizontal bars
        self._drawHBar(0, (255,0,0))
        self._drawHBar(self.current.rows-3, (255,0,0))
        
        #draw vertical bars
        self._drawVBar(0, (255,0,0))
        self._drawVBar(self.current.cols-4, (255,0,0))
        n = (self.current.cols-8)/50
        spacing = (self.current.cols)/float(n)
        pos = spacing
        while pos <= self.current.cols-4:
            self._drawVBar(int(round(pos)), (255,0,0))
            pos+=spacing

    def _drawHBar(self, row, pixel):
        """Helper function for jail.

            :param row: The start of the row to draw the bar
            **Precondition**: 0 <= row  and  row+2 < self.current.rows an int

            :param pixel: The pixel color to use
            **Precondition**: a 3-element tuple (r,g,b) where each
            value is 0..255

        Draw a horizontal 3-pixel-wide bar at row `row` of the current
        image. So the bar is at rows row, row+1, and row+2. The bar
        uses the color given by the given rgb components."""
        col = 0
        # Invariant: pixels self.current[row..row+2][0..col-1] are color pixel
        while col < self.current.cols:
            self.current.setPixel(row,   col, pixel)
            self.current.setPixel(row+1, col, pixel)
            self.current.setPixel(row+2, col, pixel)
            col = col + 1 # Remember to increment

    def _drawVBar(self, col, pixel):
        """Helper function for jail.

            :param col: The start of the column to draw the bar
            **Precondition**: col >= 0  and  self.current.cols < col + 3 and col is an int

            :param pixel: The pixel color to use
            **Precondition**: a 3-element tuple (r,g,b) where each
            value is 0..255

        Draw a vertical 4-pixel-wide bar at col `col` of the current
        image. The bar uses the color given by the given rgb components."""
        row = 0
        while row < self.current.rows:
            self.current.setPixel(row,   col,   pixel)
            self.current.setPixel(row,   col+1, pixel)
            self.current.setPixel(row,   col+2, pixel)
            self.current.setPixel(row,   col+3, pixel)
            row = row + 1 

    def monochromify(self, color):
        """Convert the current image to monochrome according to parameter color.

            :param color: Monochrome color choice
            **Precondition**: an int equal to either the global constant `GRAY`
            or the global constant `SEPIA`

        If color is `GRAY`, then remove all color from the image by setting the
        three color components of each pixel to (an int corresponding to) that
        pixel's overall brightness, defined as
        0.3 * red + 0.6 * green + 0.1 * blue.

        If color is `SEPIA`, make the same computation but set green to
        int(0.6 * brightness) and blue to int(0.4 * brightness)."""
        assert color == GRAY or color == SEPIA, 'invalid color parameter'
        n = 0
        if color == GRAY:
            while n < self.current.len:
                rgb = self.current.getFlatPixel(n)
                brightness = rgb[0]*.3 + rgb[1]*.6 + rgb[2]*.1
                red = int(brightness)
                green = int(brightness)
                blue  = int(brightness)
                rgb = (red,green,blue) 
                self.current.setFlatPixel(n, rgb)
                n = n + 1
        
        if color == SEPIA:
            while n < self.current.len:
                rgb = self.current.getFlatPixel(n)
                brightness = rgb[0]*.3 + rgb[1]*.6 + rgb[2]*.1
                red = rgb[0]
                green = int(.6*brightness)
                blue = int(.4*brightness)
                rgb = (red,green,blue) 
                self.current.setFlatPixel(n, rgb)
                n = n + 1

    def vignette(self):
        """Simulate vignetting (corner darkening) characteristic of antique lenses.

        Darken each pixel in the image by the factor

            (d / hfD)^2

        where d is the distance from the pixel to the center of the image and
        hfD (for half diagonal) is the distance from the center of the image
        to any of the corners."""
        rows = float(self.current.rows) 
        cols = float(self.current.cols) 
        r = 0
        c = 0
        hfD = sqrt((((self.current.rows-1)/2)**2)+(((self.current.cols-1)/2)**2))
        while c < cols:
            while r < rows:
                d = sqrt(((((self.current.rows-1)/2)-r)**2)+((((self.current.cols-1)/2)-c)**2))
                rgb = self.current.getPixel(r,c)
                modifier = 1 - d**2/hfD**2
                red = int(rgb[0]*modifier)
                green = int(rgb[1]*modifier)
                blue = int(rgb[2]*modifier)
                rgb = (red,green,blue) 
                self.current.setPixel(r, c, rgb)
                r+=1
            r = 0
            c+=1

    def decode(self, p):
        """**Return**: the number n that is hidden in pixel p of the current image.

            :param p: a pixel position
            **Precondition**: pixel position is valid
            (i.e. 0 <= p < self.current.len)

        This function assumes that n is a 3-digit number encoded as the
        last digit in each color channel (i.e., red, green and blue)."""
        rgb = self.current.getFlatPixel(p)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return (red % 10) * 100  +  (green % 10) * 10  +  blue % 10

    def encode(self, n, p):
        """Encode integer n in pixel number p of the current image.

            :param n: a number to hide
            **Precondition**: an int with 0 <= n < 1000

            :param p: a pixel position
            **Precondition**: pixel position is valid
            (i.e. 0 <= p < self.current.len)

        This function encodes a three digit number by adding (or otherwise
        changing) a single digit to each color channel (i.e., red, green and
        blue)."""
        
        n = self._pad3(n)
        rgb = self.current.getFlatPixel(p)
        red   = rgb[0] - (rgb[0]%10) + int(n[0])
        green = rgb[1] - (rgb[1]%10) + int(n[1])
        blue  = rgb[2] - (rgb[2]%10) + int(n[2])
        if red > 255:
            red = red-10
        if green > 255:
            green = green - 10
        if blue > 255:
            blue = blue - 10
        rgb = (red, green, blue)
        self.current.setFlatPixel(p, rgb)

    def hide(self, text):
        """Hide message text in this image, using the ASCII representation of
        text's characters.

        **Return**: True if message hiding possible, and False if not.

            :param text: a message to hide
            **Precondition**: a string

        If m has more than 999999 characters or the picture does not have enough
        pixels, return False without storing the message."""
        lcounter = 0
        tcounter = 0
        pcounter = 3
        length = len(text)
        print self.getPixels(length)
        if length > 999999 or length>self.current.len-4:
            return False
        self.encode(ord('y'),0)
        self.encode(ord('e'),1)
        self.encode(ord('s'),2)
        lengthString = str(length)
        for e in range(len(lengthString)):
            self.encode(ord(lengthString[e]),pcounter)
            pcounter += 1
        self.encode(ord('x'),pcounter)
        pcounter+=1
        while length > 0:
            textnumber = ord((text[tcounter]))
            self.encode(textnumber, pcounter )
            length-=1
            tcounter+=1
            pcounter+=1
        print self.getPixels(pcounter)
        return True

    def reveal(self):
        """**Return**: The secret message from the image array. Return
        None if no message detected."""
        
        length = ''
        message = ''
        if self.decode(0)!= ord('y') and self.decode(1)!= ord('e')and self.decode(2) != ord('s'):
            return None
        pcounter = 3
        while chr(self.decode(pcounter))!='x':
            length+=chr(self.decode(pcounter))
            pcounter+=1
        length = int(length)
        pcounter += 1
        messagestart = pcounter
        while pcounter < length+messagestart:
            message += chr(self.decode(pcounter))
            pcounter+=1
        return message

    def _pad3(self, n):
        """Returns a string value of n padded with 0s to be three characters.

            :param n: number to convert to string
            **Precondition**: a int, 0 <= n <= 999

        This method does not assert its preconditions."""
        if n < 10:
            return '00'+str(n)
        elif n < 100:
            return '0'+str(n)
        return str(n)

    def _pixel2str(self, pixel):
        """Helper function for getPixels to turn a pixel into a string.

            :param pixel: The pixel value
            **Precondition**: a 3-element tuple (r,g,b) where each
            value is 0..255

        Pads all colors with 0s with to make them three digits.  This makes
        them easier to 'line up'.

        This method does not assert its precondition."""
        return self._pad3(pixel[0])+':'+self._pad3(pixel[1])+':'+self._pad3(pixel[2])

    def getPixels(self, n):
        """**Return**: String that contains the first n pixels of the current image

            :param n: number of pixels to get
            **Precondition**: a positive int < self.current.len

        The pixels are shown 5 to a line, with annotation (i.e. something at
        the beginning to say what the string contains).

        To begin a new line, put an '\n' in the string. For example, type this
        at the Python interpreter and see what happens: 'ABCDE\nEFGH'.
        Use the function _pixel2str() to get the string representation of
        a pixel tuple."""
        
        count = 1
        pixelrgb = ''
        annotation = 'Pixels of current image:\n'
        while count <= n:
            flatpixel = self.current.getFlatPixel(count-1)
            pixelrgb += self._pixel2str(flatpixel) +'\t'
            if count%5 == 0:
                pixelrgb+='\n'
            count+=1
        return annotation +pixelrgb

    # Note: You do not have to write this procedure, and if you do write it, it
    # will not be graded. But it is instructive if you have the time!
    def fuzzify(self):
        """Change the current image so that every pixel that is not on one of
        the four edges of the image is replaced with the average of its
        current value and the current values of its eight neighboring pixels.

        When implementing this function:

            FIRST, make a copy of the image.  Use the function ImageArray.Copy()

            THEN transform the copy using the values in the current image.

            THEN copy the entire transformed copy into the current image.

        Thus, the average will be the average of values in the "original"
        current image, NOT of values that have already been fuzzified."""
        # IMPLEMENT ME
        pass
