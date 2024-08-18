class Settings: 
    def __init__(self): 

        self.s_width = 800
        self.s_height = 800

        self.play_width = 350  # meaning 30 width per block
        self.play_height = 700  # meaning 20 height per block
        self.block_size = self.play_width/10

        self.top_left_x = (self.s_width - self.play_width) // 2
        self.top_left_y = self.s_height - self.play_height

        # colors
        self.grid_line_color = (150,150,150)
        self.text_color = (255,255,255)
        self.game_background_color = (0,0,0)
        self.surface_color = (50,50,50)
        self.border_color = (0,0,0)