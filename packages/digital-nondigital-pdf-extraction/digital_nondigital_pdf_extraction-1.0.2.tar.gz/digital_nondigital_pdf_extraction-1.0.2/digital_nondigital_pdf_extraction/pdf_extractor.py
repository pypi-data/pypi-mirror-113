## Load libraries
#
import pathlib
import PyPDF2
import pdfplumber
import shutil
import easyocr
import fitz
import glob
import os
import warnings
warnings.simplefilter("ignore")

## Create output director for nondigital 
#
path = "NonDigital_Output"

def create_temp_output_folder(path):
    if(os.path.exists(path)):
        for file in glob.glob(path+"/*"):
            os.remove(file)
    else:
        os.mkdir(path)


## Non digital pdf extraction
#
def non_digital_pdf_information_extractor(files, p):
    try:
        doc = fitz.open(files)
        data = ""
        
        page = doc.loadPage(p) 
        pix = page.getPixmap()
        output = path + "/outfile.png"
        pix.writePNG(output)

        reader = easyocr.Reader(['en'])
        data_local = reader.readtext(path + "/outfile.png")

        data = " ".join(text for bbox, text, prob in data_local)
    
        return data
    
    
    except FileNotFoundError:
        return "Please provide correct pdf file path."
    except Exception as e:
        return "Error : {}".format(e)
    
## Digital pdf extraction
#
def digital_pdf_extraction(files, p):
    try:
        data = ''
        page_data = ""
        with pdfplumber.open(str(files)) as pdf:   
            page_data = pdf.pages[p]
            
            data = page_data.extract_text()        

        return data

    except FileNotFoundError:
        return "Please provide correct pdf file path."
    except Exception as e:
        return "Error : {}".format(e)


def digital_nondigital_extractor(files, digital_pages, nondigital_pages):
    try:
        # Create temporacy folder
        create_temp_output_folder(path)

        extention = pathlib.Path(files).suffix
        if(extention == ".pdf"):
            final_text = " "
            text = ""
            with pdfplumber.open(files) as pdf:
                n_pages = len(pdf.pages)
            
            for p in range(n_pages):
                # if(p < n_pages):
                if(p in digital_pages):
                    text = digital_pdf_extraction(files, p)
                elif(p in nondigital_pages):
                    text = non_digital_pdf_information_extractor(files, p)
                else:
                    return "Error : Page number {} is not belong in Digital/NonDigital PDF page number list.".format(p)
                
                final_text = final_text + str(text)
                
            return final_text

        else:
            shutil.rmtree(path)
            print("Please check extension of provided file. It is not pdf file.")
            return "None"

    except FileNotFoundError:
        return "Please provide correct pdf file path."
    except Exception as e:
        return "Error : {}".format(e)


## Digital and Non digital classifier
#     
def digital_nondigital_classifier(files):
    try:
        extention = pathlib.Path(files).suffix
        if(extention == ".pdf"):
            digital_page_numbers = []
            non_digital_page_numbers = []

            pdf_reader = PyPDF2.PdfFileReader(str(files), 'rb')
            total_pages = pdf_reader.getNumPages()
            curr_page = 0
            d_flag_count = 0
            non_d_flag_count = 0
            for curr_page in range(0, total_pages):
                page_data = pdf_reader.getPage(curr_page)
                
                if '/Font' in page_data['/Resources']:     
                    d_flag_count = d_flag_count + 1
                    digital_page_numbers.append(curr_page)
                else:
                    non_d_flag_count = non_d_flag_count + 1
                    non_digital_page_numbers.append(curr_page)

            if(d_flag_count > 0 and non_d_flag_count == 0):
                return "Digital", digital_page_numbers, non_digital_page_numbers
            elif(non_d_flag_count > 0 and d_flag_count == 0):
                return "Non-Digital", digital_page_numbers, non_digital_page_numbers
            else:
                return "Mixed", digital_page_numbers, non_digital_page_numbers
        
        else:
            print("Please check extension of provided file. It is not pdf file.")
            return "None", [],  []
        
    except FileNotFoundError as e:
        print("Error : {}".format(e.strerror))
        return "None", [], []
    except FileExistsError as e:
        print("Error : {}".format(e.strerror))
        return "None", [], []
    
# classification, digi_pages, non_digi_pages = digital_nondigital_classifier("sample-merged.pdf")
# # print(classification)
# # print(digi_pages)
# # print(non_digi_pages)

# data = digital_nondigital_extractor("sample-merged.pdf", digi_pages, non_digi_pages)
# print(data)