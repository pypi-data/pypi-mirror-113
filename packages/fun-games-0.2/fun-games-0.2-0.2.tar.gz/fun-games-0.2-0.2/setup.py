from setuptools import setup,find_packages
setup(
    name='fun-games-0.2',
    version='0.2',
    packages=find_packages(),
    entry_points={"console_scripts": ["games=src.play_games:main"]}
)
