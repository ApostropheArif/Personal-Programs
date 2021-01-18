#! python3

"""
Author: ApostropheArif
Created on Thu Jan 14 15:37:14 2021

This script can be used to:
    i) combine several PDF documents, or 
    ii) extract specific pages from a PDF document 

"""

import os
import PyPDF2

def file_not_found():
    print('\nThe PDF document cannot be found. Please check its absolute path and try again.')

print('Combine Your PDFs!'.center(40))

merger = PyPDF2.PdfFileMerger()

while True:
    path = input(r'Please enter the absolute path to your PDF file: ')
    if os.path.isabs(path):
        keep_pages = input("Which pages of this document do you want to keep? \nEnter the page numbers separated by a comma or '0' to keep all of the pages: ")
        keep_pages = keep_pages.split(',')
        keep_pages = [int(x.strip()) for x in keep_pages] # Elements of this list will be passed as arguments to merger.append()
        
        try:
            # The 'pages' parameter within merger.append() accepts a tuple in the format of (start, stop[, step]). Default is None which represents all pages.
            
            if keep_pages[0] == 0: # Keep all pages in original document
                try:
                    merger.append(path)
                except FileNotFoundError:
                    file_not_found()
                    continue
                
            elif len(keep_pages) == 1: # Extract one specific page
                try:
                    merger.append(path, pages=(keep_pages[0] - 1, keep_pages[0]))
                except FileNotFoundError:
                    file_not_found()
                    continue
                          
            elif len(keep_pages) == 2: # Extract pages within a range
                try:
                    merger.append(path, pages=(keep_pages[0] - 1, keep_pages[1]))
                except FileNotFoundError:
                    file_not_found()
                    continue
        
            elif len(keep_pages) == 3: # Extract every second, third, etc. page within a range
                try:
                    merger.append(path, pages=(keep_pages[0] - 1, keep_pages[1], keep_pages[2]))
                except FileNotFoundError:
                    file_not_found()
                    continue
        
            cont = input('Do you want to add more PDF files? (y/n) ')
            if cont.lower() == 'n':
                break
        except IndexError:
            print('This document does not have that page number. Please try again.')
    else:
        print('That is not an absolute path. Please try again.')


output_filename = input('Please enter the name of the final combined file: ')
if not output_filename.endswith('.pdf'):
    output_filename += '.pdf'
    
merger.write(output_filename)

merger.close()