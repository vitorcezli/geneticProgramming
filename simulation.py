#!/usr/bin/python3
from __future__ import division
from individualKeijzer7 import individualKeijzer7
import numpy
import random
import math


class simulation:
	"This class implements the simulation operation"

	def __init__(self, data_train, data_test, individuals):
		# initializes datasets
		self.train = numpy.loadtxt(open(data_train, "rb"), delimiter=",", skiprows=0)
		self.test = numpy.loadtxt(open(data_test, "rb"), delimiter=",", skiprows=0)
		
		# initializes population
		self.population = []
		for individual in individuals:
			self.population.append([individual, self.fitness(individual)])


	def execute_epoch(self, prob_cross, tour_size, mutation, n_elitism):
		"Executes an epoch"
		min_fitness = min([j[len(self.population[0]) - 1] for j in self.population])
		max_fitness = max([j[len(self.population[0]) - 1] for j in self.population])
		mean_fitness = sum([j[len(self.population[0]) - 1] for j in self.population]) / \
			len(self.population)

		print("%f,%f,%f" % (min_fitness, mean_fitness, max_fitness))

		number_same_individuals = 0
		better_than_fathers = 0
		worse_than_fathers = 0

		sons = self.generate_sons(self.population, tour_size, \
			mutation, len(self.population) * prob_cross)

		sons += self.select_elitism(self.population, n_elitism)
		sons += self.select_individuals(self.population, \
			len(self.population) - len(sons))
		self.population = sons


	def generate_sons(self, individuals, tour_size, mutation, number_sons):
		"Generates two new sons"
		sons = []
		while len(sons) < number_sons:
			# gets the first father
			selected = self.select_individuals(individuals, tour_size)
			father1 = self.select_from_tournament(selected)

			# gets the second father
			selected = selected = self.select_individuals(individuals, tour_size)
			father2 = self.select_from_tournament(selected)

			# generates new sons
			sons += self.create_sons_from_fathers(father1[0], father2[0], mutation)
		return sons


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


	def select_individuals(self, individuals, number):
		"Selects the passed number of individuals"
		if number >= len(individuals):
			return individuals
		else:
			selection = []
			selection.append(individuals[random.randint(0, len(individuals) - 1)])
			return selection


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
		difference = [self.train[i][len(self.train[0]) - 1] - \
			individual.classify(self.train[i][0 : len(self.train[0]) - 1]) \
			for i in range(len(self.train))]
		difference_square = [math.pow(dif, 2) for dif in difference]
		rmse = math.sqrt(sum(difference_square) / len(difference_square))
		size_normalization = math.log1p(4 + individual.get_size() / 10)
		return rmse / size_normalization


	def calculate_final_difference(self, individual):
		"Calculates the difference on the test set"
		difference = [self.test[i][len(self.test[0]) - 1] - \
			individual.classify(self.test[i][0 : len(self.test[0]) - 1]) \
			for i in range(len(self.test))]
		difference_square = [math.pow(dif, 2) for dif in difference]
		return math.sqrt(sum(difference_square) / len(difference_square))



population = [individualKeijzer7() for i in range(100)]
test = simulation('keijzer-7-train.csv', 'keijzer-7-test.csv', population)

for i in range(200):
	test.execute_epoch(0.5, 7, 0.01, 10)