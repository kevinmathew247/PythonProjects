# COMP 517 Continuos Assessment 2
# Name : Kevin John Mathew
# Student ID : 201591357

finalDict = {}
tempDict = {}

"""
generatePreferences(values) - sorts the preferences of agent alternatives in descending order
Parameters: input - worksheet
Returns: dictionary - with keys as agent numbers and values as their preferences sorted in descending order
"""
def generatePreferences(sheet):
    for i in range(1, sheet.max_row+1):
        for j in range(1, sheet.max_column+1):
            tempDict[j] = sheet.cell(row=i, column=j).value
        sortedDict = sorted(tempDict, key=tempDict.get)
        sortedDict.reverse()
        finalDict.setdefault(i,sortedDict.copy())
        tempDict.clear()
        sortedDict.clear()
    return finalDict


"""
dictatorship(preferenceProfile, agent) - sorts the preferences of agent alternatives and returns selected agent's winner
Parameters: input - (dictionary, int)
Returns: int - returns winner of the selected agent's preference order
"""
def dictatorship(preferenceProfile, agent):
    try:
        winner = preferenceProfile[agent][0]
        print("Winner is : {}".format(winner))
        return winner
    except:
        print("Agent not found")


"""
scoringRule(preferences, scoreVector, tieBreak) - assigns scores from scoreVector to each agent alternatives
Parameters: input - (dictionary, list, Any)
Returns: int - returns the alternative with the highest total score
"""
def scoringRule(preferences, scoreVector, tieBreak):
    try:
        scoreDict = {}
        agentValues = list(preferences[1])
        if len(scoreVector) != len(agentValues):
            raise ValueError
        else:
            # sorting scoring vector values in descending order
            scoreVector.sort(reverse = True)
            for value in preferences.values():
                for index,val in enumerate(value):
                    if val in scoreDict.keys():
                        scoreDict[val] += scoreVector[index]
                    else:
                        scoreDict[val] = scoreVector[index]
            # check if there is a tie
            maxScore = max(scoreDict.values())
            maxValueKeys = []
            for key, value in scoreDict.items():
                if value == maxScore:
                    # maxValueKeys : this list contains all keys that has appeared most times in first position
                    maxValueKeys.append(key)
            if len(maxValueKeys) > 1:
                # tie occured
                return tieBreaker(preferences, tieBreak, maxValueKeys)
            else:
                winner = maxValueKeys[0]
                print("Winner is : {}".format(winner))
                return winner
    except ValueError:
        print("Incorrect input")
        return False


"""
plurality(preferences, tieBreak) - counts the number of times a key is in the first position of the preference orderings
and 1 point to every other alternative
Parameters: input - (dictionary, Any)
Returns: int - returns the alternative with most count in first place
"""
def plurality(preferences, tieBreak):
    agentValues = list(preferences[1])
    countDict = dict.fromkeys(agentValues,0)
    for key in preferences:
        firstVal = preferences[key][0]
        # countDict : dictionary with count of the values that came first in preferences
        countDict[firstVal] += 1
    maxScore = max(countDict.values())
    maxValueKeys = []
    for key, value in countDict.items():
        if value == maxScore:
            # maxValueKeys : this list contains all keys that has appeared most times in first position
            maxValueKeys.append(key)
    if len(maxValueKeys) > 1:
        # tie occured
        return tieBreaker(preferences, tieBreak, maxValueKeys)               
    else:
        # no tie occured, return maximum value
        winner = maxValueKeys[0]
        print("Winner is : {}".format(winner))
        return winner


"""
veto(preferences, tieBreak) - assigns 0 points to every agent alternative ranked last place 
and 1 point to every other alternative
Parameters: input - (dictionary, Any)
Returns: int - returns the alternative with the most number of points
"""
def veto(preferences,tieBreak):
    agentValues = list(preferences[1])
    vetoDict = dict.fromkeys(agentValues,0)
    for value in preferences.values():
            for index,val in enumerate(value):
                if index != len(agentValues)-1:
                    vetoDict[val] += 1
                else:
                    vetoDict[val] += 0
    # check if there is a tie
    maxScore = max(vetoDict.values())
    maxValueKeys = []
    for key, value in vetoDict.items():
        if value == maxScore:
            # maxValueKeys : this list contains all keys that has appeared most times in first position
            maxValueKeys.append(key)
    if len(maxValueKeys) > 1:
        # tie occured
        return tieBreaker(preferences, tieBreak, maxValueKeys)
    else:
        winner = maxValueKeys[0]
        print("Winner is : {}".format(winner))
        return winner


"""
borda(preferences, tieBreak) - assigns a score of 0 to least-preferred alternative, 
a score of 1 to the second least-preferred alternative and so on
Parameters: input - (dictionary, Any)
Returns: int - returns the alternative with the highest score
"""
def borda(preferences, tieBreak):
    agentValues = list(preferences[1])
    bordaDict = dict.fromkeys(agentValues,0)
    for value in preferences.values():
        i=1
        for index, val in enumerate(value):
            bordaDict[val] += len(agentValues)-i
            i += 1
    # check if there is a tie
    maxScore = max(bordaDict.values())
    maxValueKeys = []
    for key, value in bordaDict.items():
        if value == maxScore:
            # maxValueKeys : this list contains all keys that has appeared most times in first position
            maxValueKeys.append(key)
    if len(maxValueKeys) > 1:
        # tie occured
        return tieBreaker(preferences, tieBreak, maxValueKeys)
    else:
        winner = maxValueKeys[0]
        print("Winner is : {}".format(winner))
        return winner


"""
harmonic(preferences, tieBreak) - assigns a score of 1/m to least-preferred alternative, 
a score of 1/(m-1) to the second least-preferred alternative and so on
Parameters: input - (dictionary, Any)
Returns: int - returns the alternative with the highest score
"""
def harmonic(preferences, tieBreak):
    agentValues = list(preferences[1])
    harmonicDict = dict.fromkeys(agentValues,0)
    for value in preferences.values():
        i=len(agentValues)-1
        for index,val in enumerate(value):
            harmonicDict[val] += 1/(len(agentValues)-i)
            i -= 1
    # check if there is a tie
    maxScore = max(harmonicDict.values())
    maxValueKeys = []
    for key, value in harmonicDict.items():
        if value == maxScore:
            # maxValueKeys : this list contains all keys that has appeared most times in first position
            maxValueKeys.append(key)   
    if len(maxValueKeys) > 1:
        # tie occured
        return tieBreaker(preferences, tieBreak, maxValueKeys)
    else:
        winner = maxValueKeys[0]
        print("Winner is : {}".format(winner))
        return winner


"""
STV(preferences, tieBreak) - the alternatives that appear the least frequently in the first position 
of agents' rankings are removed in each round until final set is removed
Parameters: input - (dictionary, Any)
Returns: int - returns the last set of possible winners. Passed to tie-break if multiple values are returned
"""
def STV(preferences, tieBreak):
    while len(preferences[1]) > 1 :
        agentValues = list(preferences[1])
        countDict = dict.fromkeys(agentValues,0)
        for key in preferences:
            firstValue = preferences[key][0]
            # countDict : dictionary with count of the values that came first in preference
            countDict[firstValue] += 1
        minScore = min(countDict.values())
        minValueKeys = []
        for key, value in countDict.items():
            if value == minScore:
                # minValueKeys : this list contains all keys that has appeared least times in first position
                minValueKeys.append(key)
        # checking if all values in countDict are same            
        if len(list(set(list(countDict.values())))) == 1:
                break
        for value in preferences.values():
            i = 0
            while i < len(minValueKeys):
                # removing values which has least occured using minValueKeys list
                value.remove(minValueKeys[i])
                i += 1      
    # check if there is a tie
    if len(preferences[1]) > 1:
        # tie occured
        return tieBreaker(preferences, tieBreak, minValueKeys)
    else:
        winner = preferences[1][0]
        print("Winner is : {}".format(winner))
        return winner


"""
rangeVoting (values, tieBreak) - finds sum of each alternative column from the worksheet being given as input 
Parameters: input - (worksheet, Any)
Returns: int - return the alternative that has the maximum sum of valuations
"""
def rangeVoting (values, tieBreak):
    initialDict = generatePreferences(values)
    columnNumbers = list(range(1,values.max_column + 1))
    rangeDict = dict.fromkeys(columnNumbers,0)
    # finding sum of each alternative column
    for j in range(1, values.max_column+1):
            for i in range(1, values.max_row+1):
                cellValue = values.cell(row=i, column=j).value
                rangeDict[j] += cellValue
    maxValue = max(rangeDict.values())
    maxvalueKeys = []
    for key, value in rangeDict.items():
        if value == maxValue:
            # maxValueKeys : this list contains all keys that has appeared most times in first position
            maxvalueKeys.append(key)        
    if len(maxvalueKeys) > 1:
        # tie occured
        return tieBreaker(initialDict, tieBreak, maxvalueKeys)
    else:
        winner = maxvalueKeys[0]
        print("Winner is : {}".format(winner))
        return winner


"""
tieBreaker(preferences, tieBreak, keys) - resolves any tie-break occuring in the voting function results based on option selcted
Parameters: input - (dictionary, Any, list)
Returns: int - returns the winning alternative in case of tie between winning alternative scores
based on tie-breaking option selected
If tieBreak = "max", the maximum value from winning alternatives(keys) in returned
If tieBreak = "min", the minimum value from winning alternatives(keys) is returned
If tieBreak is an integer between 1 and n: the more preferred winning alternative for agent number selected is returned
"""
def tieBreaker(preferences, tieBreak, keys):
    try:
        agentList = list(preferences.keys())
        if(tieBreak == "max"):
            winner = max(keys)
            print("Winner is : {}".format(winner))
            return winner
        elif(tieBreak == "min"):
            winner = min(keys)
            print("Winner is : {}".format(winner))
            return winner
        elif(tieBreak in agentList):
            listSelected = preferences[tieBreak]
            for i in range(0, len(listSelected)-1):
                if listSelected[i] in keys:
                    winner = listSelected[i]
                    print("Winner is : {}".format(winner))
                    return winner
        else:
            raise Exception
    except:
        print("Invalid tie break input. The selected choice does not match with an agent")
