class Score: 

    def update_score(self,new_score): 
        # reads the high score.
        with open("tetris/high_score.txt","r") as f: 
            lines = f.readlines()
            score = lines[0].strip()
        
        # writes the new high score. 
        with open("tetris/high_score.txt",'w') as f: 
            if int(score) > new_score:
                f.write(str(score))
            else:
                f.write(str(new_score))
    
    def max_score(self): 
        with open("tetris/high_score.txt","r") as f: 
            lines = f.readlines()
            score = lines[0].strip()
        return score
