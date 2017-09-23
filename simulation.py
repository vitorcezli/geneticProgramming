#!/usr/bin/python3
from individualKeijzer7 import individualKeijzer7
import numpy
import math


class simulation:
	"This class implements the simulation operation"

	def __init__(self, data_train, data_test):
		self.train = numpy.loadtxt(open(data_train, "rb"), delimiter=",", skiprows=0)
		self.test = numpy.loadtxt(open(data_test, "rb"), delimiter=",", skiprows=0)


	def calculate_fitness(self, individual):
		"Calculates the fitness of an individual given the trainset"
		difference = [self.train[i][len(self.train[0]) - 1] - \
			individual.classify(self.train[i][0 : len(self.train[0]) - 1]) \
			for i in range(len(self.train))]
		difference_square = [math.pow(dif, 2) for dif in difference]
		return math.sqrt(sum(difference_square) / len(difference_square))


	def calculate_final_difference(self, individual):
		"Calculates the difference on the test set"
		difference = [self.test[i][len(self.test[0]) - 1] - \
			individual.classify(self.test[i][0 : len(self.test[0]) - 1]) \
			for i in range(len(self.test))]
		difference_square = [math.pow(dif, 2) for dif in difference]
		return math.sqrt(sum(difference_square) / len(difference_square))




test = simulation('keijzer-7-train.csv', 'keijzer-7-test.csv')
ind = individualKeijzer7()
print(ind.get_genotype())
print(ind.classify([0]))
print(test.calculate_fitness(ind))