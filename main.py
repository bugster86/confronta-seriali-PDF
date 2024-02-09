import PyPDF2
import fitz
import re
import sys
import tkinter as tk
from tkinter import filedialog
from functools import partial
from tkinter import messagebox

def confronta_file_pdf(file_pdf1,file_pdf2):
    codici_seriali1 = set()
    codici_seriali2 = set()
    regex_seriale = re.compile(r'Nr\. Seriale: (\w+)', re.IGNORECASE)
    regex_lotto = re.compile(r'Nr\. Lotto: (\w+)', re.IGNORECASE)
    regex_mac = re.compile(r'Nr\. Seriale: (\w+|\d{2}:\d{2}:\d{2}:\w{2}:\w{2}:\w{2})', re.IGNORECASE)
    
    #print ("\n\n")
    
    with fitz.open(file_pdf1) as pdf_file:
        for pagina in range(pdf_file.page_count):
            pagina_corrente = pdf_file[pagina]
            testo_pagina = pagina_corrente.get_text()
            #print (testo_pagina)
            
            match = regex_seriale.findall(testo_pagina)
            if match:
                codici_seriali1.update(match)
                
            match = regex_lotto.findall(testo_pagina)
            if match:
                codici_seriali1.update(match)
            
            match = regex_mac.findall(testo_pagina)
            if match:
                codici_seriali1.update(match)
            
    #print ("Codici del file {} \n".format(file_pdf1),codici_seriali1)
        
    #print ("\n\n")
       
    with fitz.open(file_pdf2) as pdf_file:
        for pagina in range(pdf_file.page_count):
            pagina_corrente = pdf_file[pagina]
            testo_pagina = pagina_corrente.get_text()
            #print (testo_pagina)
            
            match = regex_seriale.findall(testo_pagina)
            if match:
                codici_seriali2.update(match)
                
            match = regex_lotto.findall(testo_pagina)
            if match:
                codici_seriali2.update(match)
                
            match = regex_mac.findall(testo_pagina)
            if match:
                codici_seriali2.update(match)
            
    #print ("Codici del file {} \n".format(file_pdf2),codici_seriali2)
    
    differenza=codici_seriali1-codici_seriali2
    return differenza


def scegli_file(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)
    
def confronta_e_visualizza():

        file1=entry_file1.get()
        file2=entry_file2.get()
        try:
            differenza = confronta_file_pdf(file1, file2)
            
            #for i in range(100):
            #    differenza.add(str(i))
            
            if len(differenza) > 0:
                risultato_str = "\n".join(differenza)
                messagebox.showinfo("Risultato Confronto", f"Differenze rilevate:\n{risultato_str}")
            else:
                messagebox.showinfo("Risultato Confronto", f"Nessuna differenza")

        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")

if __name__ == "__main__":


    root = tk.Tk()
    root.title("Confronto PDF")

    label_file1 = tk.Label(root, text="Seleziona il primo file PDF:")
    label_file1.grid(row=0, column=0, padx=10, pady=10)

    entry_file1 = tk.Entry(root, width=40)
    entry_file1.grid(row=0, column=1, padx=10, pady=10)

    button_scegli_file1 = tk.Button(root, text="Scegli", command=partial(scegli_file, entry_file1))
    button_scegli_file1.grid(row=0, column=2, padx=10, pady=10)

    label_file2 = tk.Label(root, text="Seleziona il secondo file PDF:")
    label_file2.grid(row=1, column=0, padx=10, pady=10)

    entry_file2 = tk.Entry(root, width=40)
    entry_file2.grid(row=1, column=1, padx=10, pady=10)

    button_scegli_file2 = tk.Button(root, text="Scegli", command=partial(scegli_file, entry_file2))
    button_scegli_file2.grid(row=1, column=2, padx=10, pady=10)

    button_confronta = tk.Button(root, text="Confronta", command=partial(confronta_e_visualizza))
    button_confronta.grid(row=2, column=1, pady=20)

    root.mainloop()

    
