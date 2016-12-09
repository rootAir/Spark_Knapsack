# --------------------------------------------
# Test the Approximate Knapsack function test
# --------------------------------------------

# Pull in the knapsack library.

from knapsack import knapsack

from pyspark.sql import SparkSession
import random

# Create the SparkContext.
sc = SparkSession \
    .builder \
    .appName("Knapsack Approximation Algorithm Test") \
    .getOrCreate()

# Knapsack problem size.
N = 10

# Setup sample data for knapsack.
knapsackData = [('item_' + str(k), random.uniform(1.0, 10.0), random.uniform(1.0, 10.0)) for k in range(N)]

# Make a Dataframe with item(s), weight(s), and value(s) for the knapsack.
knapsackData = sc.createDataFrame(knapsackData, ['item', 'weights', 'values'])

# Display the original data
print "Original Data:"
print knapsackData.take(N)
print "\n"

# Create a random maximum weight
W = random.uniform(N * 0.3, N * 0.6)

# Show the weight.
print "W: "
print W
print "\n"

# Call the knapsack greedy approximation function, with data and size 5.
knapTotals = []
k = knapsack.knapsackApprox(sc, knapsackData, W, knapTotals)

# Show the results Dataframe.
print "Selected Elements:"
print k.take(N)
print "\n"

# Show totals for selected elements of knapsack.
print "Totals:"
print knapTotals
print "\n"

# ------------------------------------------
# End of Approximate Knapsack function test
# ------------------------------------------
