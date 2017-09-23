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
			print(self.fitness(individual))


	def execute_epoch(self):
		min_fitness = math.inf
		max_fitness = -math.inf
		mean_fitness = 0
		number_same_individuals = 0
		better_than_fathers = 0
		worse_than_fathers = 0


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