from setuptools import setup

setup(
    name = "pydrm",
    version = "1.0.0",
    author = "Noralf Trønnes",
    author_email = "noralf@tronnes.org",
    description = ("a pure python drm library which can present the framebuffer as a PIL.Image object"),
    license = "MIT",
    keywords = "drm framebuffer dumb buffer graphics",
    packages=['pydrm'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: GPU",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics",
    ],
)


