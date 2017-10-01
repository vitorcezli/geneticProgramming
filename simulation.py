#!/usr/bin/python3
from __future__ import division
from individualKeijzer7 import individualKeijzer7
from individualKeijzer10 import individualKeijzer10
from house import house
import numpy
import random
import math
import matplotlib.pyplot as plt


class simulation:
	"This class implements the simulation operation"

	def __init__(self, data_train, data_test, individuals):
		# initializes the training set
		self.train = numpy.loadtxt(open(data_train, "rb"), delimiter=",", skiprows=0)
		numpy.random.shuffle(self.train)

		# 30% of training data will be used for cross-validation
		self.cross = self.train[: int(len(self.train) * 0.3)]
		self.train = self.train[int(len(self.train) * 0.3 + 1) :]

		# initializes the test set
		self.test = numpy.loadtxt(open(data_test, "rb"), delimiter=",", skiprows=0)
		
		# initializes population
		self.population = []
		self.fitness_set = self.return_subset(30)
		for individual in individuals:
			self.population.append([individual, self.fitness(individual)])

		# initializes the matrix to plot
		self.plot_matrix = []


	def run_simulation(self, epoch, prob_cross, tour_size, mutation, n_elitism):
		"Runs the genetic algorithm simulation"
		while epoch > 0:
			self.execute_epoch(prob_cross, tour_size, mutation, n_elitism)
			epoch -= 1


	def return_subset(self, number):
		"Defines the examples that will be used on fitness calculation"
		return [self.train[random.randint(0, len(self.train) - 1)] \
			for i in range(number)]


	def plot_fitness(self):
		"Plots the found values for fitness, individuals and error on cross-set"
		epoch_array = [i + 1 for i in range(len(self.plot_matrix))]
		plt.plot(epoch_array, self.get_column(self.plot_matrix, 0), color = 'b')
		plt.plot(epoch_array, self.get_column(self.plot_matrix, 1), color = 'g')
		plt.plot(epoch_array, self.get_column(self.plot_matrix, 2), color = 'r')
		plt.show()


	def plot_better_worse(self):
		"Plots the number of individuals that are better/worse than their fathers"
		epoch_array = [i + 1 for i in range(len(self.plot_matrix))]
		plt.plot(epoch_array, self.get_column(self.plot_matrix, 3), color = 'b')
		plt.plot(epoch_array, self.get_column(self.plot_matrix, 4), color = 'r')
		plt.show()


	def plot_same(self):
		"Plots the number of repeated individuals in a generation"
		epoch_array = [i + 1 for i in range(len(self.plot_matrix))]
		plt.plot(epoch_array, self.get_column(self.plot_matrix, 5), color = 'b')
		plt.show()


	def plot_train_cross(self):
		"Plots the best individual's fitness on the training and cross-validation set"
		epoch_array = [i + 1 for i in range(len(self.plot_matrix))]
		plt.plot(epoch_array, self.get_column(self.plot_matrix, 0), color = 'b')
		plt.plot(epoch_array, self.get_column(self.plot_matrix, 6), color = 'g')
		plt.show()


	def get_column(self, matrix, column):
		"Returns the column of a matrix as an array"
		return [i[column] for i in matrix]


	def get_final_error(self):
		"Calculates the error on the test set"
		best_individual = self.select_elitism(self.population, 1)
		return self.error_on_set(best_individual[0][0], self.test)	


	def execute_epoch(self, prob_cross, tour_size, mutation, n_elitism):
		"Executes an epoch"
		# generates new sons
		[sons, better, worse] = self.generate_sons(self.population, tour_size, \
			mutation, len(self.population))

		# adds the sons using the probability of crossover for the next population
		new_generation = self.select_individuals(sons, \
			int(len(self.population) * prob_cross))

		new_generation += self.select_elitism(self.population, n_elitism)
		new_generation += self.select_individuals(self.population, \
			len(self.population) - len(new_generation))
		self.population = new_generation

		# calculates the fitness after the epoch
		min_fitness = min([j[len(self.population[0]) - 1] for j in self.population])
		max_fitness = max([j[len(self.population[0]) - 1] for j in self.population])
		mean_fitness = sum([j[len(self.population[0]) - 1] \
			for j in self.population]) / len(self.population)

		# calculates the error on cross-validation set
		best_individual = self.select_elitism(self.population, 1)
		error_cross = self.error_on_set(best_individual[0][0], self.cross)

		# prints the values found in this epoch
		print("%f,%f,%f,%d,%d,%d,%f" % (min_fitness, mean_fitness, \
			max_fitness, better, worse,\
			self.number_same_individuals(self.population), 
			error_cross))
		self.plot_matrix.append([min_fitness, mean_fitness, \
			max_fitness, better, worse,\
			self.number_same_individuals(self.population), 
			error_cross]
		)

		# redefine the fitness
		self.fitness_set = self.return_subset(30)


	def get_cross_error(self):
		"Return the last cross-set error"
		return self.plot_matrix[len(self.plot_matrix) - 1]\
			[len(self.plot_matrix[0]) - 1]


	def number_same_individuals(self, population):
		"Returns the number of same individuals"
		# variables that will be used to count
		individuals = [str(individual[0]) for individual in population]
		dictIndividual = {}
		same = 0

		# puts each time the individual appears on the dictionary
		for individual in individuals:
			if individual in dictIndividual:
				dictIndividual[individual] += 1
			else:
				dictIndividual[individual] = 1

		# gets the number of repeated individuals
		for individual, count in dictIndividual.items():
			if count > 1:
				same += count
		return same


	def generate_sons(self, individuals, tour_size, mutation, number_sons):
		"Generates two new sons"
		sons = []
		better = 0
		worse = 0

		while len(sons) < number_sons:
			# gets the first father
			selected = self.select_individuals(individuals, tour_size)
			father1 = self.select_from_tournament(selected)

			# gets the second father
			selected = selected = self.select_individuals(individuals, tour_size)
			father2 = self.select_from_tournament(selected)

			# generates new sons
			newsons = self.create_sons_from_fathers(father1[0], father2[0], mutation)
			sons += newsons

			for son in newsons:
				if self.compare_with_fathers(son, father1, father2) == 1:
					better += 1
				elif self.compare_with_fathers(son, father1, father2) == -1:
					worse += 1
		return [sons, better, worse]


	def create_sons_from_fathers(self, father1, father2, mutation):
		"Creates new individuals"
		individual1 = father1.cross(father2)
		individual2 = father2.cross(father1)

		# apply mutation if possible
		if random.random() < mutation:
			individual1.mutate()
		if random.random() < mutation:
			individual2.mutate()
		return [[individual1, self.fitness(individual1)], \
			[individual2, self.fitness(individual2)]]


	def compare_with_fathers(self, son, father1, father2):
		"Returns if the son is better or worse than its fathers"
		if son[1] > father1[1] and son[1] > father2[1]:
			return 1
		elif son[1] == father1[1] and son[1] == father2[1]:
			return 0
		else:
			return -1


	def select_individuals(self, individuals, number):
		"Selects individuals based on their fitness"
		if number >= len(individuals):
			return individuals
		else:
			random.shuffle(individuals)
			return individuals[0 : number]


	def select_elitism(self, individuals, number):
		"Selects the best individuals"
		if number >= len(individuals):
			return individuals
		individuals_sorted = sorted(individuals, key = lambda x: x[1])
		return individuals_sorted[0 : number]


	def select_from_tournament(self, individuals):
		"Selects individual from tournament"
		individuals_sorted = sorted(individuals, key = lambda x: x[1])
		return individuals_sorted[0]


	def fitness(self, individual):
		"Calculates the fitness of an individual given the trainset"
		# calculates the difference
		difference = [self.fitness_set[i][len(self.fitness_set[0]) - 1] - \
			individual.classify(self.fitness_set[i][0 : len(self.fitness_set[0]) - 1]) \
			for i in range(len(self.fitness_set))]
		difference_square = [math.pow(dif, 2) for dif in difference]
		rmse = math.sqrt(sum(difference_square) / len(difference_square))

		# the difference calculated is normalized by the tree size
		size_normalization = math.log1p(4 + individual.get_size() / 10)
		return rmse / size_normalization


	def error_on_set(self, individual, dataset):
		"Calculates the difference on the specified set"
		difference = [dataset[i][len(dataset[0]) - 1] - \
			individual.classify(dataset[i][0 : len(dataset[0]) - 1]) \
			for i in range(len(dataset))]
		difference_square = [math.pow(dif, 2) for dif in difference]
		return math.sqrt(sum(difference_square) / len(difference_square))


cross_error = []
times = 30

test = None
for time in range(times):
	population = [individualKeijzer7() for i in range(200)]
	test = simulation('keijzer-7-train.csv', 'keijzer-7-test.csv', population)
	test.run_simulation(25, 0.5, 2, 1, 10)
	cross_error.append(test.get_cross_error())
	print("Simulation %d done" % (time + 1))

print("Cross-validation error %f" % (sum(cross_error) / len(cross_error)))
print("Test error: %f" % (test.get_final_error()))


# test one try
#population = [individualKeijzer7() for i in range(200)]
#test = simulation('keijzer-7-train.csv', 'keijzer-7-test.csv', population)
#test.run_simulation(25, 0.9, 2, 1, 10)
#print(test.get_final_error())
#test.plot_fitness()
#test.plot_better_worse()
#test.plot_same()
#test.plot_train_cross()