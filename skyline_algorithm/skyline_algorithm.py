#author: YI DING
#email: dydifferent@gmail.com
#Jun 2021

import pandas as pd
import numpy as np



class skyline_query_BNL:
    '''
    Implement skyline algorithm by Block Nested loop
    '''

    def __init__(self,player_df,position):
        '''
        Parameters:
            player_df: the stats dataframe
            position: string, only accept PG, PF, SF, SG, C
        '''
        self.player_df=player_df
        self.player=None
        self.player_array=None
        self.player_num=None
        self.position=position
        self.index_stack=[]
        

    def reset_index(self):
        '''
        add 'index' column to solve that palyer's with same name
        '''
        self.player_df=self.player_df.reset_index()
        self.player_df['index']=range(len(self.player_df))


    def position_filter(self):
        '''
        group player into array by positions
        '''
        self.reset_index()
        #players paly in center
        if self.position=='C':
            self.player=self.player_df[(self.player_df['Pos']=='C')]
            self.player_array=self.player.values.tolist()
        #players play in power forward
        elif self.position=='PF':
            self.player=self.player_df[(self.player_df['Pos']=='PF')]
            self.player_array=self.player.values.tolist()
        #players play in point guard
        elif self.position=='PG':
            self.player=self.player_df[(self.player_df['Pos']=='PG')]
            self.player_array=self.player.values.tolist()
        #players play in small forward
        elif self.position=='SF':
            self.player=self.player_df[(self.player_df['Pos']=='SF')]
            self.player_array=self.player.values.tolist()
        #players play in shooting guard
        elif self.position=='SG':
            self.player=self.player_df[(self.player_df['Pos']=='SG')]
            self.player_array=self.player.values.tolist()

        self.player_num=len(self.player_array)

    
    def player_is_dominated(self):
        '''
        drop players who are dominated from the array
        '''
        self.position_filter()
        for i in range(self.player_num):
            #give an initial value to index_number
            index_number=-1
            #extract one top point as comparison object
            top_point=self.player_array[i]
            for j in range(self.player_num):      
                if j==i:
                    continue
                else:
                    check_point=self.player_array[j]
                    #judge the top_point is dominated or not 
                    if top_point[3]<check_point[3] and top_point[4]<check_point[4] and top_point[5]<check_point[5] and top_point[6]<check_point[6]:
                        index_number=top_point[0]
                    else:
                        continue
            if index_number !=-1:
                self.index_stack.append(index_number)
            else:
                continue

    
    def player_isnot_dominated(self):
        '''
        filter points cannot be dominated
        '''
        self.player_is_dominated()
        for i in self.index_stack:
            self.player=self.player.drop(self.player[self.player['index']==i].index)
        return self.player


    def player_is_dominated_test(self):
        '''
        drop players who are dominated from the array
        '''
        self.position_filter()
        for i in range(self.player_num):
            #give an initial value to index_number
            index_number=-1
            #extract one top point as comparison object
            top_point=self.player_array[i]
            for j in range(self.player_num):      
                if j==i:
                    continue
                else:
                    check_point=self.player_array[j]
                    #judge the top_point is dominated or not 
                    if top_point[3]<check_point[3] and top_point[4]<check_point[4]:
                        index_number=top_point[0]
                    else:
                        continue
            if index_number !=-1:
                self.index_stack.append(index_number)
            else:
                continue

    
    def player_isnot_dominated_test(self):
        '''
        filter points cannot be dominated
        '''
        self.player_is_dominated_test()
        for i in self.index_stack:
            self.player=self.player.drop(self.player[self.player['index']==i].index)
        return self.player

        
        
    








if __name__=='__main__':
    pass
    #read data and select columns
    stats_df_original=pd.read_csv('./NBA_2015_16_season_stats.csv')
    stats_df=stats_df_original[['Player','Pos','PTS','TRB','AST','BLK']].copy()

    #check data integratation
    print(pd.isnull(stats_df).values.any())

    #choose players with one position: 'C', 'PG', 'PF', 'SF', 'SG'
    a=skyline_query_BNL(stats_df,'PG')
    print(a.player_isnot_dominated())



    #test
    #add one test data into dataframe
    stats_test=stats_df.loc[stats_df.shape[0]+1]={'Player':'test_player','Pos':'PG','PTS':100,'TRB':100,'AST':100,'BLK':100}
    b=skyline_query_BNL(stats_df,'PG')
    print('after inserting outlier')
    print(b.player_isnot_dominated())


    #test
    #4-dimension to 2-dimension
    stats_df=stats_df_original[['Player','Pos','PTS','TRB']].copy()
    c=skyline_query_BNL(stats_df,'PG')
    print(c.player_isnot_dominated_test())
    stats_df.loc[stats_df.shape[0]+1]={'Player':'test_player','Pos':'PG','PTS':27,'TRB':6}
    d=skyline_query_BNL(stats_df,'PG')
    print(d.player_isnot_dominated_test())
