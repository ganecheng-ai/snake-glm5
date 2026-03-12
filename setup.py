"""
贪吃蛇游戏安装配置
Snake Game Setup Configuration
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='snake-game',
    version='1.0.1',
    author='Claude Code',
    author_email='',
    description='一个精美的贪吃蛇游戏，支持中文界面',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ganecheng-ai/snake-glm5',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Games/Entertainment',
    ],
    python_requires='>=3.10',
    install_requires=[
        'pygame>=2.5.0',
    ],
    entry_points={
        'console_scripts': [
            'snake-game=snake_game:main',
        ],
    },
)