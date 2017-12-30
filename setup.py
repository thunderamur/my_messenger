from setuptools import setup, find_packages


setup(
    name="MyMessenger",
    version='0.1a',
    description="Study project of chat based on JSON IM protocol",
    long_description="Study project of chat based on JSON IM protocol with python3 and PyQt5",
    author="Ramil Minnigaliev",
    author_email="minnigaliev-r@yandex.ru",
    url="https://github.com/thunderamur/my_messenger",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Students',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['chat PyQt 5', 'client jim chat'],
    packages=find_packages('src'),
    package_dir={'my_messenger': 'src/my_messenger'},
    package_data={'my_messenger':
                        ['ui/img/*.png',
                         'ui/img/*.jpg',
                         'ui/img/*.gif']
    },
    install_requires=[
        "PyQt5>=5.9",
        "SQLAlchemy>=1.1.15",
    ],
    extras_require={
        'test': ["pytest==3.2.2",
                 "pytest-cov==2.5.1",
                 "pytest-sugar==0.9.0",],
    },
    entry_points={
        'gui_scripts': [
            'my_messenger = my_messenger.client_gui:main',
        ]
    },
)
