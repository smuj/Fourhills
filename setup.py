import setuptools

setuptools.setup(
    name="fourhills",
    version="0.0.1",
    author="Simeon Jenkins",
    author_email="55206+smuj@users.noreply.github.com",
    description="A package for managing D&D campaigns",
    license="GPL",
    packages=["fourhills"],
    install_requires=[
        "click",
        "dataclasses",
        "pyyaml",
    ],
    entry_points={
        'console_scripts': [
            'fh = fourhills.fourhills:main',
            'fourhills = fourhills.fourhills:main',
        ],
    }
)
