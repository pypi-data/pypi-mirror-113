from setuptools import setup

VERSION = '2.0.0'
DESCRIPTION = 'This module will return whether PDF is Digital, Non-Digital or Mixed.'

# Setting up
setup(
    name="pdf_segregation",
    version=VERSION,
    author="Kishan Tongrao",
    author_email="kishan.tongs@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=['pdf_segregation'],
    include_package_data=True,
    install_requires=['PyPDF2'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    long_description = """After installation use syntax : \n
    from pdf_segregation import pdf_classifier\n
    result, digital_pages, nondigital_pages = pdf_classifier.digital_nondigital_classifier("scansmpl.pdf")\n\n
    scansmpl.pdf replace with your file name.\n
    print(result)\n
    print(digital_pages)\n
    print(nondigital_pages)\n\n
    It will return Digital, Non-Digital or Mixed based on document.\n\n
    This is the first pip library I am publishing. In future the exception handling and \n
    and detailed classification is going to included in code.\n

    \n
    Thanks and Enjoy !!!\n\n

    """

)