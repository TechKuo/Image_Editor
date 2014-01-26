# imager.py
# Dexter Kozen (dck10) and Walker White (wmw2)
# October 26, 2012
"""This module provides the primary Controller for our application.

The application corresponds to the class ImagerApp.  All of the
other classes are individual controllers for each of the View components
defined in imager.kv.  The View (imager.kv) and this Controller
module (imager.py) have the same name because they are so tightly
interconnected."""
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.config import Config
from kivy.clock import Clock

import os.path

from image_array import ImageArray
from image_processor import ImageProcessor
from image_panel import ImagePanel


class LoadDialog(BoxLayout):
    """Instance is a controller for a LoadDialog, a pop-up dialog to load a file.

    The View for this controller is defined in imager.kv."""
    # These fields are 'hooks' to connect to the imager.kv file
    # They work sort of like @properties, but are different
    filechooser = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(BoxLayout):
    """Instance is a controller for a SaveDialog, a pop-up dialog to save a file.

    The View for this controller is defined in imager.kv."""
    # These fields are 'hooks' to connect to the imager.kv file
    # They work sort of like @properties, but are different
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ErrorDialog(BoxLayout):
    """Instance is a controller for an ErrorDialog, a pop-up dialog to notify
    the user of an error.

    The View for this controller is defined in imager.kv."""
    # These fields are 'hooks' to connect to the imager.kv file
    # They work sort of like @properties, but are different
    label = StringProperty('')
    ok = ObjectProperty(None)


class WarningDialog(BoxLayout):
    """Instance is a controller for a WarningDialog, a pop-up dialog to
    warn the user.

    It differs from ErrorDialog in that it may be nested inside of another
    pop-up dialog.

    The View for this controller is defined in imager.kv."""
    # These fields are 'hooks' to connect to the imager.kv file
    # They work sort of like @properties, but are different
    label = StringProperty('')
    data = StringProperty('')
    ok = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Main(BoxLayout):
    """Instance is a controller for the primary application.

    This controller manages all of the buttons and text fields of
    the application. It instantiates ImageProcessor (the student
    defined class), and uses that sub-controller to process images.

    The View for this controller is defined in imager.kv."""
    # These fields are 'hooks' to connect to the imager.kv file
    # They work sort of like @properties, but are different
    source = StringProperty('samples/goldhill.jpg')
    original_image = ObjectProperty(None)
    current_image = ObjectProperty(None)
    grayscale = ObjectProperty(None)
    hidden_text = ObjectProperty(None)
    text_input = ObjectProperty(None)
    image_processor = ObjectProperty(None)
    notifier = ObjectProperty(None)

    # Hidden fields not needed by imager.kv
    _operand = None # current executing option
    _op_args = None # arguments for the executing option

    def config(self):
        """Configures the application at start-up.

        Controllers are responsible for initializing the application
        and creating all of the other objects. This method does just
        that. It loads the currently selected image file, creates an
        ImageArray for that file, creates an ImageProcessor to handle
        the array, and connects the ImageProcessor to the two
        ImagePanel objects."""
        # Load the image into an array
        image_array = ImageArray.LoadFile(self.source)
        # Create the processor for the given ImageArray
        self.image_processor = ImageProcessor(image_array)
        # Set up the display panels
        self.original_image_panel = ImagePanel(self.original_image, self.image_processor.original)
        self.current_image_panel = ImagePanel(self.current_image, self.image_processor.current)

    def error(self, msg):
        """Report an error to the user

            :param msg: the error message
            **Precondition**: a string

        The error message will take up most of the Window, and last until
        the user dismisses it."""
        assert type(msg) == str, `msg`+' is not a string'
        content = ErrorDialog(label=msg, ok=self._dismiss_popup)
        self._popup = Popup(title='Error', content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def do(self, trans, *args):
        """Perform a transformation on the image.

            :param trans: transformation method in ImageProcessor
            **Precondition** : a reference to a method or function, not a string for its name

            :param args: list of arguments for `transform`
            **Precondition**: a list or tuple with valid argument values

        This method does not enforce its preconditions. Use with care."""
        if not self._operand is None:
            return

        # Say PROCESSING...
        self.notifier.color = [1,1,1,1]
        self._operand = trans
        self._op_args = args
        # Process the transform on the next clock cycle.
        Clock.schedule_once(self._do_async)

    def _do_async(self,dt):
        """Perform the active image transform.

        Hidden method that allows us to spread a transformation over
        two clock cycles.  This allows us to print a progress message
        on the screen."""
        # Perform the transformation
        if len(self._op_args) == 0:
            self._operand()
        else:
            self._operand(self._op_args[0])

        # Remove the status message and redisplay
        self.notifier.color = [0,0,0,0]
        self.current_image_panel.display(self.image_processor.current)
        self._operand = None
        self.op_args = None

    def hide(self):
        """Stores the hidden message in the image via steganography.

        Calls the method from image_processor. Displays a pop-up
        if the method fails (i.e. returns False).  Otherwise, message is
        now stored in the image."""
        text = str(self.hidden_text.text)
        result = self.image_processor.hide(text)
        if not result:
            self.error('Nothing was hidden')

    def reveal(self):
        """Reveal the hidden message in the image.

        Calls the method from image_processor. Displays a pop-up
        if there is no message.  Otherwise, places message in
        the text input box."""
        self.hidden_text.text = ''
        text = self.image_processor.reveal()
        if text is None:
            self.error('No hidden message, apparently')
        else:
            self.hidden_text.text = '<message revealed:> ' + text

    def _dismiss_popup(self):
        """Used to dismiss the currently active pop-up"""
        self._popup.dismiss()

    def load(self):
        """Open a dialog to load an image file."""
        content = LoadDialog(load=self._load_helper, cancel=self._dismiss_popup)
        self._popup = Popup(title="Load image", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def _load_helper(self, path, filename):
        """Callback function for load. Called when user selects a file.

        This method loads the image file and redisplays the ImagePanels.

        Hidden method used only internally.  No preconditions enforced."""
        self._dismiss_popup()
        if (len(filename) == 0):
            return
        self.source = str(os.path.join(path, filename[0]))
        self.config()
        self.original_image_panel.display()
        self.current_image_panel.display()

    def save(self):
        """Save the image in the current ImageArray to a file."""
        content = SaveDialog(save=self._check_png, cancel=self._dismiss_popup)
        self._popup = Popup(title="Save image", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def _check_png(self, path, filename):
        """Make sure we are saving in .png format.

        If user uses another extension, or no extension at all, force
        the file to be a .png

        Hidden method used only internally.  No preconditions enforced."""
        self._dismiss_popup()
        if filename.lower().endswith('.png'):
            self._save_png(filename)
        else:
            i = filename.rfind('.')
            if i != -1: filename = filename[:i] # strip old extension
            filename += '.png'
            msg = 'File will be saved as\n{}\nin .png format. Proceed?'
            self._file_warning(msg.format(filename), filename, self._save_png)

    def _save_png(self, filename):
        """Check whether file exists before saving.

        Saves the file if does not exist or user confirms.

        Hidden method used only internally.  No preconditions except png suffix enforced."""
        assert filename.lower().endswith('.png')
        self._dismiss_popup()
        if os.path.isfile(filename):
            msg = 'File\n{}\nexists. Overwrite?'
            self._file_warning(msg.format(filename), filename, self._force_save)
        else:
            self._force_save(filename)

    def _force_save(self, filename):
        """Forceably saves the specified file, without user confirmation.

        Hidden method used only internally.  No preconditions enforced."""
        self._dismiss_popup()
        # prepare image for saving
        im = self.image_processor.current.image
        # Direct file descriptor save broken on Windows
        # with open(filename, 'w') as f:
        try:
            im.save(filename, 'PNG')
        except:
            self.error('Cannot save image file: ' + filename)
        #f.close

    def _file_warning(self, msg, filename, ok):
        """Alerts the user of an issue when trying to load or save a file

        Hidden method used only internally.  No preconditions enforced."""
        content = WarningDialog(label=msg, data=filename, ok=ok, cancel=self._dismiss_popup)
        self._popup = Popup(title='Warning', content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def loadText(self):
        """Open a dialog to load a text file.

        Hidden method to try loading large messages into the text
        field.  Used for grading purposed on hide/reveal, as the
        clipboard does not work on all OSs"""
        content = LoadDialog(load=self._load_text_helper, cancel=self._dismiss_popup)
        content.filechooser.filters = ['*.txt','*.py']
        self._popup = Popup(title="Load image", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def _load_text_helper(self, path, filename):
        """Callback function for _load_text. Called when user selects a file.

        This method loads the text file and puts it in the text input box.

        Hidden method used only internally.  No preconditions enforced."""
        self._dismiss_popup()
        if (len(filename) == 0):
            return
        filename = str(os.path.join(path, filename[0]))
        instream = open(filename)
        self.hidden_text.text = instream.read()


class ImagerApp(App):
    """Instance is an Imager application.

    This class is the primary controller.  It creates all of the views
    and other objects. However, after start-up, it delegates all
    activity to the `Main` class."""
    def build(self):
        """Read kivy file and perform layout"""
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '672')
        Config.set('graphics', 'resizable', '0') # make not resizable
        return Main()

    def on_start(self):
        """Start up the app and initialize values"""
        super(ImagerApp, self).on_start()
        self.root.config()

# Application Code
if __name__ == '__main__':
    ImagerApp().run()
