import sys
sys.path.append("./helpers/")
import json
import helper
import postgre
from pyspark import SparkContext

class BatchProcessor:
	"""
	class that reads data from S3 bucket, prcoesses it with Spark
	and saves the results into PostgreSQL database
	"""
	def __init__(self, s3_configfile, psql_configfile):
		"""
		class constructor that initializes the instance according to the configurations of the S3 bucket, raw data and PostgreSQL table
		:type s3_configfile:     str  path to S3 config file
		:type psql_configfile:   str  path tp psql config file
		"""
		self.s3_config   = helper.parse_config(s3_configfile)
		self.psql_config = helper.parse_config(psql_configfile)
		self.sc = SparkContext()
		self.sc.setLogLevel("ERROR")


	def read_from_s3(self):
		"""
		reads files from s3 bucket defined by s3_configfile and creates Spark DataFrame
		"""
		yelp_business_filename = "s3a://{}/{}/{}".format(self.s3_config["BUCKET1"], self.s3_config["FOLDER2"], self.s3_config["RAW_DATA_FILE1"])
		yelp_rating_filename = "s3a://{}/{}/{}".format(self.s3_config["BUCKET2"], self.s3_config["FOLDER2"], self.s3_config["RAW_DATA_FILE2"])
		sanitory_inspection_filename = "s3a://{}/{}/{}".format(self.s3_config["BUCKET3"], self.s3_config["FOLDER3"], self.s3_config["RAW_DATA_FILE3"])
		self.df_yelp_business = self.sc.read.json(yelp_business_filename)
		self.df_yelp_rating = self.sc.read.json(yelp_rating_filename)
		self.df_sanitory_inspection = self.sc.read.csv(sanitory_inspection_filename)


	def run(self):
		"""
		executes the read from S3, transform by Spark and write to PostgreSQL database sequence
		"""
		self.read_from_s3()
		#self.spark_transform()
		#self.save_to_postgresql()
		


