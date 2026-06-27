import tkinter as tk

window=tk.Tk()
window.title("Chess")
window.geometry('850x700')

canvas=tk.Canvas(window,height=656,width=656,bg='black',highlightthickness=0)
canvas.pack()

size=82

board=[[None for _ in range(8)] for _ in range(8)]

selected_square=None
row=-1
col=-1
piece=''
can_move=False
black=['♜','♞','♝','♛','♚','♝','♞','♜','♟']
white=['♖','♘','♗','♕','♔','♗','♘','♖','♙']
white_king_moved=False
black_king_moved=False
legal=[]
white_king_position=[7,4]
black_king_position=[0,4]
move=0
castling=False

def draw_board():
    for i in range(8):
        for j in range(8):
            if i%2==0:
                if j%2==0:
                    canvas.create_rectangle(j*size,i*size,(j+1)*size,(i+1)*size,fill='grey',outline='')
                else:
                    canvas.create_rectangle(j*size,i*size,(j+1)*size,(i+1)*size,fill='brown',outline='')
            else:
                if j%2==0:
                    canvas.create_rectangle(j*size,i*size,(j+1)*size,(i+1)*size,fill='brown',outline='')
                else:
                    canvas.create_rectangle(j*size,i*size,(j+1)*size,(i+1)*size,fill='grey',outline='')


def click(event):
    global size,selected_square,col,row,board,piece,can_move,legal,white_king_position,black_king_position,move,white,black
    promote=False
    row=event.y//size
    col=event.x//size
    if selected_square==None:
        selected_square=(row,col)
        piece=board[selected_square[0]][selected_square[1]]
        legal=highlight(row,col,piece,board)
        

    else:
        piece=board[selected_square[0]][selected_square[1]]
        print(row,col)
        if piece=='♔':
            if [row,col] in legal:
                if not in_check(row,col,piece,board):
                    can_move=True
                    white_king_position=[row,col]
        if piece=='♚':
            if [row,col] in legal:
                if not in_check(row,col,piece,board):
                    can_move=True
                    black_king_position=[row,col]
        if piece=='♜' or piece=='♖':
            if [row,col] in legal:
                can_move=True
        if piece=='♗' or piece=='♝':
            if [row,col] in legal:
                can_move=True
        if piece=='♛' or piece=='♕':
            if [row,col] in legal:
                can_move=True
        if piece=='♘' or piece=='♞':
            if [row,col] in legal:
                can_move=True
        if piece=='♟' or piece=='♙':
            if [row,col] in legal:
                can_move=True
        color='white' if piece in white else 'black'
        if own_piece(row,col,color,board):
            can_move=False
        if move%2==0 and piece not in ('♖','♘','♗','♕','♔','♗','♘','♖','♙'):
            can_move=False
        elif move%2!=0 and piece not in ('♜','♞','♝','♛','♚','♝','♞','♜','♟'):
            can_move=False
        if can_move:
            if (piece=='♟' and row==7) or (piece=='♙' and row==0):
                promote=True
            canvas.delete('all')
            move_piece()
            draw_board()
            draw_piece()
        if promote:
            pawn_promotion()
            promote=False
        selected_square=None
        piece=''
        can_move=False
        game_end()
        

def draw_piece():
    global board,size,black
    for row in range(8):
        for col in range(8):
            if board[row][col]!=None:
                if board[row][col] in black:
                    canvas.create_text((col*size)+(size//2),(row*size)+(size//2),text=board[row][col],font=('Arial',45),fill='black')
                else:
                    canvas.create_text((col*size)+(size//2),(row*size)+(size//2),text=board[row][col],font=('Arial',45),fill='white')

def create_board():
    global board
    board[1]=['♟']*8
    board[6]=['♙']*8
    board[0]=['♜','♞','♝','♛','♚','♝','♞','♜']
    board[7]=['♖','♘','♗','♕','♔','♗','♘','♖']
        
def is_piece(move):
    global board
    if board[move[0]][move[1]]!=None:
        return True
    
def castle():
    global selected_square,piece,board,castling
    row=selected_square[0]
    moves=[]
    k_side=True
    Q_side=True
    attacks=all_attacks(piece,board)
    # if (piece=='♔' and row!=7) or (piece=='♚' and row!=0):
    #     castling=False
    #     return moves
    for column in (2,6):
        if column==6:
            k_col=4
            for _ in range(2):
                k_col+=1
                if (is_piece([row,k_col])) or ([row,k_col] in attacks):
                    k_side=False
                    break
        elif column==2:
            k_col=4
            for _ in range(2):
                k_col-=1
                if (is_piece([row,k_col])) or ([row,k_col] in attacks):
                    Q_side=False
                    break
    if k_side:
        moves.append([row,6])
    if Q_side:
        moves.append([row,2])
    if moves!=None:
        castling=True
    return moves
        

def own_piece(row,col,color,board):
    global white,selected_square,black
    if color=='black' and board[row][col] in black:
        return True
    # elif board[selected_square[0]][selected_square[1]] in white and board[row][col] in white:
    elif color=='white' and board[row][col] in white:
        return True
    else: 
        return False
    
def move_piece():
    global selected_square,row,col,board,piece,white_king_position,white_king_moved,black_king_moved,move
    dummy_board=[row.copy() for row in board]
    dummy_board[selected_square[0]][selected_square[1]]=None
    dummy_board[row][col]=piece
    if move%2==0:
        if in_check(white_king_position[0],white_king_position[1],'♔',dummy_board):
            return
    elif move%2!=0:
        if in_check(black_king_position[0],white_king_position[1],'♚',dummy_board):
            return
    if (piece=='♔' and row==7) or (piece=='♚' and row==0):
        if castling==True:
            if col==6:
                temp=board[row][7]
                board[row][4]=None
                board[row][7]=None
                board[row][6]=piece
                board[row][5]=temp
                move+=1
                return
            elif col==2:
                temp=board[row][0]
                board[row][4]=None
                board[row][0]=None
                board[row][1]=piece
                board[row][2]=temp
                move+=1
                return
    board[selected_square[0]][selected_square[1]]=None
    board[row][col]=piece
    move+=1
    if piece=='♔':
        white_king_moved=True
    elif piece=='♚':
        black_king_moved=True
    return

def pawn_promotion():
    global row,col,board
    def place_piece(piece):
        board[row][col]=piece
        box.destroy()
        canvas.delete('all')
        draw_board()
        draw_piece()
    box=tk.Toplevel(window)
    box.title("Promotion")
    box.geometry('255x70')
    if row==0:
        queen_button=tk.Button(box,text='♕',font=('Arial',25),command=lambda : place_piece('♕'))
        rook_button=tk.Button(box,text='♖',font=('Arial',25),command=lambda : place_piece('♖'))
        bishop_button=tk.Button(box,text='♗',font=('Arial',25),command=lambda : place_piece('♗'))
        knight_button=tk.Button(box,text='♘',font=('Arial',25),command=lambda : place_piece('♘'))
        queen_button.grid(row=0,column=0)
        rook_button.grid(row=0,column=1)
        bishop_button.grid(row=0,column=2)
        knight_button.grid(row=0,column=3)
    else:
        queen_button=tk.Button(box,text='♛',font=('Arial',25),command=lambda : place_piece('♛'))
        rook_button=tk.Button(box,text='♜',font=('Arial',25),command=lambda : place_piece('♜'))
        bishop_button=tk.Button(box,text='♝',font=('Arial',25),command=lambda : place_piece('♝'))
        knight_button=tk.Button(box,text='♞',font=('Arial',25),command=lambda : place_piece('♞'))
        queen_button.grid(row=0,column=0)
        rook_button.grid(row=0,column=1)
        bishop_button.grid(row=0,column=2)
        knight_button.grid(row=0,column=3)

class Highlight:
    def __init__(self,row,col,piece,board):
        global size,selected_square,white,black
        self.row=row
        self.col=col
        self.piece=piece
        self.size=size
        self.legal_moves=[]
        self.board=board
        self.color='white' if piece in white else 'black'
    def king(self):
        king=[self.row-1,self.col-1]
        update=[[0,1],[1,0],[0,-1],[-1,0]]
        for up in update:
            for _ in range(2):
                king=[king[0]+up[0],king[1]+up[1]]
                if (king[0]>=0 and king[0]<=7 and king[1]<=7 and king[1]>=0) and not own_piece(king[0],king[1],self.color,board=self.board):
                    self.legal_moves.append(king)
        castle_move=castle()
        if piece=='♔' and white_king_moved==False:
            self.legal_moves.extend(castle_move)
        elif piece=='♚' and black_king_moved==False:
            self.legal_moves.extend(castle_move)
        return self.legal_moves
    def pawn(self):
            pawn=[self.row,self.col]
            update=1 if self.piece=='♟' else -1
            if (pawn[0]+update>=0 and pawn[0]+update<=7 and pawn[1]<=7 and pawn[1]>=0) and self.board[pawn[0]+update][pawn[1]]==None:
                self.legal_moves.append([pawn[0]+update,pawn[1]])
                if ((self.piece=='♙' and pawn[0]==6) or (self.piece=='♟' and pawn[0]==1)) and self.board[pawn[0]+(2*update)][pawn[1]]==None:
                    self.legal_moves.append([pawn[0]+(2*update),pawn[1]])
            if (pawn[1]+1<=7 and pawn[1]+1>=0 and pawn[0]+update<=7 and pawn[0]+update>=0) and self.board[pawn[0]+update][pawn[1]+1]!= None and not own_piece(pawn[0]+update,pawn[1]+1,self.color,board=self.board):
                self.legal_moves.append([pawn[0]+update,pawn[1]+1])
            if (pawn[1]-1<=7 and pawn[1]-1>=0 and pawn[0]+update<=7 and pawn[0]+update>=0) and self.board[pawn[0]+update][pawn[1]-1]!= None and not own_piece(pawn[0]+update,pawn[1]-1,self.color,board=self.board):
                self.legal_moves.append([pawn[0]+update,pawn[1]-1])
            return self.legal_moves
    def pawn_attack(self):
        pawn=[self.row,self.col]
        update=1 if self.piece=='♟' else -1
        if pawn[1]+1<=7 and pawn[1]+1>=0 and pawn[0]+update<=7 and pawn[0]+update>=0:
            self.legal_moves.append([pawn[0]+update,pawn[1]+1])
        if pawn[1]-1<=7 and pawn[1]-1>=0 and pawn[0]+update<=7 and pawn[0]+update>=0:
            self.legal_moves.append([pawn[0]+update,pawn[1]-1])
        return self.legal_moves
    def knight(self):
        if self.piece=='♘' or self.piece=='♞':
            knight_sq=[self.row,self.col]
            offset1=(-1,1)
            offset2=(-2,2)
            for row in offset1:
                for col in offset2:
                    if (knight_sq[1]+col<=7 and knight_sq[1]+col>=0 and knight_sq[0]+row>=0 and knight_sq[0]+row<=7) and (not own_piece(knight_sq[0]+row,knight_sq[1]+col,self.color,board=self.board)):
                        self.legal_moves.append([knight_sq[0]+row,knight_sq[1]+col])
            for row in offset2:
                for col in offset1:
                    if (knight_sq[1]+col<=7 and knight_sq[1]+col>=0 and knight_sq[0]+row>=0 and knight_sq[0]+row<=7) and (not own_piece(knight_sq[0]+row,knight_sq[1]+col,self.color,board=self.board)):
                        self.legal_moves.append([knight_sq[0]+row,knight_sq[1]+col])
            return self.legal_moves
    def other(self):
        up=[self.row,self.col]
        down=[self.row,self.col]
        left=[self.row,self.col]
        right=[self.row,self.col]
        top_right=[self.row,self.col]
        top_left=[self.row,self.col]
        bottom_right=[self.row,self.col]
        bottom_left=[self.row,self.col]
        pawn=[self.row,self.col]
        if self.piece not in ('♗','♝','♕','♛'):
            top_left=top_right=bottom_left=bottom_right=-1
        if self.piece not in ('♜','♖','♛','♕'):
            up=down=left=right=-1
        for _ in range(8):
            if up!=-1:
                up[0]-=1
                if up[0]==-1:
                    up=-1
                elif own_piece(up[0],up[1],self.color,board=self.board):
                    up=-1
            if down!=-1:
                down[0]+=1
                if down[0]==8:
                    down=-1
                elif own_piece(down[0],down[1],self.color,board=self.board):
                    down=-1
            if left!=-1:
                left[1]-=1
                if left[1]==-1:
                    left=-1
                elif own_piece(left[0],left[1],self.color,board=self.board):
                    left=-1
            if right!=-1:
                right[1]+=1
                if right[1]==8:
                    right=-1
                elif own_piece(right[0],right[1],self.color,board=self.board):
                    right=-1
            if top_right!=-1:
                top_right[0]-=1
                top_right[1]+=1
                if top_right[0]==-1 or top_right[1]==8 or own_piece(top_right[0],top_right[1],self.color,board=self.board):
                    top_right=-1
            if top_left!=-1:
                top_left[0]-=1
                top_left[1]-=1
                if top_left[0]==-1 or top_left[1]==-1 or own_piece(top_left[0],top_left[1],self.color,board=self.board):
                    top_left=-1
            if bottom_right!=-1:
                bottom_right[0]+=1
                bottom_right[1]+=1
                if bottom_right[0]==8 or bottom_right[1]==8 or own_piece(bottom_right[0],bottom_right[1],self.color,board=self.board):
                    bottom_right=-1
            if bottom_left!=-1:
                bottom_left[0]+=1
                bottom_left[1]-=1
                if bottom_left[0]==8 or bottom_left[1]==-1 or own_piece(bottom_left[0],bottom_left[1],self.color,board=self.board):
                    bottom_left=-1
            
            for move in (up,down,left,right,top_left,top_right,bottom_left,bottom_right):
                if move!=-1:
                    self.legal_moves.append(move.copy())

            if top_left!=-1 and self.board[top_left[0]][top_left[1]]!=None:
                top_left=-1
            if top_right!=-1 and self.board[top_right[0]][top_right[1]]!=None:
                top_right=-1
            if bottom_left!=-1 and self.board[bottom_left[0]][bottom_left[1]]!=None:
                bottom_left=-1
            if bottom_right!=-1 and self.board[bottom_right[0]][bottom_right[1]]!=None:
                bottom_right=-1

            if up!=-1 and self.board[up[0]][up[1]]!=None:
                    up=-1
            if down!=-1 and self.board[down[0]][down[1]]!=None:
                    down=-1
            if left!=-1 and self.board[left[0]][left[1]]!=None:
                    left=-1
            if right!=-1 and self.board[right[0]][right[1]]!=None:
                    right=-1
            if up==-1 and down==-1 and left==-1 and right==-1 and top_left==-1 and top_right==-1 and bottom_right==-1 and bottom_left==-1:
                return self.legal_moves
        return self.legal_moves
    def moves_legal(self):
        if self.piece=='♔' or self.piece=='♚':
            return self.king()
        elif self.piece=='♞' or self.piece=='♘':
            return self.knight()
        elif self.piece=='♟' or self.piece=='♙':
            return self.pawn()
        else:
            return self.other()

def all_attacks(piece,board):
    all_moves=[]
    if piece=='♚':
        pieces=('♖','♘','♗','♕','♗','♘','♖','♙')  #'♔'
    elif piece=='♔':
        pieces=('♟','♜','♞','♝','♛','♝','♞','♜')  #'♚'
    for check in pieces:
        position=where_piece(check,board)
        for move in position:
            moves=Highlight(move[0],move[1],check,board)
            if check=='♟' or check=='♙':
                legal_move=moves.pawn_attack()
            else:
                legal_move=moves.moves_legal()
            all_moves.extend(legal_move)
    return all_moves

def in_check(row,col,king,board):
    if [row,col] in all_attacks(king,board):
        return True
    else:
        return False

def where_piece(piece,board):
    location=[]
    for row in range(8):
        for col in range(8):
            if board[row][col]==piece:
                location.append([row,col])
    return location


def highlight(row,col,piece,board):
        moves=Highlight(row,col,piece,board)
        canvas.delete('all')
        draw_board()
        draw_piece()
        legalmoves=moves.moves_legal()
        legal_moves=[]
        for moves in legalmoves:
            if piece=='♚' or piece=='♔':
                if not in_check(moves[0],moves[1],piece,board):
                    canvas.create_text((moves[1]*size)+(size//2),(moves[0]*size)+(size//2),text='●',font=('Arial',25),fill='white')
                    legal_moves.append(moves)
            else:
                canvas.create_text((moves[1]*size)+(size//2),(moves[0]*size)+(size//2),text='●',font=('Arial',25),fill='white')
                legal_moves.append(moves)
        return legal_moves

def game_end():
    global board,white_king_position,black_king_position
    if move%2==0:
        pieces=('♖','♘','♗','♕','♗','♘','♖','♙')  #'♔'
        position=white_king_position.copy()
        king='♔'
    else:
        pieces=('♟','♜','♞','♝','♛','♝','♞','♜')  #'♚'
        position=black_king_position.copy()
        king='♚'
    for piece in pieces:
        location=where_piece(piece,board)
        for row,col in location:
            moves=Highlight(row,col,piece,board)
            legal_moves=moves.moves_legal()
            for n_row,n_col in legal_moves:
                dummy_board=[row.copy() for row in board]
                dummy_board[row][col]=None
                dummy_board[n_row][n_col]=piece
                if not in_check(position[0],position[1],king,board):
                    return
    print("Checkmate")



create_board()
draw_board()
draw_piece()





canvas.bind('<Button-1>',click)
window.mainloop()