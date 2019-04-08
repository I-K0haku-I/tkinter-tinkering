from app.notes import NotesApp

if __name__ == "__main__":
    app = NotesApp()
    app.geometry('640x480')
    app.mainloop()
    app.destroy()
