"""No-console entry point shared by Desktop and Start menu shortcuts."""
try:
    from status_launcher import main
    main()
except Exception as exc:
    import ctypes
    ctypes.windll.user32.MessageBoxW(
        None,
        f"The Project Control Dashboard could not start.\n\n{exc}\n\n"
        "Use desktop Python 3.10+ with Tcl/Tk. Restore the complete scripts folder "
        "or recreate the shortcut after moving the checkout.",
        "Everyday Digital Box — Startup error", 0x10,
    )
