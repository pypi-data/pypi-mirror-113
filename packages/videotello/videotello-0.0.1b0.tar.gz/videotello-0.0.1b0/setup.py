import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='videotello',
    version='0.0.1-beta',
    author='Matteo Kimura',
    author_email='mateus.sakata@gmail.com',
    description='An easy framework to support DJI Tello Video Recording in Python 3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Piphi5/videotello',
    packages=setuptools.find_packages(),
    install_requires=[
        'djitellopy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)