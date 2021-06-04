from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *
from nested import *

ASC_1ibaraki  = Beta('ASC_1ibaraki', 0     , -100, 100, 1,'1ibaraki cte.') 
ASC_2tokyo    = Beta('ASC_2tokyo'  ,0.5342 , -100, 100, 0,'2tokyo cte.')  
ASC_3hachi    = Beta('ASC_3hachi'  , 2.652 , -100, 100, 0,'3hachi cte.')
ASC_4rail     = Beta('ASC_4rail'   ,-3.677 , -100, 100, 0,'4rail cte.') 
ASC_5seikan   = Beta('ASC_5seikan' ,0.4521 , -100, 100, 0,'5seikan cte.') 
B_TIME        = Beta('B_TIME'      ,-2     , -100, 100, 0,'Travel time')
B_COST        = Beta('B_COST'      ,-2     , -100, 100, 0,'Travel cost')
D_1weight     = Beta('D_1weight'   , 0.4128, -100, 100, 0,'Weight 1')
D_2weight     = Beta('D_2weight'   , 0.0756, -100, 100, 0,'Weight 2')
D_3weight     = Beta('D_3weight'   ,-0.8467, -100, 100, 0,'Weight 3')
D_4weight     = Beta('D_4weight'   , 0.6351, -100, 100, 0,'Weight 4')
D_5weight     = Beta('D_5weight'   , 0     , -100, 100, 1,'Weight 5')

S_TIME        = Beta('S_TIME'      , 0.8,    0,  10, 0)
ES_TIME       = S_TIME * bioDraws('ES_TIME')
S_COST        = Beta('S_COST'      , 0.8,    0,  10, 0)
ES_COST       = S_COST * bioDraws('ES_COST')

n_time_1ibaraki = DefineVariable('time_1ibaraki_neg', time_1ibaraki * -1 )
n_time_2tokyo   = DefineVariable('time_2tokyo_neg'  , time_2tokyo   * -1 )
n_time_3hachi   = DefineVariable('time_3hachi_neg'  , time_3hachi   * -1 )
n_time_4rail    = DefineVariable('time_4rail_neg'   , time_4rail    * -1 )
n_time_5seikan  = DefineVariable('time_5seikan_neg' , time_5seikan  * -1 )
n_cost_1ibaraki = DefineVariable('cost_1ibaraki_neg', cost_1ibaraki * -1 )
n_cost_2tokyo   = DefineVariable('cost_2tokyo_neg'  , cost_2tokyo   * -1 )
n_cost_3hachi   = DefineVariable('cost_3hachi_neg'  , cost_3hachi   * -1 )
n_cost_4rail    = DefineVariable('cost_4rail_neg'   , cost_4rail    * -1 )
n_cost_5seikan  = DefineVariable('cost_5seikan_neg' , cost_5seikan  * -1 )

V1 = ASC_1ibaraki  + exp(B_TIME + ES_TIME) * n_time_1ibaraki  + exp(B_COST + ES_COST) * n_cost_1ibaraki + D_1weight * weight_log10
V2 = ASC_2tokyo    + exp(B_TIME + ES_TIME) * n_time_2tokyo    + exp(B_COST + ES_COST) * n_cost_2tokyo   + D_2weight * weight_log10
V3 = ASC_3hachi    + exp(B_TIME + ES_TIME) * n_time_3hachi    + exp(B_COST + ES_COST) * n_cost_3hachi   + D_3weight * weight_log10
V4 = ASC_4rail     + exp(B_TIME + ES_TIME) * n_time_4rail     + exp(B_COST + ES_COST) * n_cost_4rail    + D_4weight * weight_log10
V5 = ASC_5seikan   + exp(B_TIME + ES_TIME) * n_time_5seikan   + exp(B_COST + ES_COST) * n_cost_5seikan  + D_5weight * weight_log10

V = {1: V1, 2: V2, 3: V3, 4: V4, 5: V5 }
av ={1: 1,  2: 1,  3: 1,  4: 1,  5: 1  }

logprob = bioLogit(V,av,mode)
l = mixedloglikelihood(logprob)

rowIterator('obsIter')
BIOGEME_OBJECT.ESTIMATE = Sum(l, 'obsIter')

nullLoglikelihood(av,'obsIter')
choiceSet = [1,2,3,4,5]
cteLoglikelihood(choiceSet,mode,'obsIter')
availabilityStatistics(av,'obsIter')

BIOGEME_OBJECT.PARAMETERS['NbrOfDraws'] = "300"
BIOGEME_OBJECT.PARAMETERS['RandomDistribution'] = "HALTON"
BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = "BIO"
BIOGEME_OBJECT.DRAWS = {  'ES_TIME':'NORMAL',
                          'ES_COST':'NORMAL' }

BIOGEME_OBJECT.FORMULAS['1ibaraki utility'] = V1
BIOGEME_OBJECT.FORMULAS['2tokyo   utility'] = V2
BIOGEME_OBJECT.FORMULAS['3hachi   utility'] = V3
BIOGEME_OBJECT.FORMULAS['4rail    utility'] = V4
BIOGEME_OBJECT.FORMULAS['5seikan  utility'] = V5
