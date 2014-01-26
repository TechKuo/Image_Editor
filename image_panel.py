# image_panel.py
# Dexter Kozen (dck10) and Walker White (wmw2)
# October 26, 2012
"""This module provides an additional View for our application.

This is the primary View for coordinating with ImageProcessor.
Therefore, we separated it as a new class for you to see,
rather than putting it in a .kv file."""
from kivy.graphics import Rectangle


class ImagePanel(object):
    """Instance maintains a kivy Image widget on which to display an image"""

    # Fields (hidden)
    _widget = None # Widget where image will be displayed
    _image = None  # Reference to image array for display

    # Immutable properties
    @property
    def widget(self):
        """Kivy Widget where image will be displayed.

        *This attribute is set by the constructor and may not be modified*"""
        return self._widget

    @property
    def image(self):
        """Reference to ImageArray to display

        *This attribute is set by the constructor and may not be modified*"""
        return self._image

    def __init__(self, widget, image):
        """**Constructor**: Create an ImagePanel in the given widget.

            :param widget: The widget to display the image in
            **Precondition**: a Kivy Widget

            :param image: image to display.
            **Precondition**: an ImageArray object

        Changes to the image will only be shown in the ImagePanel when
        you invoke the display method."""
        self._widget = widget
        self._image  = image

    def display(self,image=None):
        """Display an image array.

            :param image: An image to display.
            **Precondition**: an ImageArray object or None

        If no image_array is specified, it will use the one stored in
        its `image` attribute."""
        if not image is None:
            self._image = image
        texture = self._image.texture

        # calculate placement of rectangle to draw the texture
        s = self._widget.size[0] # bounding box size
        assert self._widget.size[1] == s # sanity check - should be square
        a = self._image.cols
        b = self._image.rows
        if a > b:
            ra = s
            rb = s*b/a
        elif a < b:
            rb = s
            ra = s*a/b
        else: # a == b
            ra = rb = s
        pos = (int((s-ra)/2 + self._widget.pos[0]), int((s-rb)/2 + self._widget.pos[1]))
        size = (int(ra), int(rb))

        # display it
        self._widget.canvas.clear()
        with self._widget.canvas:
            Rectangle(texture=texture, pos=pos, size=size)
