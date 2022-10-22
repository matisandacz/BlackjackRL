from blackjack import Action, Blackjack
from collections import defaultdict
import numpy as np
import random
from plot_utils import plot_policy

class QLearner():
	def __init__(self):
		self.gamma = 1 #discount factor
		self.alpha = 0.015 #learning rate
		self.epsilon = 0.15
		self.env = Blackjack() #blackjack game instance

	def choose_action(self, Q, state, explore):
		best_action = Action(np.argmax(Q[state]))
		if not explore:
			return best_action

		random_number = random.uniform(0,1)
		if random_number < self.epsilon:
			return random.choice(list(Action))
		else: 
			return best_action

	def update_q_table(self, Q, state, action, newState, reward):
		Q[state][action.value] += self.alpha * (reward + self.gamma * np.max(Q[newState]) - Q[state][action.value])

	def play(self, Q, episodes, train=False):

		print("-------------------------------Playing for {0} episodes-------------------------------".format(episodes))
		rewards_all_episodes = []

		for episode in range(1, episodes + 1):

			if episode%1000 == 0:
				print("Episode: {0}/{1}".format(episode, episodes))

			state = self.env.reset()
			terminated = False

			while not terminated:
				action = self.choose_action(Q, state, explore=train)
				newState, terminated, reward = self.env.step(action)
				
				if train:
					self.update_q_table(Q, state, action, newState, reward)

				state = newState

			rewards_all_episodes.append(reward)

		if train:
			self.print_rewards(rewards_all_episodes)
		else:
			self.print_statistics(rewards_all_episodes)

		policy = dict((state, np.argmax(q_value)) for state, q_value in Q.items())

		return Q, policy

	def print_rewards(self, rewards_all_episodes):
		episodes = len(rewards_all_episodes)
		reward_per_thousand_episodes = np.split(np.array(rewards_all_episodes), episodes/1000)
		count = 1000
		print("\nAvg Reward per 1000 episodes:\n")
		for r in reward_per_thousand_episodes:
			print(count, ": ", str(sum(r/1000)))
			count += 1000

	def print_statistics(self, rewards_all_episodes):
		number_of_wins = rewards_all_episodes.count(1)
		number_of_loss = rewards_all_episodes.count(-1)
		number_of_ties = rewards_all_episodes.count(0)
		episodes = len(rewards_all_episodes)
		print("\n")
		print("Win percentaje is {0}%".format((number_of_wins/episodes)*100))
		print("Loss percentaje is {0}%".format((number_of_loss/episodes)*100))
		print("Tie percentaje is {0}%".format((number_of_ties/episodes)*100))

	def draw_optimal_q_table(self, optimal_policy):
		plot_policy(optimal_policy)



train_iterations = 500000
play_iterations = 500000

zeros_q_table = defaultdict(lambda : np.zeros(2))
random_q_table = defaultdict(lambda : np.random.uniform(0,1,2))

q = QLearner()
optimal_q_table, optimal_policy = q.play(zeros_q_table, train_iterations, train=True)

q.play(optimal_q_table, play_iterations, train=False)
q.play(random_q_table, play_iterations, train=False)

q.draw_optimal_q_table(optimal_policy)

# Estaria bueno separar en train y play... Train toma Q, y play toma directamente una policy Pi.