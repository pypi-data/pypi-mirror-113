import setuptools
from distutils.core import setup

setup(
 name = "voiceit2",
 version = "2.6.1",
 description = "VoiceIt API 2.0 Python Wrapper",
 author = "Hassan Ismaeel",
 author_email = "hassan@voiceit.io",
 packages=setuptools.find_packages(),
 install_requires=[
     "requests",
 ],
 url = "https://github.com/voiceittech/VoiceIt2-Python",
 download_url = "https://github.com/voiceittech/VoiceIt2-Python/archive/2.6.1.tar.gz",
 keywords = ["biometrics", "voice verification", "voice biometrics"],
 classifiers = [
 "Programming Language :: Python :: 3",
 "License :: OSI Approved :: MIT License",
 "Operating System :: OS Independent"],
)