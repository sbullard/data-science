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
        self.initial_cell = set()
        self.cells = set(cells)
        self.count = count
        self.safe_cells = set()
        self.mine_cells = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mine_cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safe_cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        self.mine_cells.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.safe_cells.add(cell)
        

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


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """

        #-----------------------------------------------------------------
        # 1. Add cell to self.moves_made and self.safes, and remove cell
        #    from self.available_moves as it is not longer available
        #----------------------------------------------------------------- 
   
        # 1a. Add cell to self.moves_made and self.safes
        self.moves_made.add(cell)
        self.safes.add(cell)
        
        # 1b. Remove cell from available moves
        if len(self.available_moves) > 0:
            if cell in self.available_moves:
                self.available_moves.remove(cell)


        #-----------------------------------------------------------------
        # 2. Get current move cells neighbors (if any), if count = 0,
        #    then add them to safe moves
        #-----------------------------------------------------------------

        # 2a. Get all of current cells neighbors that are still available
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell or i < 0 or j < 0 or i >= 8 or j >= 8:
                    continue
                else:
                    if (i,j) not in self.moves_made:
                        neighbors.add((i,j))

        # 2b. Mark all available neighbors of current cell that are safe
        if count == 0:
            for neighbor in neighbors:
                if neighbor not in self.moves_made:
                    self.safes.add(neighbor)


        #-----------------------------------------------------------------
        # 3. Create sentence for all available neighbors and add to KB
        #-----------------------------------------------------------------
        
        # If count of nearby cells passed in from runner.py == 0,
        # OR if then length of neighbors == count (all bombs), no sentence 
        if count == 0 or len(neighbors) == count:
            #print('DONT NEED TO CREATE A SENTENCE')
            pass            
        else: 
            sentence = Sentence(neighbors, count)
            sentence.initial_cell.add(cell)
            sentence.safe_cells.add(cell)
            sentence.initial_cell.add(cell)
            self.knowledge.append(sentence)
            print(f'---------------------------------------------------')
            print(f'\nNEW SENTENCE CREATED:')
            print(f'Move Cell: {sentence.initial_cell}')
            print(f'Neighbor Cells: {sentence.cells}')
            print(f'Bomb Count: {sentence.count}')
            print(f'---------------------------------------------------')
         
        
        #-----------------------------------------------------------------
        # 4. Update all sentences to reflect current cell information
        #-----------------------------------------------------------------

        # 4a. Remove current moves cell from all sentences        
        if len(self.knowledge) > 0:
            for i, sentence in enumerate(self.knowledge):
                # 4a. Remove the current moves cell from each sentence that
                #     contains it as the cell is no longer a threat.
                if cell in sentence.cells:
                    sentence.safe_cells.add(cell)
                    sentence.cells.remove(cell)
                    
                  
        # 4b. Check sentences to see if the length of sentence matches the count value
        #     if so then the sentence only contains mines. So add them to self.mines
        #     and sentence mine_cells
        if len(self.knowledge) > 0:
            for i, sentence in enumerate(self.knowledge):
                if sentence.count == len(sentence.cells):
                    for cell in sentence.cells:
                        self.mines.add(cell)
                        sentence.mine_cells.add(cell)
                        if cell in self.available_moves:  
                            self.available_moves.remove(cell)
                    print(f'\nMINE FOUND IN SENTENCE FOR CEL {sentence.initial_cell}:')
                    print(f'Move Cell: {sentence.initial_cell}')
                    print(f'Neighbor Cells: {sentence.cells}')
                    print(f'Bomb Count: {sentence.count}')
                    print(f'Safe Cells: {sentence.safe_cells}')
                    print(f'Mine Cells: {sentence.mine_cells}')
                    print(f'---------------------------------------------------')
             
                
        # 4c. Check each sentence for existing known mines from self.mines
        #     if a mine from self.mines is found in the sentence, then
        #     remove the mine and re-check the length to see if it matches
        #     the count. If so, the remaining cells are safe and the sentence
        #     can be deleted
        if len(self.mines) > 0 and len(self.knowledge) > 0:
            for mine in self.mines:
                for sentence in self.knowledge:
                    if mine in sentence.cells:
                        if sentence.count == 1:
                            # remove mine from sentence, and mark other cells safe
                            sentence.cells.remove(mine)
                            for c in sentence.cells:
                                print(f'{c} ADDED TO SAFE CELLS ')
                                self.safes.add(c)
                                sentence.safe_cells.add(c)                      
                        else:
                            # remove mine from sentence and subtract 1 from count
                            print(f'SENTENCE ADJUSTED FOR MINE:')
                            print(f'Original Sentence: {sentence}, Count: {sentence.count}')
                            sentence.mine_cells.add(mine)
                            sentence.cells.remove(mine)
                            sentence.count -= 1 
                            print(f'Adjusted Sentence: {sentence}, Count: {sentence.count}\n')


        # 4d Remove all safe cells from sentences (internal to sentences)
        if len(self.knowledge) > 0 and len(self.safes) > 0:
            for safe_cell in self.safes:
                for sentence in self.knowledge:
                    if safe_cell in sentence.cells:
                        sentence.cells.remove(safe_cell)
                        sentence.safe_cells.add(safe_cell)
                        
                        # Now that cell removed, do mine check
                        if sentence.cells == sentence.count:
                            for cell in sentence.cells:
                                self.mines.add(cell)
                                sentence.mine_cells.add(cell)
                                if cell in self.available_moves:  
                                    self.available_moves.remove(cell) 
                            print(f'\nMINE FOUND IN SENTENCE FOR CEL {sentence.initial_cell}:')
                            print(f'Move Cell: {sentence.initial_cell}')
                            print(f'Neighbor Cells: {sentence.cells}')
                            print(f'Bomb Count: {sentence.count}')
                            print(f'Safe Cells: {sentence.safe_cells}')
                            print(f'Mine Cells: {sentence.mine_cells}')
                            print(f'---------------------------------------------------')     

                    
        # 4e. Perform one final mine check against all sentences and delete as necessary
        if len(self.mines) > 0 and len(self.knowledge) > 0:
            for mine in self.mines:
                for sentence in self.knowledge:
                    if mine in sentence.cells:
                        if sentence.count == 1:
                            # remove mine from sentence, add all other cells to self.safes, 
                            # then delete sentence
                            sentence.cells.remove(mine)
                            for c in sentence.cells:
                                print(f'{c} ADDED TO SAFE CELLS ')
                                self.safes.add(c)
                                sentence.safe_cells.add(c)

                        else:
                            # remove mine from sentence and subtract 1 from count
                            print(f'SENTENCE ADJUSTED FOR MINE:')
                            print(f'Original Sentence: {sentence}, Count: {sentence.count}')
                            sentence.mine_cells.add(mine)
                            sentence.cells.remove(mine)
                            sentence.count -= 1 
                            print(f'Adjusted Sentence: {sentence}, Count: {sentence.count}\n')


        #-----------------------------------------------------------------
        # 5. Create subsets from existing sentences if possible
        #-----------------------------------------------------------------
      
#        # 5b. Create new Sentence if possible
#        if len(self.knowledge) > 1:
#            for i in range(0, len(self.knowledge)-1):
#                for j in range(i+1, len(self.knowledge)):
#                    if self.knowledge[i].cells == self.knowledge[j].cells:
#                        continue  
#                    elif self.knowledge[i].count == self.knowledge[j].count:
#                        continue
#                    elif not self.knowledge[i].cells.intersection(self.knowledge[j].cells):
#                        continue
#                    else:
#                        print(f'NEW SENTENCE CREATED FROM TWO OTHERS')
#                        print(f'Original Sentence #{i}: {self.knowledge[i].cells}, Count: {self.knowledge[i].count}')
#                        print(f'Original Sentence #{j}: {self.knowledge[j].cells}, Count: {self.knowledge[j].count}')
#                        if self.knowledge[i].count > self.knowledge[j].count:
#                            new_s = self.knowledge[i].cells - self.knowledge[j].cells
#                            new_c = self.knowledge[i].count - self.knowledge[j].count
#                            self.knowledge.append(Sentence(new_s, new_c) )
#                        else:
#                            new_s = self.knowledge[j].cells - self.knowledge[i].cells
#                            new_c = self.knowledge[j].count - self.knowledge[i].count
#                            self.knowledge.append(Sentence(new_s, new_c))

        print(f'All Available Moves: {self.available_moves}\n')
        print(f'All Moves Made: {self.moves_made}\n')
        print(f'All Marked Safes: {self.safes}\n')
        print(f'All Marked Mines: {self.mines}\n')
  
        for i, s in enumerate(self.knowledge):
            print(f'Number of Senteces in KB: {len(self.knowledge)}')
            print(f'KB S{i}: {s}, Count: {s.count}\n')
                            

                               
                                    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """       
        # ALWAYS RUN A CHECK TO ENSURE THAT NO MINES IN MINE LIST ARE IN SAFES LIST
        # IF THEY ARE, MUST REMOVE THE MINE MOVE FROM SAFES

        if len(self.safes) == 0:
            return None
        else:
            for c in self.safes:
                if c not in self.moves_made:
                    print(f'Safe Move: {c}')
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
        rmove = random.choice(list(self.available_moves))
        print(f'Random Move: {rmove}')
        return(rmove)
