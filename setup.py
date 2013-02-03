import sys
from setuptools import setup

install_requires = [
        "Flask",
        "python-mpd2"
]

setup(
        name="Flask-MPDKit",
        version="0.1",
        url="http://github.com/feltnerm/flask-mpdkit",
        license="BSD",
        author="Mark Feltner",
        author_email="feltner.mj@gmail.com",
        description="A Flask extension that simplifies the use of MPD",
        py_modules=["flask-mpdkit"],
        zip_safe=False,
        platforms="any",
        install_requires=install_requires,
)
