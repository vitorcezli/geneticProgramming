#!/usr/bin/python3
from individual import individual
import numbers
import math


class individualKeijzer7(individual):
	"The representation for a genetic programming individual"

	def __init__(self, size):
		"Initializes the tree with its genotype"
		self.genotype = self.generate_genotype(size)

	def generate_genotype(self, size):
		"Generates the individual's genotype"
		return ['sum', ['log', 10, 'XX'], 3]


	def get_datum_with_values(self, values):
		"gets the datum with the values"
		


	def classify(self, values):
		"Classifies the data based on the genotype"
		# gets the datum with the values
		datum_and_values = self.get_datum_with_values(values)

		# returns the same number if there isn't a function
		if isinstance(datum_and_values, numbers.Number):
			return datum_and_values

		# classifies for log function
		elif datum_and_values[0] == 'log':
			base = self.classify(datum_and_values[1])
			exponent = self.classify(datum_and_values[2])
			return math.log(exponent, base)

		# classifies for sum function
		elif datum_and_values[0] == 'sum':
			factor1 = self.classify(datum_and_values[1])
			factor2 = self.classify(datum_and_values[2])
			return factor1 + factor2

		# an error has happened
		else:
			print("An error occurred on genotype format: %s" % 
				(str(datum_and_values)))
			exit()
		

	def mutate(self):
		"Mutates the individual"
		pass

	def cross(self, other_individual):
		"Returns a new individual using crossover operation"
		pass


individual = individualKeijzer7(7)
print(individual.classify(['sum', ['log', 10, 100], 3]))