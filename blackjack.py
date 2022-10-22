import random
from enum import Enum

class Action(Enum):
	HIT = 1
	STAND = 0

class Blackjack():

	deck = [1,2,3,4,5,6,7,8,9,10,10,10,10]

	def dealCards(self, amount):
		return [self.getCard() for card in range(amount)]

	def getCard(self):
		return random.choice(self.deck)

	def reset(self):
		self.playerCards = self.dealCards(2)
		self.casinoCards = self.dealCards(1)
		self.playerSum = self.findSum(self.playerCards)
		self.casinoSum = self.findSum(self.casinoCards)
		self.hasAce = 1 in self.playerCards
		return self.getState()

	def getState(self):
		return (self.playerSum, self.casinoSum, self.hasAce)

	def playerHit(self):
		card = self.getCard()
		self.playerCards.append(card)
		self.playerSum = self.findSum(self.playerCards)
		#print("Player Hits: {0}. Current player sum: {1}".format(card, self.playerSum))

	def playerStand(self):
		while self.casinoSum < 17: # Stands at soft 17
			card = self.getCard()
			self.casinoCards.append(card)
			self.casinoSum = self.findSum(self.casinoCards)
			#print("Casino Hits: {0}. Current casino sum: {1}".format(card, self.casinoSum))

	def step(self, action):
		if action == Action.HIT:
			self.playerHit()
		else:
			self.playerStand()
		terminated, reward = self.endStep(action)
		return (self.getState(), terminated, reward)

	def busted(self, currentSum):
		return currentSum > 21

	def calculateReward(self):
		if self.playerSum > self.casinoSum:
			return 1
		elif self.playerSum == self.casinoSum:
			return 0
		else:
			return -1

	# Returns a tuple (terminated, reward)
	def endStep(self, action): 
		if action == Action.HIT:
			if self.playerSum > 21:
				return (True, -1)
			return (False, 0)
		
		if self.casinoSum > 21:
			return (True, 1)
		return (True, self.calculateReward())

	def selectAction(self):
		if self.playerSum <= 11:
			return Action.HIT
		if self.playerSum == 21:
			return Action.STAND
		else:
			return random.choice(list(Action))

	def hasUsableAce(self, cards):
		return 1 in cards and sum(cards) + 10 <= 21

	def findSum(self, cards):
		if self.hasUsableAce(cards):
			return sum(cards) + 10
		return sum(cards)

	def playEpisode(self, episode):

		print ("-------------------------------{0}-------------------------------".format(episode))

		self.reset()

		done = False
		episodes = 0

		while not done:
			episodes += 1
			action = self.selectAction()
			print("P_SUM: {0} C_SUM: {1} ACE: {2} ACTION: {3}".format(self.playerSum, self.casinoSum, self.hasAce, action))
			state, done, reward = self.step(action)
			if done:
				print("Game ended after {0} episodes. Result was {1}".format(episodes, reward))
				return reward

	def runSimulation(self, episodes):
		win = 0
		loss = 0
		tie = 0
		for iteration in range(episodes):
			reward = self.playEpisode(iteration)
			if reward == 1:
				win += 1
			elif reward == -1:
				loss += 1
			else:
				tie += 1
		print("-------------------------------STATISTICS-------------------------------")
		print("Win percentaje is {0}%".format((win/episodes)*100))
		print("Loss percentaje is {0}%".format((loss/episodes)*100))
		print("Tie percentaje is {0}%".format((tie/episodes)*100))


#blackjack = Blackjack()
#print(blackjack.dealCards(3))
#blackjack.runSimulation(5000)