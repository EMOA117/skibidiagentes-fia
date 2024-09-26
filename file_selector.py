from tkinter import filedialog, Tk

class FileSelector:
    @staticmethod
    def seleccionar_archivo():
        root = Tk()
        root.withdraw()  # Oculta la ventana principal de Tkinter
        archivo = filedialog.askopenfilename(
            title="Selecciona archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Archivos CSV", "*.csv")]
        )
        root.destroy()  # Destruye la ventana después de seleccionar el archivo
