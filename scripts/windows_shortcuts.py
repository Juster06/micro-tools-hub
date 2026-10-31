"""Small Windows Shell adapter using ctypes only; no registry or taskbar edits."""
from contextlib import contextmanager
import ctypes as ct
from pathlib import Path
import sys
import uuid

APP_ID = "EverydayDigitalBox.ProjectStatus"
APP_TITLE = "Everyday Digital Box — Project Status"
LINK_DESCRIPTION = "Everyday Digital Box project status launcher"
APP_PROPERTIES = "9f4c2855-9f79-4b39-a8d0-e1d42de1d5f3"


class GUID(ct.Structure):
    _fields_ = [("a", ct.c_uint32), ("b", ct.c_uint16), ("c", ct.c_uint16), ("d", ct.c_ubyte * 8)]


class PropertyKey(ct.Structure):
    _fields_ = [("format", GUID), ("id", ct.c_uint32)]


class Blob(ct.Structure):
    _fields_ = [("size", ct.c_uint32), ("data", ct.c_void_p)]


class VariantValue(ct.Union):
    _fields_ = [("text", ct.c_wchar_p), ("blob", Blob), ("integer", ct.c_int64)]


class PropVariant(ct.Structure):
    _fields_ = [("vt", ct.c_uint16), ("reserved", ct.c_uint16 * 3), ("value", VariantValue)]


def guid(value):
    return GUID.from_buffer_copy(uuid.UUID(value).bytes_le)


def check(hr):
    if hr < 0:
        raise OSError(f"Windows Shell operation failed (HRESULT 0x{hr & 0xffffffff:08X}).")


def method(pointer, index, *types, result=ct.c_long):
    address = ct.cast(pointer, ct.POINTER(ct.POINTER(ct.c_void_p))).contents[index]
    return ct.WINFUNCTYPE(result, ct.c_void_p, *types)(address)


def release(pointer):
    if pointer:
        method(pointer, 2, result=ct.c_ulong)(pointer)


def query(pointer, interface):
    result = ct.c_void_p()
    iid = guid(interface)
    check(method(pointer, 0, ct.POINTER(GUID), ct.POINTER(ct.c_void_p))(pointer, ct.byref(iid), ct.byref(result)))
    return result


@contextmanager
def shell_link():
    if sys.platform != "win32":
        raise OSError("Windows shortcuts require Windows.")
    ole = ct.WinDLL("ole32")
    ole.CoUninitialize.restype = None
    ole.CoInitializeEx.argtypes = [ct.c_void_p, ct.c_ulong]
    check(ole.CoInitializeEx(None, 2))
    link = ct.c_void_p()
    try:
        clsid, iid = guid("00021401-0000-0000-c000-000000000046"), guid("000214f9-0000-0000-c000-000000000046")
        ole.CoCreateInstance.argtypes = [ct.POINTER(GUID), ct.c_void_p, ct.c_ulong, ct.POINTER(GUID), ct.POINTER(ct.c_void_p)]
        check(ole.CoCreateInstance(ct.byref(clsid), None, 1, ct.byref(iid), ct.byref(link)))
        yield link
    finally:
        release(link)
        ole.CoUninitialize()


def app_id_property(link, value=None):
    store = query(link, "886d8eeb-8cf2-4446-8d02-cdba1dbdcf99")
    key = PropertyKey(guid(APP_PROPERTIES), 5)
    variant = PropVariant()
    ole = ct.WinDLL("ole32")
    ole.PropVariantClear.argtypes = [ct.POINTER(PropVariant)]
    try:
        if value is None:
            check(method(store, 5, ct.POINTER(PropertyKey), ct.POINTER(PropVariant))(store, ct.byref(key), ct.byref(variant)))
            return variant.value.text if variant.vt == 31 else None
        # InitPropVariantFromString is an inline SDK helper, not a DLL export.
        # A VT_LPWSTR uses CoTaskMemAlloc so PropVariantClear owns its cleanup.
        buffer = ct.create_unicode_buffer(value)
        ole.CoTaskMemAlloc.argtypes = [ct.c_size_t]
        ole.CoTaskMemAlloc.restype = ct.c_void_p
        memory = ole.CoTaskMemAlloc(ct.sizeof(buffer))
        if not memory:
            raise OSError("Could not allocate shortcut property value.")
        ct.memmove(memory, buffer, ct.sizeof(buffer))
        variant.vt = 31
        variant.value.text = ct.cast(memory, ct.c_wchar_p)
        check(method(store, 6, ct.POINTER(PropertyKey), ct.POINTER(PropVariant))(store, ct.byref(key), ct.byref(variant)))
        check(method(store, 7)(store))
    finally:
        ole.PropVariantClear(ct.byref(variant))
        release(store)


def known_folder(which):
    ids = {"desktop": "b4bfcc3a-db2c-424c-b029-7fe99a87c641", "programs": "a77f5d77-2e2b-44c3-a6a2-aba601054a51"}
    if sys.platform != "win32":
        raise OSError("Windows known folders require Windows.")
    folder_id = guid(ids[which])
    result = ct.c_void_p()
    shell = ct.WinDLL("shell32")
    shell.SHGetKnownFolderPath.argtypes = [ct.POINTER(GUID), ct.c_ulong, ct.c_void_p, ct.POINTER(ct.c_void_p)]
    check(shell.SHGetKnownFolderPath(ct.byref(folder_id), 0, None, ct.byref(result)))
    try:
        return Path(ct.wstring_at(result))
    finally:
        ole = ct.WinDLL("ole32")
        ole.CoTaskMemFree.argtypes = [ct.c_void_p]
        ole.CoTaskMemFree.restype = None
        ole.CoTaskMemFree(result)


def read_shortcut(filename):
    with shell_link() as link:
        persist = query(link, "0000010b-0000-0000-c000-000000000046")
        try:
            check(method(persist, 5, ct.c_wchar_p, ct.c_ulong)(persist, str(Path(filename).resolve()), 0))
        finally:
            release(persist)
        values = {}
        for name, index in (("arguments", 10), ("working_directory", 8), ("description", 6)):
            buffer = ct.create_unicode_buffer(32768)
            check(method(link, index, ct.c_wchar_p, ct.c_int)(link, buffer, len(buffer)))
            values[name] = buffer.value
        buffer = ct.create_unicode_buffer(32768)
        check(method(link, 3, ct.c_wchar_p, ct.c_int, ct.c_void_p, ct.c_ulong)(link, buffer, len(buffer), None, 4))
        values["target"] = buffer.value
        values["app_id"] = app_id_property(link)
        return values


def write_shortcut(filename, target, arguments, project_root):
    """Create/update our own shortcut, refuse unrelated same-name links, verify it."""
    filename = Path(filename)
    if filename.exists():
        previous = read_shortcut(filename)
        if previous["description"] != LINK_DESCRIPTION or previous["app_id"] != APP_ID:
            raise FileExistsError(f"An unrelated shortcut already exists: {filename.name}. It was not changed.")
    filename.parent.mkdir(parents=True, exist_ok=True)
    temporary = filename.with_name(".edb-shortcut-" + uuid.uuid4().hex + ".lnk")
    try:
        with shell_link() as link:
            for index, text in ((20, str(target)), (11, arguments), (9, str(project_root)), (7, LINK_DESCRIPTION)):
                check(method(link, index, ct.c_wchar_p)(link, text))
            check(method(link, 17, ct.c_wchar_p, ct.c_int)(link, str(target), 0))
            check(method(link, 15, ct.c_int)(link, 1))
            app_id_property(link, APP_ID)
            persist = query(link, "0000010b-0000-0000-c000-000000000046")
            try:
                check(method(persist, 6, ct.c_wchar_p, ct.c_int)(persist, str(temporary.resolve()), 1))
            finally:
                release(persist)
        result = read_shortcut(temporary)
        if Path(result["target"]).resolve() != Path(target).resolve() or result["arguments"] != arguments or Path(result["working_directory"]).resolve() != Path(project_root).resolve() or result["app_id"] != APP_ID:
            raise OSError("Shortcut verification failed; original shortcut was preserved.")
        temporary.replace(filename)
        return read_shortcut(filename)
    finally:
        if temporary.exists():
            temporary.unlink()


def set_process_identity():
    if sys.platform == "win32":
        shell = ct.WinDLL("shell32")
        shell.SetCurrentProcessExplicitAppUserModelID.argtypes = [ct.c_wchar_p]
        check(shell.SetCurrentProcessExplicitAppUserModelID(APP_ID))
