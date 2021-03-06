'''
Created on May 9, 2011

@author: Chris Boesch
'''
import unittest
#from google.appengine.ext import db
import logging

#import urllib
#import datetime
#from google.appengine.api import urlfetch
#from google.appengine.api import memcache

class TicTacToe():
    name = 'TicTacToe'
    def get_name(self):
        return self.name

    @staticmethod
    def get_new_board():
        return {'board':'***\n***\n***'}

    @staticmethod
    def is_board_valid(board):
        countX = board.count('X')
        countO = board.count('O')
        countS = board.count('*')
        if len(board) != 11:
            return {'valid': False,
                    'message': 'Board does not have 11 characters.',
                    'board':board}
        if board[3] != '\n' or board[7] != '\n':
            return {'valid': False,
                    'message': 'Board does not have 2 carriage returns.',
                    'board':board}
        if countX != countO and countX != countO + 1:
            return {'valid': False,
                    'message': 'Board does not correct # of O and X.',
                    'board':board}
        if countX + countO + countS != 9:
            return {'valid': False,
                    'message': 'Invalid characters. Only X,O,* allowed.',
                    'board':board}
        return {'valid': True,
              'message': 'Valid board.',
              'board':board}

    @staticmethod
    def game_status(board):
        result = TicTacToe.is_board_valid(board)
        if result['valid'] == False:
            return {'error': result['message']}

        turn = 'X'
        if board.count('X') > board.count('O'):
            turn = 'O'

        status = 'PLAYING'  # 'PLAYING', 'X WON', 'O WON', 'TIE', 'ERROR'

        #Check for O winner
        if board[0] == board[1] == board[2] == 'O' or \
           board[4] == board[5] == board[6] == 'O' or \
           board[8] == board[9] == board[10] == 'O'or \
           board[0] == board[4] == board[8] == 'O' or \
           board[1] == board[5] == board[9] == 'O' or \
           board[2] == board[6] == board[10] == 'O'or \
           board[0] == board[5] == board[10] == 'O' or \
           board[8] == board[5] == board[2] == 'O':
            status = 'O WON'
        #Check for X winner
        if board[0] == board[1] == board[2] == 'X' or \
           board[4] == board[5] == board[6] == 'X' or \
           board[8] == board[9] == board[10] == 'X'or \
           board[0] == board[4] == board[8] == 'X' or \
           board[1] == board[5] == board[9] == 'X' or \
           board[2] == board[6] == board[10] == 'X'or \
           board[0] == board[5] == board[10] == 'X' or \
           board[8] == board[5] == board[2] == 'X':
            status = 'X WON'

        if board.count('X') == 5 and board.count('O') == 4 \
                                 and status == 'PLAYING':
            status = 'TIE'
        eval = 0.0
        message = ''
        result = {'turn': turn, 
                'eval': eval,
                'status': status,
                'message': message}
        return result
    
    @staticmethod
    def is_move_valid(start, move):
        startStatus = TicTacToe.game_status(start)
        moveStatus = TicTacToe.game_status(move)
        if startStatus.has_key('error'): return {'valid':False, 'message':'Error with start. '+startStatus['error']}
        if moveStatus.has_key('error'): return {'valid':False, 'message':'Error with move. '+moveStatus['error']}
    
        changes = 0
        for i in range(11):
            if start[i] != move[i]: changes += 1
    
        if changes==0: return {'valid':False, 'message':'No move made'}
        if changes>1: return {'valid':False, 'message':'More than one move made'}
    
        if startStatus['turn']==moveStatus['turn']: {'valid':False, 'message':'No turn change.'}
      
        return {'valid':True,
              'start':start,
              'move':move}
    
    def move_calculation(self,board,turn):
        return board.replace('*',turn,1)
      
    #Default behavior to to return the next open space filled by the current players piece
    def get_next_move(self,board):
        statusResult = TicTacToe.game_status(board)
        if statusResult.has_key('error'): return statusResult
        if statusResult['status']!='PLAYING':  {'error':'Status was not PLAYING.'+str(statusResult)}
        if board.find('*')==-1: {'error':'No empty spaces.'+str(statusResult)}
      
        #move = board.replace('*',statusResult['turn'],1)
        move = self.move_calculation(board,turn=statusResult['turn'])
        
        #Check the move
        result = TicTacToe.is_move_valid(board, move)
        if not result['valid']: {'error':'Produced move was invalid.'} 
        
        return {'move':move,
                'start':board}
    
    @staticmethod      
    def head_to_head(playerX, playerO, referee,log=False):
        player = {'X':playerX, 'O': playerO}
        board = referee.get_new_board()['board']
        moves = []
        for i in range(9):
            if log==True: print board + '\n'
            turn = referee.game_status(board)['turn']
            move = player[turn].get_next_move(board)['move']
            moves.append(move)
            status = referee.game_status(move)
            #self.assertEqual(True, referee.is_move_valid(board, move)['valid'])
            if status['status']!='PLAYING':
              #print '\n'+status['status']
              return status['status']
            board = move
        return 'Nothing returned'

class BottomUpTicTacToe(TicTacToe):
  name = "BottomUpTicTacToe"
  def move_calculation(self,board,turn):
    index = board.rfind('*')
    return board[:index]+turn+board[index+1:]

      
class CenterGrabTicTacToe(TicTacToe):
  name = "CenterGrabTicTacToe"
  def move_calculation(self,board,turn):
    if board[5]=='*': 
      return board[:5]+turn+board[6:]
    else:
      return board.replace('*',turn,1)

    
class RandomTicTacToe(TicTacToe):
  name = "RandomTicTacToe"
  def move_calculation(self,board,turn):
    indexes = []
    for i in range(11):
      if board[i]=='*': indexes.append(i)
    from random import choice
    index = choice(indexes)
    return board[:index]+turn+board[index+1:]


class CenterGrabRandomTicTacToe(TicTacToe):
  name = 'CenterGrabRandomTicTacToe'
  def move_calculation(self,board,turn):
    if board[5]=='*': 
      return board[:5]+turn+board[6:]
    indexes = []
    for i in range(11):
      if board[i]=='*': indexes.append(i)
    from random import choice
    index = choice(indexes)
    return board[:index]+turn+board[index+1:]

class HunterTicTacToe(TicTacToe):
  name = 'Hunter'
  def move_calculation(self,board,turn):
    if board[5]=='*': 
      return board[:5]+turn+board[6:]
    index = board.rfind('*')
    if board[0]==board[1]!='*' and board[2]=='*': index=2
    elif board[4]==board[5]!='*' and board[6]=='*': index=6
    elif board[8]==board[9]!='*' and board[10]=='*': index = 10
    elif board[0]==board[4]!='*' and board[8]=='*': index = 8
    elif board[1]==board[5]!='*' and board[9]=='*': index = 9
    elif board[2]==board[6]!='*' and board[10]=='*': index = 10
    elif board[0]==board[5]!='*' and board[10]=='*': index = 10
    elif board[8]==board[5]!='*' and board[2]=='*': index = 2
    
    elif board[0]==board[2]!='*' and board[1]=='*': index=1
    elif board[4]==board[6]!='*' and board[5]=='*': index=5
    elif board[8]==board[10]!='*' and board[9]=='*': index = 9
    elif board[0]==board[8]!='*' and board[4]=='*': index = 4
    elif board[1]==board[9]!='*' and board[5]=='*': index = 5
    elif board[2]==board[10]!='*' and board[6]=='*': index = 6
    elif board[0]==board[10]!='*' and board[5]=='*': index = 5
    elif board[8]==board[2]!='*' and board[5]=='*': index = 5
    
    elif board[1]==board[2]!='*' and board[0]=='*': index=0
    elif board[5]==board[6]!='*' and board[4]=='*': index=4
    elif board[9]==board[10]!='*' and board[8]=='*': index = 8
    elif board[4]==board[8]!='*' and board[0]=='*': index = 0
    elif board[5]==board[9]!='*' and board[1]=='*': index = 1 
    elif board[6]==board[10]!='*' and board[2]=='*': index = 2
    elif board[5]==board[10]!='*' and board[0]=='*': index = 0
    elif board[5]==board[2]!='*' and board[8]=='*': index = 8
    return board[:index]+turn+board[index+1:]
    
