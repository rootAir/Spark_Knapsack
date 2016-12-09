'''
Copyright 2016 Darrell Ulm

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
'''

# Knapsack 0-1 function weights, values and size n.
from pyspark.sql.functions import lit
from pyspark.sql.functions import col
from pyspark.sql.functions import sum
from pyspark.sql import SparkSession

def knapsackApprox(knapsackDF, W, knapTotals):
    """
    Greedy implementation of 0-1 Knapsack algorithm.

    Parameters
    ----------
    knapsackDF : Spark Dataframe with knapsack data
        sqlContext.createDataFrame(knapsackData, ['item', 'weights', 'values'])

    W : float
        Total weight allowed for knapsack.

    knapTotals : list
        List of result totals of knapsack values and weights.

    Returns
    -------
    Dataframe
        Dataframe with results.
    """

    # Add ratio of values / weights column.
    ratioDF = (knapsackDF.withColumn("ratio", lit(knapsackDF.values / knapsackDF.weights))
               .filter(col("weights") <= W)
               .sort(col("ratio").desc())
               )

    # Get the current Spark Session.
    sc = SparkSession.builder.getOrCreate()

    # Calculate the partial sums of the ratios.
    ratioDF.registerTempTable("tempTable")
    partialSumWeightsDF = sc.sql("""
        SELECT
            item,
            weights,
            values,
            ratio,
            sum(weights) OVER (ORDER BY ratio desc) as partSumWeights
        FROM
        tempTable
        """)

    # Get the max number of items, greedy less than or equal to W in Spark.
    partialSumWeightsFilteredDF = partialSumWeightsDF.sort(col("ratio").desc()).filter(col("partSumWeights") <= W)

    knapTotals.append(['Values', partialSumWeightsFilteredDF.select(sum("values")).head()[0]])
    knapTotals.append(['Weights', partialSumWeightsFilteredDF.select(sum("weights")).head()[0]])
    knapTotals.append(['Count', partialSumWeightsFilteredDF.count()])

    # Return the elements.
    return partialSumWeightsFilteredDF
    # End of knapsack function
