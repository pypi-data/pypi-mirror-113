from setuptools import setup


setup(
    long_description=open("README.md", "r").read(),
    name="onboot",
    version="0.2",
    description="cross-platform onboot installers",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/onboot",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License'
    ],
    keywords="cross-platform onboot installer",
    long_description_content_type="text/markdown"
)
