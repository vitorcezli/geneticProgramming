#!/usr/bin/python3
from individual import individual
import numbers
import math


class individualKeijzer7(individual):
	"The representation for a genetic programming individual"

	def __init__(size):
		"Initializes the tree with its genotype"
		self.genotype = generate_genotype(size)

	def generate_genotype(size):
		"Generates the individual's genotype"
		pass

	def classify(datum):
		"Classifies the data based on the genotype"
		# returns the same number if there isn't a function
		if isinstance(datum, numbers.Number):
			return datum

		# classifies for log function
		elif datum[0] == 'log':
			base_value = classify(datum[1])
			exponent_value = classify(datum[2])
			return math.log(exponent_value, base_value)

		# classifies for sum function
		elif datum[0] == 'sum':
			factor1 = classify(datum[1])
			factor2 = classify(datum[2])
			return factor1 + factor2

		# an error has happened
		else:
			print("An error occurred on genotype format: %s" % (str(datum)))
			exit()
		

	def mutate():
		"Mutates the individual"
		pass

	def cross(other_individual):
		"Returns a new individual using crossover operation"
		pass