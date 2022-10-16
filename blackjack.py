import random

class Blackjack():

	def playEpisode(self, episode):

		print ("-------------------------------{0}-------------------------------".format(episode))

		self.playerCards = [random.randint(1, 10), random.randint(1, 10)]
		self.casinoCards = [random.randint(1, 10)]
		self.playerSum = self.findSum(self.playerCards)
		self.casinoSum = self.findSum(self.casinoCards)
		self.hasAce = 1 in self.playerCards

		done = False
		episodes = 0

		while not done:
			episodes += 1
			action = self.selectAction()
			print("P_SUM: {0} C_SUM: {1} ACE: {2} ACTION: {3}".format(self.playerSum, self.casinoSum, self.hasAce, action))
			done, reward = self.step(action)
			if done:
				print("Game ended after {0} episodes. Result was {1}".format(episodes, reward))
				return reward

	def step(self, action):
		if action == 0:
			card = random.randint(1, 10)
			self.playerCards.append(card)
			self.playerSum = self.findSum(self.playerCards)
			print("Player HITS and gets {0} NEW SUM {1}".format(card, self.playerSum))
			return self.gameEnd(0)
		done = False
		reward = 0
		while not done:
			card = random.randint(1, 10)
			self.casinoCards.append(card)
			self.casinoSum = self.findSum(self.casinoCards)
			print("Player STANDS. Casino gets {0} and now SUMS {1}".format(card, self.casinoSum))
			done, reward = self.gameEnd(1)
		return (done, reward)

	def gameEnd(self, action):
		if action == 0:
			if self.playerSum > 21:
				return (True, -1)
			return (False, 0)
		if self.casinoSum > 21:
			return (True, 1)
		elif self.casinoSum >= 18: #Forced to stand at 18
			if self.casinoSum == self.playerSum: #Tie
				return (True, 0) 
			elif self.casinoSum > self.playerSum:
				return (True, -1)
			else:
				return (True, 1)
		else:
			return (False, 0)

	def selectAction(self):
		if self.playerSum <= 11:
			return 0
		if self.playerSum == 21:
			return 1
		else:
			return random.randint(0,1)

	def findSum(self, cards):
		totalSum = sum(cards)

		if 1 not in cards:
			return totalSum

		boostedSum = totalSum + 10

		if boostedSum <= 21:
			return boostedSum
		return totalSum

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


blackjack = Blackjack()
blackjack.runSimulation(5000)