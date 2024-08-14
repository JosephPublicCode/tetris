class Settings: 
    def __init__(self): 

        self.s_width = 800
        self.s_height = 700

        self.play_width = 300  # meaning 30 width per block
        self.play_height = 600  # meaning 20 height per block
        self.block_size = 30

        self.top_left_x = (self.s_width - self.play_width) // 2
        self.top_left_y = self.s_height - self.play_height