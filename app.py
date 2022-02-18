import tkinter as tk
import random
import os.path

categories = [""]
categoriesDictionary = {
}

otherNames = {}

category_name_text_preview = "enter category name"
names_text_preview = "enter name : discordname/league name\npersons separated with a comma."

root = tk.Tk()
root.title("Get a person")
root.geometry("500x200")

add_category_window = tk.Toplevel(root)
add_category_window.geometry("500x300")
add_category_window.title("Add a new category")
add_category_window.withdraw()

canvas = tk.Canvas(root, width=500, height=200, bg="#232323")
canvas.pack()
label = tk.Label(canvas, text="", bg="#232323", fg="#ffffff")
label.place(x=25, y=150)

variable = tk.StringVar(canvas)
variable.set(categories[0])

opt = tk.OptionMenu(canvas, variable, *categories)
opt.config(bg="#111111", fg="#ffffff")
opt["menu"].config(bg="#111111", fg="#ffffff")
opt.place(x=25, y=50)

second_canvas = tk.Canvas(add_category_window, width=500, height=300, bg="#232323")
second_canvas.pack()

category_name = tk.Entry(second_canvas)
category_name.insert(0, category_name_text_preview)
category_name.place(x=30, y=50)

names = tk.Text(second_canvas, height=10, width=50)
names.insert(tk.END, names_text_preview)
names.place(x=30, y=75)

enter_category = tk.Button(second_canvas, text="enter category", bg="#111111", fg="#ffffff",
                           command=lambda: new_category(category_name.get(), names.get("1.0", "end-1c")))
enter_category.place(x=350, y=250)


def read_file():
    if os.path.isfile("saved_categories.txt"):
        with open('saved_categories.txt', 'r') as f:
            try:
                for line in f.readlines():
                    line = line.rstrip()
                    name, dictionary = line.split("=")
                    dictionary = dictionary.split(",")
                    categories.append(name)
                    locals()[name] = dictionary
                    categoriesDictionary[name] = locals()[name]
            except ValueError:
                pass
            finally:
                update_option_menu()


def save_other_names():
    with open('other_names.txt', 'w') as f:
        for key, value in otherNames.items():
            f.write(key + ":" + value +"\n")


def read_other_names():
    if os.path.isfile("other_names.txt"):
        with open('other_names.txt', 'r') as f:
            for line in f.readlines():
                if line != "\n":
                    key, value = line.split(":")
                    otherNames[key] = value


def save_in_file(category_to_add):
    with open('saved_categories.txt', 'a') as f:
        dictionary = categoriesDictionary.get(category_to_add)
        text = ""
        for name in dictionary:
            text += name
            if name != dictionary[len(dictionary) - 1]:
                text += ","
            else:
                text += "\n"
        f.write(category_to_add + "=" + text)


def update_option_menu():
    menu = opt["menu"]
    menu.delete(0, "end")
    for string in categories:
        menu.add_command(label=string,
                         command=lambda value=string: variable.set(value))


def edit_in_file(name):
    with open('saved_categories.txt', 'r') as f:
        lines = f.readlines()
    with open('saved_categories.txt', 'w') as f:
        for line in lines:
            if name not in line:
                f.write(line)
            else:
                dictionary = categoriesDictionary.get(name)
                text = ""
                for item in dictionary:
                    text += item
                    if item != dictionary[len(dictionary) - 1]:
                        text += ","
                    else:
                        text += "\n"
                f.write(name + "=" + text)


def get_a_person():
    chosen_list = []
    for category in categoriesDictionary:
        if category == variable.get():
            chosen_list = categoriesDictionary.get(category)
    try:
        random_person_index = random.randint(0, len(chosen_list) - 1)
        random_person = chosen_list[random_person_index]
        if random_person in otherNames:
            social_name = otherNames.get(random_person)
            label.config(text=random_person + " : " + social_name)
        else:
            label.config(text=random_person)
        label.place(x=25, y=150)
    except ValueError:
        label.config(text="Diese Kategorie ist leer.")
        label.place(x=25, y=150)


def new_category(name, namelist):
    is_new = True
    for category in categories:
        if name == category:
            is_new = False
    namelist = namelist.replace(" ", "")
    different_names = namelist.split(",")
    persons = []
    in_game_names = []
    for n in different_names:
        try:
            person, in_game_name = n.split(":")
            persons.append(person)
            in_game_names.append(in_game_name)
        except ValueError:
            persons.append(n)
            in_game_names.append(" ")
    locals()[name] = persons
    categoriesDictionary[name] = locals()[name]
    for new_ingame_name in in_game_names:
        if new_ingame_name == " ":
            continue
        counter = 0
        for normalName, socialName in otherNames.items():
            if normalName != persons[in_game_names.index(new_ingame_name)] or new_ingame_name not in socialName:
                counter += 1
        if counter == len(otherNames):
            if persons[in_game_names.index(new_ingame_name)] in otherNames.keys():
                socialName = otherNames[persons[in_game_names.index(new_ingame_name)]]
                otherNames[persons[in_game_names.index(new_ingame_name)]] = new_ingame_name + "/" + socialName
            else:
                otherNames[persons[in_game_names.index(new_ingame_name)]] = new_ingame_name
    if is_new:
        categories.append(name)
        save_in_file(name)
    else:
        edit_in_file(name)
    save_other_names()
    update_option_menu()
    names.delete("1.0", "end")
    names.insert(tk.END, names_text_preview)
    category_name.delete(0, "end")
    category_name.insert(0, category_name_text_preview)
    add_category_window.withdraw()


def add_a_category():
    add_category_window.deiconify()
    add_category_window.mainloop()


getAPerson = tk.Button(canvas, text="Get a random Person", bg="#111111", fg="#ffffff", command=get_a_person)
getAPerson.place(x=320, y=150)

addACategory = tk.Button(canvas, text="Add a category", bg="#111111", fg="#ffffff", command=add_a_category)
addACategory.place(x=320, y=20)

read_file()
read_other_names()

root.mainloop()
