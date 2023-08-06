from setuptools import Extension
from setuptools import setup


transparentwin_mod = Extension(
    name="transparentwindow._transparentwindow",
    sources=["src/transparentwindow.c", "src/resource.rc"],
    extra_compile_args=[
        "/utf-8",
        "/DUNICODE",
        "/D_UNICODE",
        "/DWINVER=0x0A00",
        "/D_WIN32_WINNT=0x0A00",
    ],
    extra_link_args=[
        "User32.lib",
        "Shell32.lib",
        "Gdi32.lib",
        "Comctl32.lib",
        "/RELEASE",
    ],
)

screenshot_mod = Extension(
    name="transparentwindow._screenshot",
    sources=["src/screenshot.c"],
    extra_compile_args=[
        "/utf-8",
        "/DUNICODE",
        "/D_UNICODE",
        "/DWINVER=0x0A00",
        "/D_WIN32_WINNT=0x0A00",
    ],
    extra_link_args=["User32.lib", "Gdi32.lib", "/RELEASE"],
)


setup(
    packages=["transparentwindow"],
    ext_modules=[transparentwin_mod, screenshot_mod],
)
