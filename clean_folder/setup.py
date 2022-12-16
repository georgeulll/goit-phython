from setuptools import setup

setup(
    name="clean-folder",
    version ="1",
    description="You can sort your files in the folder, which you don't want to check",
    url="github.com",
    author="Heorhii Ulinets",
    author_email="ulinets.g@gmail.com",
    license="GoIT",
    packages=["Clean_folder"],
    entry_points={'console_scripts': ['clean-folder = Clean_folder.clean:main']}
)