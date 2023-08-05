from setuptools import setup

setup(
    name='maso',
    version='1.3',
    description='方便使用OPENCV包的套件',
    url='https://github.com/maso0310/maso/tree/master',
    author='Maso',
    author_email='balimon@hotmail.com',
    install_requires=["opencv-python", "numpy","joblib","pandas","scikit-learn==0.24.1"],
    license='MIT License',
    packages=['maso'],
    zip_safe=False,
    keywords=['maso'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)