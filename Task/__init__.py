from otree.api import *
import numpy.random as rnd  
import random 
import pandas as pd 

doc = """
Your app description
"""


class C(BaseConstants): #app’s parameters and constants that do not vary from player to player.
    NAME_IN_URL = 'Task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 38
    NUM_PROUNDS = 3
    
    # Images 
    carbon      = "global/figures/carbon/carbon_"
    price        = "global/figures/price/price_"

    ##OLD CODE 
    lAttrID     = ['p','s']
    lAttrNames  = ['Price','Sustainability']
    #product = ['nuts','sweets','muesli']
    # Template vars
    lColNames   = ['Product A','Product B']


    # In between round messages
    BetweenTrialMessages = {
        "1": f"Now you will have {NUM_PROUNDS} practice rounds.", 
        str(int(NUM_PROUNDS+1)): "The practice rounds are over."
        }


    # Confidence page ##Probably not going to use confidence ratings 
    #iLikertConf     = 7
    #sConfQuestion   = f"From 1 to {iLikertConf}, how confident are you on your choice?"
    #sLeftConf       = "Very unsure"
    #sRightConf      = "Very sure"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer): #Here we fill out our data model (table) for our players 
    # DVs
    sChoice     = models.StringField()
    dRT_dec     = models.FloatField()
    iConfidence = models.IntegerField()
    dRT_conf    = models.FloatField()

    # 
    P1=models.IntegerField()
    P2=models.IntegerField()
    S1=models.IntegerField()
    S2=models.IntegerField()

    # Attention variables
    sNames      = models.LongStringField(blank=True) 
    sDT         = models.LongStringField(blank=True)

    # # Timestamps
    sStartDec   = models.StringField()
    sEndDec     = models.StringField()
    sStartCross = models.StringField()
    sEndCross   = models.StringField()
    #sStartConf = models.StringField() 
    #sEndConf   = models.StringField()


    # Others 
    sBetweenBtn = models.StringField() #Assuming this means seconds between button
    lRoundOrder = models.StringField()  # To store the randomized round order
 

def creating_session(subsession):
    # Load Session variables
    s = subsession.session #making s variable to improve readability  
    if subsession.round_number == 1: #if practice 
        for player in subsession.get_players():
            p = player.participant #setting treatment on participant not player 
            ### Randomizing order of attributes
            lPos = C.lAttrID[:]         # Create hard copy of attributes (price and sustainability)
            #random.shuffle(lPos)        # Shuffle order
            p.lPos = lPos               # Store it as a participant variable
            #### Select trial for payment (from the first round after practice rounds to the last)
            p.iSelectedTrial = random.randint(C.NUM_PROUNDS+1,C.NUM_ROUNDS)
           
           #randomizing assignment to one of the three conditions 
            if s.config['treatment']=='random':
                p.sTreatment = random.choice(['price_prime','sustainability_prime','control'])
                print(f"Treatment assigned randomly: {p.sTreatment}")  # Print the randomly assigned treatment
            else:
                p.sTreatment = s.config['treatment']
                print(f"Treatment assigned from config: {p.sTreatment}")  # Print the treatment from config

            # Randomize the order of rounds
            lRoundOrder = list(range(1, C.NUM_ROUNDS + 1))
            random.shuffle(lRoundOrder)
            p.lRoundOrder = ','.join(map(str, lRoundOrder))
            print(f"Round order for participant {p.id_in_session}: {p.lRoundOrder}")

        #fix values 
    lValuesMap = { 
        #nuts
    1: [1, 0, 1, 2], 2: [2, 0, 1, 2], 3: [0,3,2,1], 4: [4, 0, 1, 2],
    5: [0,1,3,2], 6: [0,2,3,2], 7: [3, 0, 2, 3], 8: [4, 0, 2, 3],
    9: [0,1,3,1], 10: [0,2,3,1], 11: [3, 0, 1, 3], 12: [4, 0, 1, 3],
        #sweets
    13: [5,6,5,4], 14: [7, 5, 4, 5], 15: [5,8,5,4], 16: [9, 5, 4, 5],
    17: [5,6,6,5], 18: [7, 5, 5, 6], 19: [5,8,6,5], 20: [9, 5, 5, 6],
    21: [5,6,6,4], 22: [7, 5, 4, 6], 23: [5,8,6,4], 24: [9, 5, 4, 6],
        #muesli
    25: [10,11,8,7], 26: [10,12,8,7], 27: [10,13,8,7], 28: [10,14,8,7],
    29: [11, 10, 8, 9], 30: [10,12,9,8], 31: [13, 10, 8, 9], 32: [10,14,9,8],
    33: [10,11,9,7], 34: [12, 10, 7, 9], 35: [10,12,9,7], 36: [10,14,9,7],
    37: [1,0,3,1], 38: [10, 11, 7, 9]
}

    for player in subsession.get_players():
        p = player.participant
        player.sBetweenBtn = random.choice(['left', 'right']) #Randomly assign 'left' or 'right' to sBetweenBtn
        current_round = subsession.round_number
        lRoundOrder = list(map(int, p.lRoundOrder.split(',')))
        randomized_round = lRoundOrder[current_round - 1]

        if player.round_number <= C.NUM_PROUNDS: 
            # Practice Trials
            print(player.round_number, "practice")  
            if player.round_number == 1:
                lValues = [4,0, 1,2] #Preset values for round 1 
            elif player.round_number == 2:
                lValues = [4,0, 1,2] #Preset values for round 2 
            elif player.round_number == 3:
                lValues = [4,0, 1,2] #Preset values for round 3 
        else:
            print(player.round_number, "normal") #normal rounds randomized 
            if randomized_round in lValuesMap:
                lValues = lValuesMap[randomized_round]
                print(f"Round {current_round} (Randomized to {randomized_round}): {lValues}") 
            else: lValues = [1,1,1,1] # Default in case of missing key

        player.P1,player.P2, player.S1,player.S2 = lValues
    
def attributeList(lValues,lPos,treatment):
    lAttributes = []
    lOrder = []

    for i in range(len(C.lAttrID)): #where lAttrID = ['p','s']
        id                  = C.lAttrID[i]      
        name                = C.lAttrNames[i]
        #productname        = C.product[i]  
        # Store the order of the list
        lOrder.append(lPos.index(id))
        lPaths = [] #Creates an empty list lPaths to store image paths.
        for v in lValues[i]:
            if id=="s":  #iterates through carbon label folders 
                 lPaths.append(f"{C.carbon}{v}.png") #carbon label folder
            else:
                lPaths.append(f"{C.price}{v}.png") #prices folder


        # Create object with all the relevant variables
        Attr = {
            'id'        : id,
            'name'      : name,
            'lValues'   : lPaths,
            #'productname' : productname
        }
        lAttributes.append(Attr)
    
    lFinal = [ lAttributes[x] for x in lOrder]
    return lFinal



# PAGES
class Decision(Page):
    form_model      = 'player'
    form_fields     = [ 'sChoice']
    form_fields     = [ 'sStartDec','sEndDec', 'dRT_dec', 'sNames', 'sDT' , 'sChoice'] #'dTime2first'
    
    @staticmethod
    def vars_for_template(player: Player): # vars_for_template passes variables to the template so you can access them there
        # Order of attributes (from participant var)
        p = player.participant
        lPos = p.lPos
        treatment=p.sTreatment
      
        lValues = [[player.P1,player.P2],[player.S1,player.S2]]
        print(lValues)
        return dict(
            lAttr = attributeList(lValues,lPos,treatment), #treatment
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p = player.participant
        
        if player.round_number == p.iSelectedTrial: 
            p.bChoseA = player.iChooseB == '0'   
            print(f"Decision in selected trial recorded: {p.bChoseA}")

class FixCross(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]
    template_name = 'global/FixCross.html'


class SideButton(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]
    template_name = 'global/SideButton.html'

    @staticmethod
    def js_vars(player: Player): #js_vars is used to pass data to JavaScript code in the template
        
        return dict(
            sPosition = player.sBetweenBtn
        )


class Confidence(Page):
    form_model      = 'player'
    form_fields     = [ 'sStartConf','sEndConf', 'dRT_conf','iConfidence']
    template_name   = 'global/Confidence.html'
    
    @staticmethod
    def vars_for_template(player: Player):
        p = player.participant
        return dict(
            lScale = list(range(1,C.iLikertConf+1))
        )

class Message(Page):
    template_name = 'global/Message.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_PROUNDS
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            MessageText = 'The practice rounds ended. <br> The experiment will start now.'
        )

page_sequence = [SideButton, Decision, Message]
#page_sequence = [SideButton, Decision, Confidence]

 