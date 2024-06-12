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
    NUM_ROUNDS = 41 #I changed this to 38
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
    iLikertConf     = 7
    sConfQuestion   = f"From 1 to {iLikertConf}, how confident are you on your choice?"
    sLeftConf       = "Very unsure"
    sRightConf      = "Very sure"


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
    sStartConf = models.StringField() #i dont think I need these 
    sEndConf   = models.StringField()


    # Others 
    sBetweenBtn = models.StringField() #Assuming this means seconds between button
 
 #To assign participants to different treatment groups, you use creating_session


def creating_session(subsession):
    # Load Session variables
    s = subsession.session #making s variable to improve readability  
    if subsession.round_number == 1: #if practice 
        for player in subsession.get_players():
            p = player.participant #setting treatment on participant not player 
            #### Randomizing order of attributes
            lPos = C.lAttrID[:]         # Create hard copy of attributes (price and sustainability)
            random.shuffle(lPos)        # Shuffle order
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


    for player in subsession.get_players(): #for loop that iterates over each player in the list
        p = player.participant
        player.sBetweenBtn = random.choice(['left','right']) #Randomly assign 'left' or 'right' to sBetweenBtn
        if player.round_number <= C.NUM_PROUNDS: 
            # Practice Trials
            print(player.round_number, "practice")  
            if player.round_number == 1:
                lValues = [1,0, 1,2] #Preset values for round 1 
            elif player.round_number == 2:
                lValues = [3,0, 1,2] #Preset values for round 2 
            elif player.round_number == 3:
                lValues = [11,10,8,9] #Preset values for round 3 
    
        else:
            # Normal Trials
            print(player.round_number, "normal")
            if player.round_number == 4:
                lValues = [1,0, 1,2] #Preset values for round 1 
            elif player.round_number == 5:
                lValues = [2,0, 1,2] #Preset values for round 2 
            elif player.round_number == 6:
                lValues = [3,0, 1,2] #Preset values for round 3 
            elif player.round_number == 7:
                lValues = [4,0, 1,2] #Preset values for round 4 
            elif player.round_number == 8:
                lValues = [1,0, 2,3] #Preset values for round 5 
            elif player.round_number == 9:
                lValues = [2,0, 2,3] #Preset values for round 6 
            elif player.round_number == 10:
                lValues = [3,0, 2,3] #Preset values for round 7
            elif player.round_number == 11:
                lValues = [4,0, 2,3] #Preset values for round 8 
            elif player.round_number == 12:
                lValues = [1,0, 1,3] #Preset values for round 9 
            elif player.round_number == 13:
                lValues = [2,0, 1,3] #Preset values for round 10 
            elif player.round_number == 14:
                lValues = [3,0, 1,3] #Preset values for round 11 
            elif player.round_number == 15:
                lValues = [4,0, 1,3] #Preset values for round 12
            elif player.round_number == 16:
                lValues = [6,5, 4,5] #Preset values for round 13
            elif player.round_number == 17:
                lValues = [7,5, 4,5] #Preset values for round 14
            elif player.round_number == 18:
                lValues = [8,5, 4,5] #Preset values for round 15
            elif player.round_number == 19:
                lValues = [9,5, 4,5] #Preset values for round 16 
            elif player.round_number == 20:
                lValues = [6,5, 5,6] #Preset values for round 17
            elif player.round_number == 21:
                lValues = [7,5, 5,6] #Preset values for round 18
            elif player.round_number == 22:
                lValues = [8,5, 5,6] #Preset values for round 19
            elif player.round_number == 23:
                lValues = [9,5, 5,6] #Preset values for round 20
            elif player.round_number == 24:
                lValues = [6,5, 4,6] #Preset values for round 21
            elif player.round_number == 25:
                lValues = [7,5, 4,6] #Preset values for round 22
            elif player.round_number == 26:
                lValues = [8,5, 4,6] #Preset values for round 23
            elif player.round_number == 27:
                lValues = [9,5, 4,6] #Preset values for round 24
            elif player.round_number == 28:
                lValues = [11,10, 7,8] #Preset values for round 25
            elif player.round_number == 29:
                lValues = [12,10, 7,8] #Preset values for round 26
            elif player.round_number == 30:
                lValues = [13,10, 7,8] #Preset values for round 27
            elif player.round_number == 31:
                lValues = [14,10, 7,8] #Preset values for round 28
            elif player.round_number == 32:
                lValues = [11,10, 8,9] #Preset values for round 29
            elif player.round_number == 33:
                lValues = [12,10, 8,9] #Preset values for round 30
            elif player.round_number == 34:
                lValues = [13,10, 8,9] #Preset values for round 31
            elif player.round_number == 35:
                lValues = [14,10, 8,9] #Preset values for round 32 
            elif player.round_number == 36:
                lValues = [11,10, 7,9] #Preset values for round 33
            elif player.round_number == 37:
                lValues = [12,10, 7,9] #Preset values for round 34
            elif player.round_number == 38:
                lValues = [13,10, 7,9] #Preset values for round 35
            elif player.round_number == 39:
                lValues = [14,10, 7,9] #Preset values for round 36
            elif player.round_number == 40:
                lValues = [0,1, 1,3] #Preset values for round 37
            elif player.round_number == 41:
                lValues = [10,10, 7,9] #Preset values for round 38
            #lValues = [1,1, 1,1] # lValues= p.database[int(player.round_number-4)]
            print(lValues)
        player.P1,player.P2, player.S1,player.S2 = lValues #assigns lValues to the corresponding attributes of the player object.
        #if 1 <= player.round_number <= 12:
        #    product = ['nuts']
        #elif 13 <= player.round_number <= 24:
        #    product = ['sweets']
        #else:
        #    product = ['muesli']

        #player.S1,player.S2,player.P2,player.P2 = lValues

def attributeList(lValues,lPos,treatment):
    lAttributes = []
    lOrder = []

    for i in range(len(C.lAttrID)): #where lAttrID = ['p','s']
        id                  = C.lAttrID[i]      
        name                = C.lAttrNames[i]
        #productname             = C.product[i]  
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
    # form_fields     = [ 'sStartDec','sEndDec', 'dRT_dec', 'sNames', 'sDT' , 'dTime2first', 'sChoice']
    
    @staticmethod
    def vars_for_template(player: Player): # vars_for_template passes variables to the template so you can access them there
        # Order of attributes (from participant var)
        p = player.participant
        lPos = p.lPos
        treatment=p.sTreatment

        # Candidates values          
      
        lValues = [[player.P1,player.P2],[player.S1,player.S2]]
        print(lValues)
        return dict(
            lAttr = attributeList(lValues,lPos,treatment), #treatment
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p = player.participant
        
        if player.round_number == p.iSelectedTrial: 
            p.bChoseA = player.iChooseB == 0   
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



page_sequence = [SideButton, Decision, Confidence]

 