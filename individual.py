#!/usr/bin/python3
from abc import ABC, abstractmethod


class individual(ABC):
	"The representation for a genetic programming individual"

	def __init__(self, size, number_arguments):
		"Initializes the tree with its genotype"
		self.genotype = self.generate_genotype(size)
		self.number_arguments = number_arguments

	def get_number_arguments(self):
		"Gets the number of arguments necessary"
		return self.number_arguments

	def get_genotype(self):
		"Returns the individual's genotype"
		return self.genotype

	@abstractmethod
	def generate_genotype(self, size):
		"Generates the individual's genotype"
		pass

	@abstractmethod
	def classify(self, data):
		"Classifies the data based on the genotype"
		pass

	@abstractmethod
	def mutate(self):
		"Mutates the individual"
		pass

	@abstractmethod
	def cross(self, other_individual):
		"Returns a new individual using crossover operation"
		pass