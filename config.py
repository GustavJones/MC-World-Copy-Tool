import os, re

class Config:
    def __init__(self, file_name, config_dir, default_text : list = None) -> None:
        '''
        file_name: The name of the config file \n
        config_dir: The directory of the config file \n
        '''
        
        self.config_dir = config_dir
        self.file_name = file_name
        
        if not os.path.exists(os.path.join(self.config_dir, self.file_name + ".txt")):
            self.file = open(os.path.join(self.config_dir, self.file_name + ".txt"), "x")
            
            if default_text != None:
                for line in default_text:
                    if line != "\n":
                        self.file.write(line + "\n")
                    else:
                        self.file.write(line)
                self.file.close()
                
            self.file = open(os.path.join(self.config_dir, self.file_name + ".txt"), "r+")
            
        else:
            self.file = open(os.path.join(self.config_dir, self.file_name + ".txt"), "r+")
            
        self.raw_content = self.file.readlines()
        self.sorted_content = []
        self.content_indexes = []
        
        for index, line in enumerate(self.raw_content):
            if line[0] != "#":
                if line.strip("\n") != "":
                    self.sorted_content.append(line.strip("\n"))
                    self.content_indexes.append(index)
                    
        self.file.close()
                    
    def get_value(self, variable):
        for value in self.sorted_content:
            if variable in value:
                return re.findall(r'"([^"]*)"', value)[0]
            
    def set_value(self, variable, new_value):
        for index, value in enumerate(self.sorted_content):
            if variable in value:
                old_val = re.findall(r'"([^"]*)"', value)[0]
                if old_val == "":
                    self.sorted_content[index] = self.sorted_content[index].replace('""', '"old_val"')
                    old_val = "old_val"
                self.sorted_content[index] = self.sorted_content[index].replace(old_val, new_value)
                
        for i, line_index in enumerate(self.content_indexes):
            self.raw_content[line_index] = self.sorted_content[i] + "\n"
            
        self.file = open(os.path.join(self.config_dir, self.file_name + ".txt"), "w")
        self.file.writelines(self.raw_content)
        self.file.close()