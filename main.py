#Dalton Wright
#A Very Large Rat
#08/04/24
import random
import math
import time
from rat import Rat
GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what


def initial_population():
  '''Create the initial set of rats based on constants'''
  rats = [[],[]]
  mother = Rat("F", INITIAL_MIN_WT)
  father = Rat("M", INITIAL_MAX_WT)
  for r in range(NUM_RATS):
    if r < 10:
      sex = "M"
      ind = 0
    else:
      sex = "F"
      ind = 1
  
    wt = calculate_weight(sex, mother, father)
    R = Rat(sex, wt)
    rats[ind].append(R)
  return rats


def calculate_weight(sex, mother, father):
  '''Generate the weight of a single rat'''
  if mother.weight < father.weight:
    min = mother.getWeight()
    max = father.getWeight()
  else:
    min = father.getWeight()
    max = mother.getWeight()
  # Use the triangular function from the random library to skew the 
  #baby's weight based on its sex
  if sex == "M":
    wt = int(random.triangular(min, max, max))
  else:
    wt = int(random.triangular(min, max, min))
  
  return wt


def mutate(pups):
  '''Check for mutability, modify weight of affected pups'''
  
  for contents in pups:
    for r in contents:
      if random.random() <= MUTATE_ODDS:
        x = random.uniform(MUTATE_MIN, MUTATE_MAX)
        weight = math.ceil(r.getWeight() * x)
        r.setWeight(weight)

  
  return pups


def breed(rats):
  """Create mating pairs, create LITTER_SIZE children per pair"""
  children = [[],[]]
  random.shuffle(rats[0])
  random.shuffle(rats[1])
  
  for i in range(len(rats[0])):
    mother = rats[1][i]
    father = rats[0][i]

    mother.setLitters()
    father.setLitters()

    for p in range(LITTER_SIZE):

      sex = random.choice(['M','F'])
      if sex =="M":
          ind = 0
      else:
        ind = 1

      wt = calculate_weight(sex, mother, father)
      R = Rat(sex, wt)
      children[ind].append(R)
  return children  


def select(rats, pups ):
  '''Choose the largest viable rats for the next round of breeding'''
  large = [[],[]]
  largestR =[[],[]]
  rats[0].extend(pups[0])
  rats[1].extend(pups[1])
 
  rats[0].sort(reverse = True)
  rats[1].sort(reverse = True)
  if rats[0][0] > rats[1][0]:
    largestR[0].append(rats[0][0].getSex())
    largestR[1].append(rats[0][0].getWeight())
  else:
    largestR[0].append(rats[1][0].getSex())
    largestR[1].append(rats[1][0].getWeight())

  for male in rats[0]:
    if male.canBreed() and len(large[0]) < 10:
      large[0].append(male)
  
  for female in rats[1]:
    if female.canBreed() and len(large[1]) < 10:
      large[1].append(female)
    
  

  return large, largestR


def calculate_mean(rats):
  '''Calculate the mean weight of a population'''
  sumWt=0
  numRats = 0
  for content in rats:
    
    for i in content:
      a = i.getWeight()
      sumWt+=a
      numRats+=1

  return sumWt // numRats


def fitness(rats):
  """Determine if the target average matches the current population's average"""
  mean = calculate_mean(rats)
  if mean >= GOAL:
    return mean >= GOAL, mean


def main():
  start = time.time()
  mean = []
  rats = initial_population()
  goal = False
  gen = 0 
  while not goal and gen <= GENERATION_LIMIT:
    
    gen += 1
    
    '''FYI as long as we track generations, we can just do a division at the end to find number of years'''

    '''Just use fit instead of goal...'''
    fit = fitness(rats)
    if fit:
      goal = True
    else:    
      pups = breed(rats)
      pups = mutate(pups)
      '''just use rats here instead of selected'''
      rats, lr = select(rats, pups)

    mean.append(calculate_mean(rats))

    
    # :)
    # Fixed select: no females being selected - typo
    # Fixed breed: 80 babies generated
    # Removed/commented print statements
    # Please review notes to help fix your redundancies
    # Finalize & generate report :)


  end = time.time()

  if not goal:
    print("Uh oh, you reached the generation limit")
  else:

    print("~~~~~~~~~~RESULTS~~~~~~~~~~\n\n\n")
    print("Final Population Mean:", mean[-1], "grams\n\n")
    print("Generations:", len(mean))
    print("Experiment Duration:",int(len(mean)/10),"years")
    print("simulation Duration:",round(end-start,4),"seconds\n\n")
    print("~The Largest Rat~")
    gender = (" ".join(lr[0]))
   
    print(f"({gender}) - {lr[1]}g \n\n")
    print("Generation Weight Averages (grams)")
    for i in mean:
      print(i,"\t", end=" ")

    
if __name__=="__main__":
  main()