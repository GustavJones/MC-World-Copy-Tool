import os, shutil, nbtlib
from config import Config
import PySimpleGUI as sg

def main_program():
    default_text = [
        '# This is the settings file for Minecraft World Copy Tool',
        '\n'
        '# Enter your Minecraft Installation directory here e.g. "C:\\Users\\YOUR_USERNAME\\AppData\\Roaming\\.minecraft"',
        'minecraft_dir = ""'
    ]
    
    config_file = Config("settings", os.getcwd(), default_text)

    minecraft_path = config_file.get_value("minecraft_dir")

    worlds = []
    try:
        for folder in os.listdir(os.path.join(minecraft_path, "saves")):
            worlds.append(folder)
    except:
        pass

    sg.theme("BrownBlue")
    
    if minecraft_path == "":
        display_text = "No Folder Selected!"
    else:
        display_text = minecraft_path

    layout = [
        [sg.Text("Welcome To Minecraft World Copy Tool!\n", font="Arial 20 bold underline", text_color="#0b4e9c")],
        [sg.Text("Path To Minecraft Installation: "+ display_text, key="dir", font="Arial 12")],
        [sg.Text("Change Path: ", font="Arial 11"), sg.Input("", key="path"), sg.FolderBrowse()],
        [sg.Column([[sg.Button("Update Path In Config", auto_size_button=True)]], justification="center", pad=10)],
        [sg.Text("Minecraft World Saves: ", font="Arial 14 bold"), sg.Combo(worlds, key="worlds_list", size=50, readonly=True, default_value="None")],
        [sg.Checkbox("Load With Cheats", pad=5, font="Arial 10", key="cheats")],
        [sg.Column([[sg.Button("Copy World Save!", auto_size_button=True, font="Arial 20 bold")], [sg.Text("", key="errors")]], justification="center")]
    ]

    window = sg.Window("Minecraft World Copy Tool", layout, finalize=True)

    def update_worlds():
        try:
            worlds = []
            for folder in os.listdir(os.path.join(minecraft_path, "saves")):
                worlds.append(folder)
                window["worlds_list"].update("None", worlds)
        except:
            window["worlds_list"].update("None", [])
            
    def change_nbt(selected_world):
        try:
            file = nbtlib.load(os.path.join(minecraft_path, "saves", selected_world, "level.dat"))
            file["Data"]["allowCommands"] = nbtlib.tag.Byte(1)
            
            return file
        except:
            window["errors"].update("Something Went Wrong")
        
    def change_name(selected_world):
        try:
            file = nbtlib.load(os.path.join(minecraft_path, "saves", selected_world + "_Copy", "level.dat"))
            file["Data"]["LevelName"] = nbtlib.tag.String(file["Data"]["LevelName"] + " - Copy")
            
            return file
        except:
            window["errors"].update("Something Went Wrong")
        
    def make_copy(selected_world):
        try:
            shutil.copytree(os.path.join(minecraft_path, "saves", selected_world), os.path.join(minecraft_path, "saves", selected_world + "_Copy"))
            window["errors"].update("Success!")
        except:
            window["errors"].update("Error")

    while True:    
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == "Quit":
            break
        
        if event == "Update Path In Config":
            if str(values["path"]) != "":
                config_file.set_value("minecraft_dir", str(values["path"]))
                window["dir"].update("Path To Minecraft Installation: "+ config_file.get_value("minecraft_dir"))
                minecraft_path = config_file.get_value("minecraft_dir")
                update_worlds()
                
        if event == "Copy World Save!":
            if window["worlds_list"].get() != "" and window["worlds_list"].get() != "None":
                selected_world = window["worlds_list"].get()
                window["errors"].update("")
                if window["cheats"].get():
                    make_copy(selected_world)
                    change_nbt(selected_world).save(os.path.join(minecraft_path, "saves", selected_world + "_Copy", "level.dat"))
                    change_name(selected_world).save(os.path.join(minecraft_path, "saves", selected_world + "_Copy", "level.dat"))
                else:
                    make_copy(selected_world)
                    change_name(selected_world).save(os.path.join(minecraft_path, "saves", selected_world + "_Copy", "level.dat"))
                    
if __name__ == "__main__":
    main_program()