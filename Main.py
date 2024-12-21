from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano.lsb import hide, reveal
from tkinter import messagebox
root = Tk()
root.title("Steganography - Hide a text in bmp image")
root.geometry ("1400x700+150+180")
root.resizable(False,False)
root.configure(bg='#CBD2A4')
selected_bits = IntVar(value=1)
modified_img = None

def showimage():
    global filename
    global img
    global img_display
    filename=filedialog.askopenfilename(initialdir=os.getcwd(), title='select Image File',
                                        filetype=(("BMP file","*.bmp"),
                                                  ("All file","*.txt") )
                                        )
    if filename:
        label2.config(image=None)
        label2.image = None
        img = Image.open(filename)
        img = img.resize((500, 400))
        img_display = ImageTk.PhotoImage(img)
        label1.config(image=img_display, width=500, height=400)
        label1.image = img_display
        
def Hide():
    global img
    global modified_img  
    global numOfBits
    message = text2.get(1.0, "end-1c").strip()
    binaryMessage = ''.join(format(ord(char), '08b') for char in message)
    binaryMessage += '00000000'  # Append termination pattern
    print(f"binary message: {binaryMessage} ")
    binaryLength = len(binaryMessage)
    print(f"Length of binary message: {binaryLength} bits")

    numOfBits = selected_bits.get()
    img = img.convert("RGB")
    pixels = img.load()

    messageIndex = 0
    for y in range(img.height):
        for x in range(img.width):
            if messageIndex < binaryLength:
                r, g, b = pixels[x, y]

                if numOfBits == 1 and messageIndex < binaryLength:
                    r = (r & ~1) | int(binaryMessage[messageIndex])
                    messageIndex += 1
                    if messageIndex < binaryLength:
                        g = (g & ~1) | int(binaryMessage[messageIndex])
                        messageIndex += 1
                    if messageIndex < binaryLength:
                        b = (b & ~1) | int(binaryMessage[messageIndex])
                        messageIndex += 1
                    pixels[x, y] = (r, g, b)
                
                elif numOfBits == 2 and messageIndex + 2 <= binaryLength:
                    r = (r & ~0b11) | int(binaryMessage[messageIndex:messageIndex + 2], 2)
                    messageIndex += 2
                    if messageIndex + 2 <= binaryLength:
                        g = (g & ~0b11) | int(binaryMessage[messageIndex:messageIndex + 2], 2)
                        messageIndex += 2
                    if messageIndex + 2 <= binaryLength:
                        b = (b & ~0b11) | int(binaryMessage[messageIndex:messageIndex + 2], 2)
                        messageIndex += 2
                    pixels[x, y] = (r, g, b)
                
                elif numOfBits == 3 and messageIndex + 3 <= binaryLength:
                    r = (r & ~0b111) | int(binaryMessage[messageIndex:messageIndex + 3], 2)
                    messageIndex += 3
                    if messageIndex + 3 <= binaryLength:
                        g = (g & ~0b111) | int(binaryMessage[messageIndex:messageIndex + 3], 2)
                        messageIndex += 3
                    if messageIndex + 3 <= binaryLength:
                        b = (b & ~0b111) | int(binaryMessage[messageIndex:messageIndex + 3], 2)
                        messageIndex += 3
                    pixels[x, y] = (r, g, b)

            if messageIndex >= binaryLength:
                break
        if messageIndex >= binaryLength:
            break

    modified_img = img  

    img_display_hidden = ImageTk.PhotoImage(modified_img)
    label2.configure(image=img_display_hidden, width=500, height=400)
    label2.image = img_display_hidden
    text2.delete(1.0, END)
    messagebox.showinfo("Success", "Text hidden successfully!")

def showdata():
    global numOfBits
    extractedMessage = ""
    numOfBits = selected_bits.get()
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]

            if numOfBits == 1:
                extractedMessage += str(r & 1)
                if extractedMessage.endswith('00000000'):
                   break
                extractedMessage += str(g & 1)
                if extractedMessage.endswith('00000000'):
                   break
                extractedMessage += str(b & 1)
                if extractedMessage.endswith('00000000'):
                   break
            elif numOfBits == 2:
                extractedMessage += format(r & 0b11, '02b')
                if extractedMessage.endswith('00000000'):
                   break
                extractedMessage += format(g & 0b11, '02b')
                if extractedMessage.endswith('00000000'):
                   break
                extractedMessage += format(b & 0b11, '02b')
                if extractedMessage.endswith('00000000'):
                   break
                
            elif numOfBits == 3:
                extractedMessage += format(r & 0b111, '03b')
                if extractedMessage.endswith('00000000'):
                   break
                extractedMessage += format(g & 0b111, '03b')
                if extractedMessage.endswith('00000000'):
                   break
                extractedMessage += format(b & 0b111, '03b')
                if extractedMessage.endswith('00000000'):
                   break
                

            # Check for termination pattern
            if extractedMessage.endswith('00000000'):
                extractedMessage = extractedMessage[:-8]  # Remove the termination pattern
                break
        if extractedMessage.endswith('00000000'):
            break

  
    decodedMessage = ''.join(chr(int(extractedMessage[i:i+8], 2)) for i in range(0, len(extractedMessage), 8))
    text2.delete(1.0, END)
    text2.insert(END, decodedMessage)

def openFile():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),title='select Text File',
                                          filetype=(("Text File","*.txt"),("All Files","*.*")))
    if filename:
        with open(filename,'r')as file:
            content=file.read()
            text2.delete(1.0,END)
            text2.insert(END, content)

def save():
    global modified_img  

    save_path = filedialog.asksaveasfilename(defaultextension=".bmp",
                                             filetypes=[("BMP file", "*.bmp")],
                                             title="Save Image As")


    if save_path:
        try:
            modified_img.save(save_path) 
            messagebox.showinfo("Image Saved", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save image: {e}")

image_icon=PhotoImage(file="images.png")
root.iconphoto(False,image_icon)

logo=PhotoImage(file="logo.png")
Label(root,image=logo,bg="#CBD2A4").place(x=10,y=0)
Label(root,text="Steganography",bg="#CBD2A4",fg="black",font="arial 25 bold").place(x=100,y=20)

# first frame
f1=Frame(root,bd=3,bg="white",width=500,height=400,relief=GROOVE)
f1.place(x=10,y=80)

label1=Label(f1,bg="white")
label1.place(x=0,y=0)

# second frame
f2=Frame(root,bd=3,bg="white",width=340,height=400,relief=GROOVE)
f2.place(x=520,y=80)

text2=Text(f2,font="Robote 20",bg="White",fg="black",relief=GROOVE,wrap=WORD)
text2.place(x=0,y=0,width=320, height=395)

Scrollbar1=Scrollbar(f2)
Scrollbar1.place(x=320,y=0, height=400)
Scrollbar1.configure(command=text2.yview)
text2.configure(yscrollcommand=Scrollbar1.set)


# third frame
f3=Frame(root,bd=3,bg="white",width=500,height=400,relief=GROOVE)
f3.place(x=880,y=80)
label2 = Label(f3, bg="white") 
label2.place(x=0, y=0)
#first control bar

cb1=Frame(root,bd=3,bg="#CBD2A4",width=500,height=150,relief=GROOVE)
cb1.place(x=10,y=500)

Button(cb1,text="Open Image", width=10, height =1, font="arial 14 bold",command=showimage).place(x=90,y=30)
Label(cb1, text="Add a bmp image", bg="#CBD2A4", fg="red").place(x=90, y=5)

#second control bar

cb2=Frame(root,bd=3,bg="#CBD2A4",width=340,height=150,relief=GROOVE)
cb2.place(x=520,y=500)
Button(cb2,text="Hide Data", width=10, height =1, font="arial 14 bold",command=Hide).place(x=20,y=80)
Button(cb2,text="Show Data", width=10, height =1, font="arial 14 bold",command=showdata).place(x=180,y=80)
Button(cb2,text="Upload text file", width=23, height =1, font="arial 14 bold",command=openFile).place(x=20,y=30)

#Label(cb2, text="Write the text you want to hide ", bg="#CBD2A4", fg="red").place(x=90, y=5)
Label(cb2, text="Bits:", bg="#CBD2A4", fg="black", font="arial 10 bold").place(x=10, y=5)
Radiobutton(cb2, text="1", variable=selected_bits, value=1, bg="#CBD2A4").place(x=60, y=5)
Radiobutton(cb2, text="2", variable=selected_bits, value=2, bg="#CBD2A4").place(x=100, y=5)
Radiobutton(cb2, text="3", variable=selected_bits, value=3, bg="#CBD2A4").place(x=140, y=5)
#third control bar

cb3=Frame(root,bd=3,bg="#CBD2A4",width=500,height=150,relief=GROOVE)
cb3.place(x=880,y=500)
Button(cb3,text="Save Image", width=10, height =1, font="arial 14 bold",command=save).place(x=90,y=30)
Label(cb3, text="Save the image ", bg="#CBD2A4", fg="red").place(x=90, y=5)

root.mainloop()



