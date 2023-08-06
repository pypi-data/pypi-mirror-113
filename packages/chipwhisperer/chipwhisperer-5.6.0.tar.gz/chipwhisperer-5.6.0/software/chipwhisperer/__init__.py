# -*- coding: utf-8 -*-
"""
.. module:: chipwhisperer
   :platform: Unix, Windows
   :synopsis: Test

.. moduleauthor:: NewAE Technology Inc.

Main module for ChipWhisperer.
"""

__version__ = '5.6.0'
import os, os.path, time
from zipfile import ZipFile

from .capture import scopes, targets
from .capture.api import programmers
from .capture import acq_patterns as key_text_patterns
from .common.utils.util import fw_ver_compare
from .common.api import ProjectFormat as project
from .common.traces import Trace
from .common.utils import util
from .capture.scopes.cwhardware.ChipWhispererSAM3Update import SAMFWLoader, get_at91_ports
import logging
from .logging import *

# replace bytearray with inherited class with better repr and str.
import builtins
builtins.bytearray = util.bytearray

# from chipwhisperer.capture.scopes.cwhardware import ChipWhispererSAM3Update as CWFirmwareUpdate

ktp = key_text_patterns #alias

def program_sam_firmware(serial_port=None, hardware_type=None, fw_path=None):
    """Program firmware onto an erased chipwhisperer scope or target

    See https://chipwhisperer.readthedocs.io/en/latest/firmware.html for more information
    """
    if (hardware_type, fw_path) == (None, None):
        raise ValueError("Must specify hardware_type or fw_path, see https://chipwhisperer.readthedocs.io/en/latest/firmware.html")

    if serial_port is None:
        at91_ports = get_at91_ports()
        if len(at91_ports) == 0:
            raise OSError("Could not find bootloader serial port, please see https://chipwhisperer.readthedocs.io/en/latest/firmware.html")
        if len(at91_ports) > 1:
            raise OSError("Found multiple bootloaders, please specify com port. See https://chipwhisperer.readthedocs.io/en/latest/firmware.html")

        serial_port = at91_ports[0]
        print("Found {}".format(serial_port))
    prog = SAMFWLoader(None)
    prog.program(serial_port, hardware_type=hardware_type, fw_path=fw_path)

def program_target(scope, prog_type, fw_path, **kwargs):
    """Program the target using the programmer <type>

    Programmers can be found in the programmers submodule

    Args:
       scope (ScopeTemplate): Connected scope object to use for programming
       prog_type (Programmer): Programmer to use. See chipwhisperer.programmers
           for available programmers
       fw_path (str): Path to hex file to program

    .. versionadded:: 5.0.1
        Simplified programming target
    """
    if prog_type is None: #[makes] automating notebooks much easier
        return
    prog = prog_type(**kwargs)

    try:
        prog.scope = scope
        prog._logging = None
        prog.open()
        prog.find()
        prog.erase()
        prog.program(fw_path, memtype="flash", verify=True)
        prog.close()
    except:
        if isinstance(prog, programmers.XMEGAProgrammer) and isinstance(scope, scopes.OpenADC):
            target_logger.info("XMEGA error detected, resetting XMEGA")
            scope.io.pdic = 0
            time.sleep(0.05)
            scope.io.pdic = None
            time.sleep(0.05)
        raise



def open_project(filename):
    """Load an existing project from disk.

    Args:
       filename (str): Path to project file.

    Returns:
       A chipwhisperer project object.

    Raises:
       OSError: filename does not exist.
    """
    filename = project.ensure_cwp_extension(filename)

    proj = project.Project()
    proj.load(filename)
    return proj


def create_project(filename, overwrite=False):
    """Create a new project with the path <filename>.

    If <overwrite> is False, raise an OSError if this path already exists.

    Args:
       filename (str): File path to create project file at. Must end with .cwp
       overwrite (bool, optional): Whether or not to overwrite an existing
           project with <filename>. Raises an OSError if path already exists
           and this is false. Defaults to false.

    Returns:
       A chipwhisperer project object.

    Raises:
       OSError: filename exists and overwrite is False.
    """
    filename = project.ensure_cwp_extension(filename)

    if os.path.isfile(filename) and (overwrite == False):
        raise OSError("File " + filename + " already exists")

    # If the user gives a relative path including ~, expand to the absolute path
    filename = os.path.abspath(os.path.expanduser(filename))

    proj = project.Project()
    proj.setFilename(filename)

    return proj


def import_project(filename, file_type='zip', overwrite=False):
    """Import and open a project.

    Will import the **filename** by extracting to the current working
    directory.

    Currently support file types:
     * zip

    Args:
        filename (str): The file name to import.
        file_type (str): The type of file that is being imported.
            Default is zip.
        overwrite (bool): Whether or not to overwrite the project given as
            the **import_as** project.

    .. versionadded:: 5.1
        Add **import_project** function.
    """
    # extract name from input file
    input_dir, input_file = os.path.split(filename)
    input_file_root, input_file_ext = os.path.splitext(input_file)
    input_abs_path = os.path.abspath(filename)

    # use the appropriate type of import
    if file_type == 'zip':
        with ZipFile(input_abs_path, 'r') as project_zip:
            output_path = None
            for path in project_zip.namelist():
                root, ext = os.path.splitext(path)
                if ext == '.cwp':
                    directory, project_name = os.path.split(root)
                    output_path = ''.join([project_name, '.cwp'])

                    # check if name already exists in projects
                    if os.path.isfile(output_path) and (overwrite == False):
                        raise OSError("File " + output_path + " already exists")

                    # extract the project.cwp file and project_data directory to
                    # the PROJECT_DIR
                    project_zip.extractall(path=os.getcwd())

            if output_path is None:
                raise ValueError('Zipfile does not contain a .cwp file, so it cannot be imported')
    else:
        raise ValueError('Import from file type not supported: {}'.format(file_type))

    proj = project.Project()
    proj.load(output_path)

    return proj


def scope(scope_type=None, name=None, **kwargs):
    """Create a scope object and connect to it.

    This function allows any type of scope to be created. By default, the
    object created is based on the attached hardware (OpenADC for
    CWLite/CW1200, CWNano for CWNano).

    Scope Types:
     * :class:`scopes.OpenADC` (Pro and Lite)
     * :class:`scopes.CWNano` (Nano)

    If multiple chipwhisperers are connected, the serial number of the one you
    want to connect to can be specified by passing sn=<SERIAL_NUMBER>

    Args:
       scope_type (ScopeTemplate, optional): Scope type to connect to. Types
           can be found in chipwhisperer.scopes. If None, will try to detect
           the type of ChipWhisperer connected. Defaults to None.
       name (str, optional): model name of the ChipWhisperer that you want to
           connect to. Alternative to specifying the serial number when
           multiple ChipWhisperers, all of different type, are connected.
           Defaults to None. Valid values:
           * Lite
           * Pro
           * Husky
       idProduct (int, optional): idProduct of the ChipWhisperer that you want to
           connect to. Alternative to specifying the serial number when
           multiple ChipWhisperers, all of different type, are connected.
           Defaults to None. Valid values:
           * 0xace2: CW-Lite
           * 0xace3: CW-Pro
           * 0xace5: CW-Husky
       sn (str, optional): Serial number of ChipWhisperer that you want to
           connect to. sn is required if more than one ChipWhisperer of the
           same type is connected (i.e. two CWNano's or a CWLite and CWPro).
           Defaults to None.

    Returns:
        Connected scope object.

    Raises:
        OSError: Can be raised for issues connecting to the chipwhisperer, such
            as not having permission to access the USB device or no ChipWhisperer
            being connected.
        Warning: Raised if multiple chipwhisperers are connected, but the type
            and/or the serial numbers are not specified

    .. versionchanged:: 5.1
        Added autodetection of scope_type
    """
    from chipwhisperer.common.utils.util import get_cw_type
    if name is not None:
        if name == 'Husky':
            kwargs['idProduct'] = 0xace5
        elif name == 'Lite':
            kwargs['idProduct'] = 0xace2
        elif name == 'Pro':
            kwargs['idProduct'] = 0xace3
        else:
            raise ValueError

    if scope_type is None:
        scope_type = get_cw_type(**kwargs)
    scope = scope_type()
    try:
        scope.con(**kwargs)
    except IOError:
        scope_logger.error("ChipWhisperer error state detected. Resetting and retrying connection...")
        scope._getNAEUSB().reset()
        time.sleep(2)
        scope = scope_type()
        scope.con(sn)
    return scope


def target(scope, target_type=targets.SimpleSerial, **kwargs):
    """Create a target object and connect to it.

    Args:
       scope (ScopeTemplate): Scope object that we're connecting to the target
           through.
       target_type (TargetTemplate, optional): Target type to connect to.
           Defaults to targets.SimpleSerial. Types can be found in
           chipwhisperer.targets.
       **kwargs: Additional keyword arguments to pass to target setup. Rarely
           needed.

    Returns:
        Connected target object specified by target_type.
    """
    target = target_type()
    target.con(scope, **kwargs)

    # need to check 
    if scope and (isinstance(target, targets.SimpleSerial) or isinstance(target, targets.SimpleSerial2)):
        if isinstance(scope, scopes.CWNano) and not fw_ver_compare(scope.fw_version, {"major": 0, "minor": 24}):
            target.ser.cwlite_usart._max_read = 128
            target_logger.warning("Old firmware: limiting max serial read")
    return target

def capture_trace(scope, target, plaintext, key=None, ack=True):
    """Capture a trace, sending plaintext and key

    Does all individual steps needed to capture a trace (arming the scope
    sending the key/plaintext, getting the trace data back, etc.). Uses
    target.output_len as the length of the expected target reponse for
    simpleserial.

    Args:
        scope (ScopeTemplate): Scope object to use for capture.
        target (TargetTemplate): Target object to read/write text from.
        plaintext (bytearray): Plaintext to send to the target. Should be
            unencoded bytearray (will be converted to SimpleSerial when it's
            sent). If None, don't send plaintext.
        key (bytearray, optional): Key to send to target. Should be unencoded
            bytearray. If None, don't send key. Defaults to None.
        ack (bool, optional): Check for ack when reading response from target.
            Defaults to True.

    Returns:
        :class:`Trace <chipwhisperer.common.traces.Trace>` or None if capture
        timed out.

    Raises:
        Warning or OSError: Error during capture.

    Example:
        Capturing a trace::

            import chipwhisperer as cw
            scope = cw.scope()
            scope.default_setup()
            target = cw.target()
            ktp = cw.ktp.Basic()
            key, pt = ktp.new_pair()
            trace = cw.capture_trace(scope, target, pt, key)

    .. versionadded:: 5.1
        Added to simplify trace capture.

    .. versionchanged:: 5.2
        Added ack parameter and use of target.output_len
    """

    import signal, logging

    # useful to delay keyboard interrupt here,
    # since could interrupt a USB operation
    # and kill CW until unplugged+replugged
    class DelayedKeyboardInterrupt:
        def __enter__(self):
            self.signal_received = False
            self.old_handler = signal.signal(signal.SIGINT, self.handler)

        def handler(self, sig, frame):
            self.signal_received = (sig, frame)
            scope_logger.debug('SIGINT received. Delaying KeyboardInterrupt.')

        def __exit__(self, type, value, traceback):
            signal.signal(signal.SIGINT, self.old_handler)
            if self.signal_received:
                self.old_handler(*self.signal_received)
    # with DelayedKeyboardInterrupt():
    if key:
        target.set_key(key, ack=ack)

    scope.arm()

    if plaintext:
        target.simpleserial_write('p', plaintext)

    ret = scope.capture()

    i = 0
    while not target.is_done():
        i += 1
        time.sleep(0.05)
        if i > 100:
            scope_logger.warning("Target did not finish operation")
            return None

    if ret:
        scope_logger.warning("Timeout happened during capture")
        return None

    response = target.simpleserial_read('r', target.output_len, ack=ack)
    wave = scope.get_last_trace()

    if len(wave) >= 1:
        return Trace(wave, plaintext, response, key)
    else:
        return None

def plot(*args, **kwargs):
    """Get a plotting object for use in Jupyter.
    
    Uses a Holoviews/Bokeh plot with a width of 800 and
    a height of 600. You must have Holoviews and Bokeh
    installed, as well as be working in a Jupyter
    environment.

    args and kwargs are the same as a typical Holoviews plot.

    Plotting a trace in a Jupyter environment::

        import chipwhisperer as cw
        scope = cw.scope()
        ...
        trace = cw.capture_trace(scope, target, text, key)
        display(cw.plot(trace.wave))

    Returns:
        A holoviews Curve object
    """
    import holoviews as hv
    hv.extension('bokeh', logo=False) #don't display logo, otherwise it pops up everytime this func is called.
    return hv.Curve(*args, **kwargs).opts(width=800, height=600)
