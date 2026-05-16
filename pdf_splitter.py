from pypdf import PdfReader, PdfWriter
import streamlit as st
import io
import time


# The Function that Splits Pdfs Takes in the pdf and the page to split the pdf at
def split_pdf(uploaded_file, split_page):
    Reader=PdfReader(uploaded_file)
    Writer_1=PdfWriter()
    Writer_2=PdfWriter()
    
    for i in range(len( Reader.pages)):
        if i < split_page:
            Writer_1.add_page(Reader.pages[i])
        else:
            Writer_2.add_page(Reader.pages[i])
    
    # using buffers to save the data
    Buffer1=io.BytesIO()
    Buffer2=io.BytesIO()
    Writer_1.write(Buffer1)
    Writer_2.write(Buffer2)
    return Buffer1.getvalue(), Buffer2.getvalue()

# This function Extracts a portion of the pdf and takes a start page and the stop page
def slice_pdf(Input_file, start_page,stop_page):
    Pdf_Reader=PdfReader(Input_file)
    Writer=PdfWriter()

    for page in Pdf_Reader.pages[start_page:stop_page]:
        Writer.add_page(page)
        Buffer_1=io.BytesIO()

    Writer.write(Buffer_1)

    return Buffer_1.getvalue()


def merge_pdf(File_list):
        PDF_WRITER=PdfWriter()
        BUFFER=io.BytesIO()
        for pdf in File_list:
            PDF_WRITER.append(pdf)
            PDF_WRITER.write(BUFFER)
        return BUFFER.getvalue()

# The USER INTERFACE(UI)

# Lets create a sidebar that allows the user to send feedback
st.sidebar.title("User Feedback")
Feedback=st.sidebar.text_input("Enter Feedback")
email="emoefeakpughe@gmail.com"
url_notebooklm="https://notebooklm.google.com"
st.sidebar.write(f"Or email the developer {email}")
st.sidebar.write(f"Here's Google's Notebooklm  {url_notebooklm}")
st.sidebar.success("It can:" 
"\n Analyse your PDFs," \
"\nCreate Summaries, slides, videos, audio overview and many more")

print(Feedback)
Tab1,Tab2, Tab3 = st.tabs(["Split PDFs", "Slice PDFs", "Merge PDFs"])

with Tab1:

    st.title("PDF splitter 📝")
    st.info("*This tool takes in one input page and splits the pdf into two parts (first page to selected page, Selected page onwards)*")
    uploaded_file=st.file_uploader("Upload your pdf file ", type="pdf")
    if uploaded_file:
        reader=PdfReader(uploaded_file)
        if len(reader.pages) > 1:
            reader=PdfReader(uploaded_file)
            total_pages=len(reader.pages)
            title=reader.metadata.title
            st.info(f"Your PDF has {total_pages} pages")
            split_page=st.slider("Select the page you would like to split the pdf at", 1, total_pages,1)

            Split_button=st.button("Split pdf")
            if Split_button:
                with st.spinner("Splitting PDF"):
                    part1,part2=split_pdf(uploaded_file,split_page)
                    col1,col2=st.columns(2)
                
                # Display Buttons on two seperate columns
                with col1:
                    st.download_button(
                        label="Download Part 1",
                        data=part1,
                        file_name=f"{title} (from page 1 to {split_page}).pdf" or "Document_1.pdf",
                        mime="application/pdf"
                    )
                with col2:
                    st.download_button(
                        label="Download Part 2",
                        data=part2,
                        file_name=f"{title} (from page {split_page} to {total_pages}).pdf" or "Document_2.pdf",
                        mime="application/pdf"
                    )
                st.success("Split Successful")
        else:
            st.error("The uploaded PDF must have more than one page to be split")
with Tab2:
    #  Now for the UI
    st.title("PDF Slicer 📑")
    st.info("*This Tool helps you extract a section out of the pdf e.g from page X to page Y*")
    Input_file=st.file_uploader("Upload the PDF File")
    if Input_file:
        Pdf_reader2=PdfReader(Input_file)
        Title=Pdf_reader2.metadata.title
        Total_pages=len(Pdf_reader2.pages)
        st.info(F"This PDF has {Total_pages} pages")

        if Total_pages > 1 :
            start_page,stop_page=st.slider("select a range", 1, Total_pages, (0,Total_pages))
            Extract_button=st.button("Extract Section")

            if start_page != stop_page:
                if Extract_button:
                    with st.spinner("Slicing Pdf"):
                        part= slice_pdf(Input_file,start_page,stop_page)

                    with st.container(border=True):
                        st.download_button(
                            label="Download Section",
                            data=part,
                            file_name=f"{Title} from( page {start_page} to page {stop_page}).pdf" or "Document",
                            mime="application/pdf"
                        )
                    st.success("Slice Successful")
            else:
                st.warning("Your inputs on the slider must be different")
        else:
            st.error("The uploaded pdf must have more than one page")


with Tab3:
    st.title("PDF Merger")
    st.info("*This tool helps you merge PDFs. "
    "Note: PDFs will be merged in the order they are sent*")
    File_list=st.file_uploader("Upload the PDF files", type="pdf", accept_multiple_files=True)
    L=len(File_list)

    if  len(File_list) > 1:
        st.info(f"You Uploaded {L} Files")
        with st.spinner("Merging files..."):
            Final_pdf=merge_pdf(File_list)
            
        with st.container(border=True):
                st.download_button(
                label="Download",
                data=Final_pdf,
                file_name="Document.pdf",
                mime="application/pdf"
                )
        st.success("PDFs successfully merged!")









