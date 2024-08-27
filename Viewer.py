import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os

img_files = []
button_list = []
extensions = ('.jpg', '.jpeg', '.img', '.png')
image_path = None

def select_folder():
    global path
    while True:
        os.system("clear")
        path = input("Enter accurate path to the folder you want to open pictures in: ").strip()
        if os.path.exists(path) and os.path.isdir(path):
            print("Opening folder, hold up...")
            return path
        else:
            print("Invalid path. Please try again.")

def selection_screen(root):
    global image_path
    img_files.clear()
    button_list.clear()

    def on_back_press():
        root.destroy()
        main()

    def on_exit_press():
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 200) // 2
        y = (screen_height - 100) // 2
        exit_win = tk.Toplevel()
        exit_win.geometry(f"200x100+{x}+{y}")
        exit_win.title("Confirm exit")
        label = Label(exit_win, text="Exit Image Viewer?", font=('Verdana', 10))
        label.place(x=50, y=25)
        button_yes = Button(exit_win, text='YES', command=root.quit)
        button_yes.place(x=20, y=40)
        button_no = Button(exit_win, text='NO', command=exit_win.destroy)
        button_no.place(x=80, y=40)
        exit_win.mainloop()

    button_back = Button(root, text='BACK', command=on_back_press)
    button_back.place(x=3, y=10)
    button_quit = Button(root, text="EXIT", command=on_exit_press)
    button_quit.place(x=600, y=570)

    root.geometry("800x600")
    root.title("Image Viewer")

    try:
        files = os.listdir(path)
        for file in files:
            if file.lower().endswith(extensions):
                img_files.append(file)
    except Exception as e:
        print(f"Error reading folder contents: {e}")
        root.destroy()
        exit()

    def on_click_img(img_filename):
       global image_path
       image_path = os.path.join(path, img_filename)
       root.destroy()
       picture_view()

    def on_click_forward():
        nonlocal counter
        if counter + 18 < len(img_files):
            counter += 18
        else:
            counter = len(img_files) - 18
        next_buttons = img_files[counter: counter + 18]
        for widget in button_list:
            widget.destroy()
        x, y = 100, 40
        button_list.clear()
        for name_img in next_buttons:
            buttons = Button(root, text=f"{name_img}", command=lambda img=name_img: on_click_img(img))
            buttons.place(x=x, y=y)
            button_list.append(buttons)
            y += 26
        button_backward.config(state=tk.NORMAL)
        if counter + 18 >= len(img_files):
            button_forward.config(state=tk.DISABLED)

    def on_editor_open(button):
        root.destroy()


    def on_backward_click():
        nonlocal counter
        if counter - 18 >= 0:
            counter -= 18
        else:
            counter = 0
        previous_buttons = img_files[counter: counter + 18]
        for widget in button_list:
            widget.destroy()
        x, y = 100, 40
        button_list.clear()
        for name_img in previous_buttons:
            buttons = Button(root, text=f"{name_img}", command=lambda img=name_img: on_click_img(img))
            buttons.place(x=x, y=y)
            button_list.append(buttons)
            y += 26
        button_forward.config(state=tk.NORMAL)
        if counter == 0:
            button_backward.config(state=tk.DISABLED)

    label = Label(root, text="Images in the folder are: ", font=('Roboto', 20))
    label.place(x=350, y=5)
    x, y = 100, 40

    for name in img_files[:18]:
        buttons = Button(root, text=f"{name}", command=lambda img=name: on_click_img(img))
        buttons.place(x=x, y=y)
        button_list.append(buttons)
        y += 26

    button_backward = Button(root, text='<', command=on_backward_click)
    button_forward = Button(root, text='>', command=on_click_forward)
    button_backward.place(x=300, y=550)
    button_forward.place(x=340, y=550)

    edit = Button(root, text='open editor', command=lambda:on_editor_open(edit))
    edit.place(x=650, y=20)

    if len(img_files) <= 18:
        button_forward.config(state=tk.DISABLED)

    counter = 0
    

    root.mainloop()
    return image_path
    

def main():
    path = select_folder()
    if path:
        root = Tk()
        selection_screen(root)

def resize_image(image, max_width, max_height):
    """Resize the image to fit within max_width and max_height while maintaining aspect ratio."""
    width, height = image.size
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if width / max_width > height / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        new_width, new_height = width, height

    resized_image = image.resize((new_width, new_height))
    return resized_image

def picture_view():
    global img_files
    global image_path

    current_index = img_files.index(os.path.basename(image_path))

    def show_image(index):
        nonlocal current_index
        if 0 <= index < len(img_files):
            image_path = os.path.join(path, img_files[index])
            try:
                img = Image.open(image_path)
                resized_img = resize_image(img, 1024, 768)
                tk_img = ImageTk.PhotoImage(resized_img)
                
                width = tk_img.width()
                height = tk_img.height()
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                x = (screen_width - width) // 2
                y = (screen_height - height) // 2
                window.geometry(f"{width + 50}x{height + 50}+{x}+{y}")
                
                label.config(image=tk_img)
                label.image = tk_img
                current_index = index
            except Exception as error:
                Label(window, text=f'Error: {error}').pack()

    def on_key_press(event):
        nonlocal current_index
        if event.keysym == 'Right':
            if current_index + 1 < len(img_files):
                show_image(current_index + 1)
        elif event.keysym == 'Left':
            if current_index - 1 >= 0:
                show_image(current_index - 1)
        elif event.keysym == 'Escape':
            window.destroy()
            selection_screen(root=tk.Tk())
    


    window = tk.Tk()
    window.title("Pictures")
    window.geometry('1024x768')

    if not image_path or not os.path.isfile(image_path):
        Label(window, text='No valid image selected or image path is incorrect.').pack()
        window.mainloop()
        return

    try:
        img = Image.open(image_path)
        resized_img = resize_image(img, 1024, 768)
        tk_img = ImageTk.PhotoImage(resized_img)
        width = tk_img.width()
        height = tk_img.height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width + 50}x{height + 50}+{x}+{y}")
        
        label = Label(window, image=tk_img)
        label.image = tk_img
        label.pack(fill=tk.BOTH, expand=True)

        window.bind('<KeyPress>', on_key_press)
        window.mainloop()
    except Exception as error:
        Label(window, text=f'Error: {error}').pack()

main()