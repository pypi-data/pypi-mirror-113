from setuptools import setup, find_packages

setup(
    name='chessam',
    version=0.1,
    description="basic chess gui connected to stockfish.",
    author="Samuel Rodriguez",
    author_email="samrolopez@email.com",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=['chess'],
    zip_safe=False
)