from setuptools import setup

setup(
    name='gym_clgridworld',
    version='1.0.0',
    packages=['clgridworld', 'example', 'tests'],
    url='https://github.com/LeroyChristopherDunn/CurriculumLearningGridWorld',
    license='MIT',
    author='Leroy Christopher Dunn',
    author_email='social.leroy.c.dunn@gmail.com',
    description='Curriculum Learning Environment for Reinforcement Learning Agents',
    install_requires=['gym', 'numpy', 'matplotlib']
)