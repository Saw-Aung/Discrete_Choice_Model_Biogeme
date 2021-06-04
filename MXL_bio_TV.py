from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *
from nested import *

ASC_1ibaraki  = Beta('ASC_1ibaraki', 0    , -100, 100, 1,'1ibaraki cte.') 
ASC_2tokyo    = Beta('ASC_2tokyo'  ,0.5342, -100, 100, 0,'2tokyo cte.')  
ASC_3hachi    = Beta('ASC_3hachi'  , 2.652, -100, 100, 0,'3hachi cte.')
ASC_4rail     = Beta('ASC_4rail'   ,-3.677, -100, 100, 0,'4rail cte.') 
ASC_5seikan   = Beta('ASC_5seikan' ,0.4521, -100, 100, 0,'5seikan cte.') 
B_TIME        = Beta('B_TIME'      ,-0.01726, -100, 100, 0,'Travel time')
B_COST        = Beta('B_COST'      ,-0.01694, -100, 100, 0,'Travel cost')
D_1weight     = Beta('D_1weight'   , 0.4128 , -100, 100, 0,'Weight 1')
D_2weight     = Beta('D_2weight'   , 0.07561, -100, 100, 0,'Weight 2')
D_3weight     = Beta('D_3weight'   ,-0.8467 , -100, 100, 0,'Weight 3')
D_4weight     = Beta('D_4weight'   , 0.6351 , -100, 100, 0,'Weight 4')
D_5weight     = Beta('D_5weight'   , 0    , -100, 100, 1,'Weight 5')

S_time        = Beta('S_time'      , 0.1,   0,  10, 0)
ES_time       = S_time * bioDraws('ES_time')

V1 = ASC_1ibaraki + (B_TIME+ES_time)*time_1ibaraki + B_COST*cost_1ibaraki + D_1weight*weight_log10
V2 = ASC_2tokyo   + (B_TIME+ES_time)*time_2tokyo   + B_COST*cost_2tokyo   + D_2weight*weight_log10
V3 = ASC_3hachi   + (B_TIME+ES_time)*time_3hachi   + B_COST*cost_3hachi   + D_3weight*weight_log10
V4 = ASC_4rail    + (B_TIME+ES_time)*time_4rail    + B_COST*cost_4rail    + D_4weight*weight_log10
V5 = ASC_5seikan  + (B_TIME+ES_time)*time_5seikan  + B_COST*cost_5seikan  + D_5weight*weight_log10

V = {1: V1, 2: V2, 3: V3, 4: V4, 5: V5 }

av = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1 }

logprob = bioLogit(V,av,mode)
l = mixedloglikelihood(logprob)

rowIterator('obsIter')
BIOGEME_OBJECT.ESTIMATE = Sum(l, 'obsIter')

nullLoglikelihood(av,'obsIter')
choiceSet = [1,2,3,4,5]
cteLoglikelihood(choiceSet,mode,'obsIter')
availabilityStatistics(av,'obsIter')

BIOGEME_OBJECT.PARAMETERS['NbrOfDraws'] = "200"
BIOGEME_OBJECT.PARAMETERS['RandomDistribution'] = "HALTON"
BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = "BIO"
BIOGEME_OBJECT.DRAWS = {  'ES_time':'NORMAL'}

BIOGEME_OBJECT.FORMULAS['1ibaraki utility'] = V1
BIOGEME_OBJECT.FORMULAS['2tokyo   utility'] = V2
BIOGEME_OBJECT.FORMULAS['3hachi   utility'] = V3
BIOGEME_OBJECT.FORMULAS['4rail    utility'] = V4
BIOGEME_OBJECT.FORMULAS['5seikan  utility'] = V5
