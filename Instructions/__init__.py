from otree.api import *
import random
import pandas as pd
from collections import Counter
from numpy import random as rnd
import numpy as np
doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL         = 'Intro'
    PLAYERS_PER_GROUP   = None
    NUM_ROUNDS          = 1
    # Setup/Experiment variables 
    iPracticeRounds     = 3
    iOptions            = 38 #27 options? = trial
    # iNumTrials          = 5
    iNumTrials          = iPracticeRounds + 3*iOptions
    # Template variables
    AvgDur              = '15'
    iBonus              = '1.5 euros'
    ## Symbols directory 
    UvA_logo         = 'global/figures/UvA_logo.png'
    path1               = 'global/figures/example1.png'
    path2               = 'global/figures/example2.png'
    pathGif             = 'global/figures/demoMouseCrop.gif'
    pathData            = '_static/global/files/Data4Exp.csv'
    imgCandidate        = "global/figures/candidate.png"
    imgNumbers          = "global/figures/numbers/n_"
    imgStars          = "global/figures/stars/star_"
    imgLeafs        ="global/figures/leafs/leaf_"
    imgNegatives    ="global/figures/negatives/neg-eco-"
    OneTreePlanted      = "global/figures/Logo_OneTreePlanted.png"
    star_symbol                = "global/figures/one_star.png"
    leaf_symbol                = "global/figures/one_leaf.png"
    neg_symbol             = "global/figures/one-neg.png"
    revealed_pos       = "global/figures/revealed_task_pos.png"
    revealed_neg        = "global/figures/revealed_task_neg.png"
    circled_task_pos        = "global/figures/circled_task_pos.png"
    circled_task_neg        = "global/figures/circled_task_neg.png"
    TreatPos          = "global/figures/TreatPos.gif"
    TreatNeg          = "global/figures/TreatNeg.gif"
    one_leaf            ="global/figures/leafs/leaf_1.png"
    two_leaf            ="global/figures/leafs/leaf_2.png"
    three_leaf          ="global/figures/leafs/leaf_3.png"
    one_neg             ="global/figures/negatives/neg-eco-1.png"
    two_neg             ="global/figures/negatives/neg-eco-2.png"
    three_neg           ="global/figures/negatives/neg-eco-3.png"

    example_control = "global/figures/example_control.GIF"
    carbon_green       = "global/figures/carbon/carbon_1.png"
    carbon_red      = "global/figures/carbon/carbon_3.png"
    circled_task = "global/figures/circled.png"

    carbon_muesli_green = "global/figures/carbon_muesli_green.png"
    carbon_muesli_yellow = "global/figures/carbon_muesli_yellow.png"
    carbon_muesli_red = "global/figures/carbon_muesli_red.png"
    muesli_price_0 = "global/figures/muesli_price_0.png"
    muesli_price_1 = "global/figures/muesli_price_1.png"
    muesli_price_2 = "global/figures/muesli_price_2.png"
    muesli_price_3 = "global/figures/muesli_price_3.png"
    muesli_price_4 = "global/figures/muesli_price_4.png"

    carbon_nuts_green = "global/figures/carbon_nuts_green.png"
    carbon_nuts_yellow = "global/figures/carbon_nuts_yellow.png"
    carbon_nuts_red = "global/figures/carbon_nuts_red.png"
    nuts_price_0 = "global/figures/nuts_price_0.png"
    nuts_price_1 = "global/figures/nuts_price_1.png"
    nuts_price_2 = "global/figures/nuts_price_2.png"
    nuts_price_3 = "global/figures/nuts_price_3.png"
    nuts_price_4 = "global/figures/nuts_price_4.png"

    carbon_sweets_green = "global/figures/carbon_sweets_green.png"
    carbon_sweets_yellow = "global/figures/carbon_sweets_yellow.png"
    carbon_sweets_red = "global/figures/carbon_sweets_red.png"
    sweets_price_0 = "global/figures/sweets_price_0.png"
    sweets_price_1 = "global/figures/sweets_price_1.png"
    sweets_price_2 = "global/figures/sweets_price_2.png"
    sweets_price_3 = "global/figures/sweets_price_3.png"
    sweets_price_4 = "global/figures/sweets_price_4.png"

    # Links 
    # You might want to have different links, for when they submit different answers
    sLinkReturn         = "https://app.prolific.com/submissions/complete?cc=XXXXX"
    sLinkReturnCal      = "https://app.prolific.com/submissions/complete?cc=YYYYY"
    sLinkOtherBrowser   = "https://YOUR-EXPERIMENT.herokuapp.com/room/room1"
    SubmitLink          = 'https://app.prolific.com/submissions/complete?cc=ZZZZZ'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass
    sTreesLocation = models.StringField() 

# FUNCTIONS
    #Here we randomize the treatments 
def creating_session(subsession):
    # Load Session variables
    s = subsession.session 
    if subsession.round_number == 1:
        for player in subsession.get_players():
            # Store any treatment variables or things that stay constant across rounds/apps
            p = player.participant
            # When creating the session, you can define whether you have a random treatment or a specific one. 
            if s.config['treatment']=='random':
                p.sTreatment = random.choice(['price_prime','sustainability_prime','control'])
            else:
                p.sTreatment = s.config['treatment']
            # Randomly selected trial
            p.iSelectedTrial = random.randint(C.iPracticeRounds,C.iNumTrials)
            ## LOAD HERE YOUR DATABASE 



# PAGES


class Instructions(Page):
    form_model = 'player'

    @staticmethod
    def js_vars(player: Player):
        ## Variables necessary for javascript
        p = player.participant
        return dict(
            lSolutions = [
                'a','c', '3', str(C.iPracticeRounds) # Solutions to control questions
            ]
        )
    
    @staticmethod
    #Here we define variables that will be called in the html file. This one is used to define slide 4 of the instructions with the correct png. examples
    def vars_for_template(player: Player):
        p = player.participant
        return dict(  
            control =  p.sTreatment =="control"

        )


page_sequence = [Instructions]
