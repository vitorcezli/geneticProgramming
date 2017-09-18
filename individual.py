#!/usr/bin/python3
from abc import ABC, abstractmethod


class individual(ABC):
	"The representation for a genetic programming individual"

	def __init__(self, size):
		"Initializes the tree with its genotype"
		self.genotype = generate_genotype(size)

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