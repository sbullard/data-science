import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.safe_cells = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return(self.safe_cells)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.safe_cells.add(cell)
            self.cells.remove(cell)
        

class MinesweeperAI():
    """
    Minesweeper game player
    """
    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # All available moves at start of game
        self.available_moves = set()

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #-----------------------------------------------------------------
        # 1. ADD AND REMOVE CURRENT MOVE CELL AS NECESSARY
        #----------------------------------------------------------------- 
   
        # 1a. Add cell to self.moves_made
        self.moves_made.add(cell)
        
        # 1b. Remove cell from available moves
        if len(self.available_moves) > 0:
            self.available_moves.remove(cell)
        
        # 1c. Remove cell from self.safes as it is no longer eligable
        if cell in self.safes: 
            self.safes.remove(cell)


        #-----------------------------------------------------------------
        # 2. MARK CURRENT MOVE CELL AS SAFE IF AND GET ALL SURROUND CELLS
        #-----------------------------------------------------------------

        # 2b. Get all of current cells neighbors that are still available
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell or i < 0 or j < 0 or i >= 8 or j >= 8:
                    continue
                else:
                    if (i,j) not in self.moves_made:
                        neighbors.add((i,j))

        # 2a. Mark all available neighbors of current cell that are safe
        if count == 0:
            for neighbor in neighbors:
                if neighbor not in self.moves_made:
                    self.mark_safe(neighbor)

        #print(f'Available Moves: {self.available_moves}') 
        #print(f'Moves Made: {self.moves_made}')
        #print(f'Current Move Cell: {cell}')
        #print(f'All Available Neighbors: {neighbors}')
        #print(f'Safe Cells: {self.safes}')
 
         
        #-----------------------------------------------------------------
        # 3. Create Sentence for all available neighbors and add to KB
        #-----------------------------------------------------------------
                
        if count == 0 or len(neighbors) == count:
            #print('DONT NEED TO CREATE A SENTENCE')
            pass             
        else: 
            sentence = Sentence(neighbors, count)
            self.knowledge.append(sentence)
           

        #-----------------------------------------------------------------
        # 4. Update all sentences to reflect current cell information
        #-----------------------------------------------------------------
        for i, sentence in enumerate(self.knowledge):
            #print(f'Original Sentence #{i+1}: {sentence}')
            #print(f'Sentence #{i+1} Known Safe Cells: {sentence.safe_cells}')
            
            # 4a. Mark the cell as safe in each sentence that contains it and remove
            #     the cell from each sentence as it is no longer eligible. 
            if cell in sentence.cells:
                sentence.mark_safe(cell)

            #print(f'Adjusted Sentence #{i+1} in KB: {sentence}')
            #print(f'Adjusted Sentence #{i+1} Known Safe Cells: {sentence.safe_cells}')

         
        # 4b. Check each sentence for mines. If the count of the current cell
        #     matches the number of cells in the sentence, then they are all mines
        #     and at this point the sentence can be removed from KB.

        for i, sentence in enumerate(self.knowledge):
            if sentence.count == len(sentence.cells):
                for cel in sentence.cells:
                    self.mark_mine(cel)
                    if cel in self.available_moves:  
                        self.available_moves.remove(cel)
                self.knowledge.remove(sentence)
     

        #-----------------------------------------------------------------
        # 5. Create subsets from existing sentences if possible
        #-----------------------------------------------------------------
        if len(self.knowledge) > 1:
            for i in range(0, len(self.knowledge)-1):
                for j in range(i+1, len(self.knowledge)):
                    if len(self.knowledge[i].cells) == len(self.knowledge[j].cells):
                        continue
                    elif not self.knowledge[i].cells.intersection(self.knowledge[j].cells):
                        continue
                    else:                                             
                        if len(self.knowledge[i].cells) > len(self.knowledge[j].cells):
                        #if self.knowledge[i].count > self.knowledge[j].count:
                            new_cells = self.knowledge[i].cells - self.knowledge[j].cells
                            new_count = self.knowledge[i].count - self.knowledge[j].count
                            print(f'Possible New Sentence: {new_cells}')
                            print(f'Comes from: {self.knowledge[i].cells} and: {self.knowledge[j].cells}')  
                            print(f'Original Counts: i: {self.knowledge[i].count}, j: {self.knowledge[j].count}')
                            print(f'New Sentence Count Value: {new_count}')
                            if new_count == 0:
                                print('NEW COUNT FUCKING EQUALS ZERIO')
                                for cel in new_cells: 
                                    self.safes.add(cel)
# HERE IS WHERE PART OF PROBLEM IS, MUST REMOVE ALL ADDED SAFE CELL FROM ALL SENTENCES IN KB AFTER
                                    print(f'{cel} added to Safes: {self.safes}')
                            else:
                                new_sentence = Sentence(new_cells, new_count)
                                self.knowledge.append(new_sentence)
                                print(f'New Sentence Created: {new_sentence}')
                                continue
                        else:
                            new_cells = self.knowledge[j].cells - self.knowledge[i].cells
                            new_count = self.knowledge[j].count - self.knowledge[i].count
                            print(f'Possible New Sentence: {new_cells}')
                            print(f'Comes from: {self.knowledge[j].cells} and: {self.knowledge[i].cells}')  
                            print(f'Original Counts: j: {self.knowledge[j].count}, i: {self.knowledge[i].count}') 
                            print(f'New Sentence Count Value: {new_count}')
                            if new_count == 0:
                                print('NEW COUNT FUCKING EQUALS ZERO TIMES TWO!!!!')
                                for cel in new_cells: 
                                    self.safes.add(cel)
                                    print(f'{cel} added to Safes: {self.safes}')
                            else:
                                new_sentence = Sentence(new_cells, new_count)
                                self.knowledge.append(new_sentence)
                                print(f'New Sentence Created: {new_sentence}')
                                continue
                            

     

            
            
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None
        else:
            for c in self.safes:
                if c not in self.moves_made:
                    return(c)
                    break


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # If KB is empty, make random move
        if len(self.available_moves) == 0:
            for i in range(0, self.height):
                for j in range(0, self.height):
                    self.available_moves.add((i,j))

        return(random.choice(list(self.available_moves)))
