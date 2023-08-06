from setuptools import setup

VERSION = '1.0.2'
DESCRIPTION = 'This module will return whether PDF is Digital, Non-Digital or Mixed.'

# Setting up
setup(
    name="digital_nondigital_pdf_extraction",
    version=VERSION,
    author="Kishan Tongrao",
    author_email="kishan.tongs@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=['digital_nondigital_pdf_extraction'],
    include_package_data=True,
    install_requires=['PyPDF2', 'pdfplumber','fitz', 'easyocr', 'warnings'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    long_description = """
    ```Python 
    # After installation use syntax :

    ## Load library
    #
    from digital_nondigital_pdf_extraction import pdf_extractor
    
    result, digital_pages, nondigital_pages = pdf_extractor.digital_nondigital_classifier("scansmpl.pdf")
    # scansmpl.pdf replace with your file name.

    print(result)
    print(digital_pages)
    print(nondigital_pages)
    # It will return result either Digital, Non-Digital or Mixed based on document.
    # digital_pages - digital page numbers present in pdf.
    # nondigital_pages - nondigital page numbers present in pdf.

    data = pdf_extractor.digital_nondigital_extractor("scansmpl.pdf", digital_pages, nondigital_pages)
    print(data)
    # Your result
    
    ```

    Thanks and Enjoy !!!

    """

)