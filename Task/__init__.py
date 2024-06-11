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
    NUM_ROUNDS = 38 #I changed this to 38
    NUM_PROUNDS = 3
    # List of attributes (id)
    #products = ['nuts','sweets','muesli']
    #carbon_label = ['red','green','yellow']
    #price_premiums = [0.15, 0.20, 0.25, 0.30]
    #base_prices = {
       # 'nuts'  : 2.89,
      #  'sweets': 1.86,
     #   'muesli': 2.49}
    #conditions = ['price_prime', 'sustainability_prime', 'control']

    ##OLD CODE 
    lAttrID     = ['p','s']
    lAttrNames  = ['Price','Sustainability']
    # Template vars
    lColNames   = ['Product A','Product B']


    # In between round messages
    BetweenTrialMessages = {
        "1": f"Now you will have {NUM_PROUNDS} practice rounds.", 
        str(int(NUM_PROUNDS+1)): "The practice rounds are over."
        }
    
    # Images 
    imgCandidate    = "global/figures/candidate.png" #delete these images in the end
    imgNumbers      = "global/figures/numbers/n_"
    imgStars        = "global/figures/stars/star_"
    imgLeafs        ="global/figures/leafs/leaf_"
    imgNegatives    ="global/figures/negatives/neg-eco-"

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
    #Q1=models.IntegerField()
    #Q2=models.IntegerField()


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
                lValues = [1,1, 1,1] #Preset values for round 1 
            elif player.round_number == 2:
                lValues = [1,1, 1,3] #Preset values for round 2 
            elif player.round_number == 3:
                lValues = [3,1, 1,1] #Preset values for round 3 
    
        else:
            # Normal Trials
            print(player.round_number, "normal")
            lValues = [1,1, 1,1] # lValues= p.database[int(player.round_number-4)]
            print(lValues)
        player.P1,player.P2, player.S1,player.S2 = lValues #assigns  lValues to the corresponding attributes of the player object.
        #player.S1,player.S2,player.P2,player.P2 = lValues

def attributeList(lValues,lPos,treatment): # treatment
    lAttributes = []
    lOrder = []

    for i in range(len(C.lAttrID)): #where lAttrID = ['p','s']
        id                  = C.lAttrID[i]      
        name                = C.lAttrNames[i]  
        # Store the order of the list
        lOrder.append(lPos.index(id))
        lPaths = [] #Creates an empty list lPaths to store image paths.
        for v in lValues[i]:
            if id=="q":  #iterates through folders 
                 lPaths.append(f"{C.imgStars}{v}.png") #quality folder
            elif id=="s" and treatment == "Positive":
                lPaths.append(f"{C.imgLeafs}{v}.png") #positive treatment
            elif id=="s" and treatment == "Negative":
                lPaths.append(f"{C.imgNegatives}{v}.png") #negative treatment
            else:
                lPaths.append(f"{C.imgNumbers}{v}.png") #prices 


        # Create object with all the relevant variables
        Attr = {
            'id'        : id,
            'name'      : name,
            'lValues'   : lPaths,
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
      
        lValues = [[player.P1,player.P2],[player.S1,player.S2],[player.Q1,player.Q2]]
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

 