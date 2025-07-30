###################################################################################################
# Importing the Required libraries
###################################################################################################
from docling.document_converter import DocumentConverter

###################################################################################################
# Instantiate the docling converter and generate
###################################################################################################
file_path = "F:/Policy_docs/Spice_Digital_HR_policy.pdf"
converter = DocumentConverter()

result = converter.convert(source=file_path)
