from pyspark.sql.types import *
from optimus import Optimus
from optimus.helpers.json import json_enconding
from pyspark.ml.linalg import Vectors, VectorUDT, DenseVector
import numpy as np
nan = np.nan
import datetime
from pyspark.sql import functions as F
op = Optimus(master='local')
source_df=op.create.df([('names', StringType(), True),('height(ft)', ShortType(), True),('function', StringType(), True),('rank', ByteType(), True),('age', IntegerType(), True),('weight(t)', FloatType(), True),('japanese name', ArrayType(StringType(),True), True),('last position seen', StringType(), True),('date arrival', StringType(), True),('last date seen', StringType(), True),('attributes', ArrayType(FloatType(),True), True),('Date Type', DateType(), True),('timestamp', TimestampType(), True),('Cybertronian', BooleanType(), True),('function(binary)', BinaryType(), True),('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10, 5000000, 4.300000190734863, ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10', '2016/09/10', [8.53439998626709, 4300.0], datetime.date(2016, 9, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Leader'), None), ('bumbl#ebéé  ', 17, 'Espionage', 7, 5000000, 2.0, ['Bumble', 'Goldback'], '10.642707,-71.612534', '1980/04/10', '2015/08/10', [5.334000110626221, 2000.0], datetime.date(2015, 8, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Espionage'), None), ('ironhide&', 26, 'Security', 7, 5000000, 4.0, ['Roadbuster'], '37.789563,-122.400356', '1980/04/10', '2014/07/10', [7.924799919128418, 4000.0], datetime.date(2014, 6, 24), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Security'), None), ('Jazz', 13, 'First Lieutenant', 8, 5000000, 1.7999999523162842, ['Meister'], '33.670666,-117.841553', '1980/04/10', '2013/06/10', [3.962399959564209, 1800.0], datetime.date(2013, 6, 24), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'First Lieutenant'), None), ('Megatron', None, 'None', 10, 5000000, 5.699999809265137, ['Megatron'], None, '1980/04/10', '2012/05/10', [None, 5700.0], datetime.date(2012, 5, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'None'), None), ('Metroplex_)^$', 300, 'Battle Station', 8, 5000000, None, ['Metroflex'], None, '1980/04/10', '2011/04/10', [91.44000244140625, None], datetime.date(2011, 4, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Battle Station'), None), (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)])
class Testop_io(object):
	@staticmethod
	def test_load_csv_local_csv():
		actual_df =op.load.csv('examples/data/foo.csv')
		expected_df = op.create.df([('id', IntegerType(), True),('firstName', StringType(), True),('lastName', StringType(), True),('billingId', IntegerType(), True),('product', StringType(), True),('price', IntegerType(), True),('birth', StringType(), True),('dummyCol', StringType(), True)], [(1, 'Luis', 'Alvarez$$%!', 123, 'Cake', 10, '1980/07/07', 'never'), (2, 'André', 'Ampère', 423, 'piza', 8, '1950/07/08', 'gonna'), (3, 'NiELS', 'Böhr//((%%', 551, 'pizza', 8, '1990/07/09', 'give'), (4, 'PAUL', 'dirac$', 521, 'pizza', 8, '1954/07/10', 'you'), (5, 'Albert', 'Einstein', 634, 'pizza', 8, '1990/07/11', 'up'), (6, 'Galileo', '             GALiLEI', 672, 'arepa', 5, '1930/08/12', 'never'), (7, 'CaRL', 'Ga%%%uss', 323, 'taco', 3, '1970/07/13', 'gonna'), (8, 'David', 'H$$$ilbert', 624, 'taaaccoo', 3, '1950/07/14', 'let'), (9, 'Johannes', 'KEPLER', 735, 'taco', 3, '1920/04/22', 'you'), (10, 'JaMES', 'M$$ax%%well', 875, 'taco', 3, '1923/03/12', 'down'), (11, 'Isaac', 'Newton', 992, 'pasta', 9, '1999/02/15', 'never '), (12, 'Emmy%%', 'Nöether$', 234, 'pasta', 9, '1993/12/08', 'gonna'), (13, 'Max!!!', 'Planck!!!', 111, 'hamburguer', 4, '1994/01/04', 'run '), (14, 'Fred', 'Hoy&&&le', 553, 'pizzza', 8, '1997/06/27', 'around'), (15, '(((   Heinrich )))))', 'Hertz', 116, 'pizza', 8, '1956/11/30', 'and'), (16, 'William', 'Gilbert###', 886, 'BEER', 2, '1958/03/26', 'desert'), (17, 'Marie', 'CURIE', 912, 'Rice', 1, '2000/03/22', 'you'), (18, 'Arthur', 'COM%%%pton', 812, '110790', 5, '1899/01/01', '#'), (19, 'JAMES', 'Chadwick', 467, 'null', 10, '1921/05/03', '#')])
		assert (expected_df.collect() == actual_df.collect())
	@staticmethod
	def test_load_csv_remote_csv():
		actual_df =op.load.csv('https://raw.githubusercontent.com/hi-primus/optimus/master/examples/data/foo.csv')
		expected_df = op.create.df([('id', IntegerType(), True),('firstName', StringType(), True),('lastName', StringType(), True),('billingId', IntegerType(), True),('product', StringType(), True),('price', IntegerType(), True),('birth', StringType(), True),('dummyCol', StringType(), True)], [(1, 'Luis', 'Alvarez$$%!', 123, 'Cake', 10, '1980/07/07', 'never'), (2, 'André', 'Ampère', 423, 'piza', 8, '1950/07/08', 'gonna'), (3, 'NiELS', 'Böhr//((%%', 551, 'pizza', 8, '1990/07/09', 'give'), (4, 'PAUL', 'dirac$', 521, 'pizza', 8, '1954/07/10', 'you'), (5, 'Albert', 'Einstein', 634, 'pizza', 8, '1990/07/11', 'up'), (6, 'Galileo', '             GALiLEI', 672, 'arepa', 5, '1930/08/12', 'never'), (7, 'CaRL', 'Ga%%%uss', 323, 'taco', 3, '1970/07/13', 'gonna'), (8, 'David', 'H$$$ilbert', 624, 'taaaccoo', 3, '1950/07/14', 'let'), (9, 'Johannes', 'KEPLER', 735, 'taco', 3, '1920/04/22', 'you'), (10, 'JaMES', 'M$$ax%%well', 875, 'taco', 3, '1923/03/12', 'down'), (11, 'Isaac', 'Newton', 992, 'pasta', 9, '1999/02/15', 'never '), (12, 'Emmy%%', 'Nöether$', 234, 'pasta', 9, '1993/12/08', 'gonna'), (13, 'Max!!!', 'Planck!!!', 111, 'hamburguer', 4, '1994/01/04', 'run '), (14, 'Fred', 'Hoy&&&le', 553, 'pizzza', 8, '1997/06/27', 'around'), (15, '(((   Heinrich )))))', 'Hertz', 116, 'pizza', 8, '1956/11/30', 'and'), (16, 'William', 'Gilbert###', 886, 'BEER', 2, '1958/03/26', 'desert'), (17, 'Marie', 'CURIE', 912, 'Rice', 1, '2000/03/22', 'you'), (18, 'Arthur', 'COM%%%pton', 812, '110790', 5, '1899/01/01', '#'), (19, 'JAMES', 'Chadwick', 467, 'null', 10, '1921/05/03', '#')])
		assert (expected_df.collect() == actual_df.collect())
	@staticmethod
	def test_load_json_local_json():
		actual_df =op.load.json('examples/data/foo.json')
		expected_df = op.create.df([('billingId', LongType(), True),('birth', StringType(), True),('dummyCol', StringType(), True),('firstName', StringType(), True),('id', LongType(), True),('lastName', StringType(), True),('price', LongType(), True),('product', StringType(), True)], [(123, '1980/07/07', 'never', 'Luis', 1, 'Alvarez$$%!', 10, 'Cake'), (423, '1950/07/08', 'gonna', 'André', 2, 'Ampère', 8, 'piza'), (551, '1990/07/09', 'give', 'NiELS', 3, 'Böhr//((%%', 8, 'pizza'), (521, '1954/07/10', 'you', 'PAUL', 4, 'dirac$', 8, 'pizza'), (634, '1990/07/11', 'up', 'Albert', 5, 'Einstein', 8, 'pizza'), (672, '1930/08/12', 'never', 'Galileo', 6, '             GALiLEI', 5, 'arepa'), (323, '1970/07/13', 'gonna', 'CaRL', 7, 'Ga%%%uss', 3, 'taco'), (624, '1950/07/14', 'let', 'David', 8, 'H$$$ilbert', 3, 'taaaccoo'), (735, '1920/04/22', 'you', 'Johannes', 9, 'KEPLER', 3, 'taco'), (875, '1923/03/12', 'down', 'JaMES', 10, 'M$$ax%%well', 3, 'taco'), (992, '1999/02/15', 'never ', 'Isaac', 11, 'Newton', 9, 'pasta'), (234, '1993/12/08', 'gonna', 'Emmy%%', 12, 'Nöether$', 9, 'pasta'), (111, '1994/01/04', 'run ', 'Max!!!', 13, 'Planck!!!', 4, 'hamburguer'), (553, '1997/06/27', 'around', 'Fred', 14, 'Hoy&&&le', 8, 'pizzza'), (116, '1956/11/30', 'and', '(((   Heinrich )))))', 15, 'Hertz', 8, 'pizza'), (886, '1958/03/26', 'desert', 'William', 16, 'Gilbert###', 2, 'BEER'), (912, '2000/03/22', 'you', 'Marie', 17, 'CURIE', 1, 'Rice'), (812, '1899/01/01', '#', 'Arthur', 18, 'COM%%%pton', 5, '110790'), (467, '1921/05/03', '#', 'JAMES', 19, 'Chadwick', 10, 'null')])
		assert (expected_df.collect() == actual_df.collect())
	@staticmethod
	def test_load_json_remote_json():
		actual_df =op.load.json('https://raw.githubusercontent.com/hi-primus/optimus/master/examples/data/foo.json')
		expected_df = op.create.df([('billingId', LongType(), True),('birth', StringType(), True),('dummyCol', StringType(), True),('firstName', StringType(), True),('id', LongType(), True),('lastName', StringType(), True),('price', LongType(), True),('product', StringType(), True)], [(123, '1980/07/07', 'never', 'Luis', 1, 'Alvarez$$%!', 10, 'Cake'), (423, '1950/07/08', 'gonna', 'André', 2, 'Ampère', 8, 'piza'), (551, '1990/07/09', 'give', 'NiELS', 3, 'Böhr//((%%', 8, 'pizza'), (521, '1954/07/10', 'you', 'PAUL', 4, 'dirac$', 8, 'pizza'), (634, '1990/07/11', 'up', 'Albert', 5, 'Einstein', 8, 'pizza'), (672, '1930/08/12', 'never', 'Galileo', 6, '             GALiLEI', 5, 'arepa'), (323, '1970/07/13', 'gonna', 'CaRL', 7, 'Ga%%%uss', 3, 'taco'), (624, '1950/07/14', 'let', 'David', 8, 'H$$$ilbert', 3, 'taaaccoo'), (735, '1920/04/22', 'you', 'Johannes', 9, 'KEPLER', 3, 'taco'), (875, '1923/03/12', 'down', 'JaMES', 10, 'M$$ax%%well', 3, 'taco'), (992, '1999/02/15', 'never ', 'Isaac', 11, 'Newton', 9, 'pasta'), (234, '1993/12/08', 'gonna', 'Emmy%%', 12, 'Nöether$', 9, 'pasta'), (111, '1994/01/04', 'run ', 'Max!!!', 13, 'Planck!!!', 4, 'hamburguer'), (553, '1997/06/27', 'around', 'Fred', 14, 'Hoy&&&le', 8, 'pizzza'), (116, '1956/11/30', 'and', '(((   Heinrich )))))', 15, 'Hertz', 8, 'pizza'), (886, '1958/03/26', 'desert', 'William', 16, 'Gilbert###', 2, 'BEER'), (912, '2000/03/22', 'you', 'Marie', 17, 'CURIE', 1, 'Rice'), (812, '1899/01/01', '#', 'Arthur', 18, 'COM%%%pton', 5, '110790'), (467, '1921/05/03', '#', 'JAMES', 19, 'Chadwick', 10, 'null')])
		assert (expected_df.collect() == actual_df.collect())
	@staticmethod
	def test_load_parquet_local_parquet():
		actual_df =op.load.parquet('examples/data/foo.parquet')
		expected_df = op.create.df([('id', IntegerType(), True),('firstName', StringType(), True),('lastName', StringType(), True),('billingId', IntegerType(), True),('product', StringType(), True),('price', IntegerType(), True),('birth', StringType(), True),('dummyCol', StringType(), True)], [(1, 'Luis', 'Alvarez$$%!', 123, 'Cake', 10, '1980/07/07', 'never'), (2, 'André', 'Ampère', 423, 'piza', 8, '1950/07/08', 'gonna'), (3, 'NiELS', 'Böhr//((%%', 551, 'pizza', 8, '1990/07/09', 'give'), (4, 'PAUL', 'dirac$', 521, 'pizza', 8, '1954/07/10', 'you'), (5, 'Albert', 'Einstein', 634, 'pizza', 8, '1990/07/11', 'up'), (6, 'Galileo', '             GALiLEI', 672, 'arepa', 5, '1930/08/12', 'never'), (7, 'CaRL', 'Ga%%%uss', 323, 'taco', 3, '1970/07/13', 'gonna'), (8, 'David', 'H$$$ilbert', 624, 'taaaccoo', 3, '1950/07/14', 'let'), (9, 'Johannes', 'KEPLER', 735, 'taco', 3, '1920/04/22', 'you'), (10, 'JaMES', 'M$$ax%%well', 875, 'taco', 3, '1923/03/12', 'down'), (11, 'Isaac', 'Newton', 992, 'pasta', 9, '1999/02/15', 'never '), (12, 'Emmy%%', 'Nöether$', 234, 'pasta', 9, '1993/12/08', 'gonna'), (13, 'Max!!!', 'Planck!!!', 111, 'hamburguer', 4, '1994/01/04', 'run '), (14, 'Fred', 'Hoy&&&le', 553, 'pizzza', 8, '1997/06/27', 'around'), (15, '(((   Heinrich )))))', 'Hertz', 116, 'pizza', 8, '1956/11/30', 'and'), (16, 'William', 'Gilbert###', 886, 'BEER', 2, '1958/03/26', 'desert'), (17, 'Marie', 'CURIE', 912, 'Rice', 1, '2000/03/22', 'you'), (18, 'Arthur', 'COM%%%pton', 812, '110790', 5, '1899/01/01', '#'), (19, 'JAMES', 'Chadwick', 467, 'null', 10, '1921/05/03', '#')])
		assert (expected_df.collect() == actual_df.collect())
	@staticmethod
	def test_load_parquet_remote_parquet():
		actual_df =op.load.parquet('https://raw.githubusercontent.com/hi-primus/optimus/master/examples/data/foo.parquet')
		expected_df = op.create.df([('id', IntegerType(), True),('firstName', StringType(), True),('lastName', StringType(), True),('billingId', IntegerType(), True),('product', StringType(), True),('price', IntegerType(), True),('birth', StringType(), True),('dummyCol', StringType(), True)], [(1, 'Luis', 'Alvarez$$%!', 123, 'Cake', 10, '1980/07/07', 'never'), (2, 'André', 'Ampère', 423, 'piza', 8, '1950/07/08', 'gonna'), (3, 'NiELS', 'Böhr//((%%', 551, 'pizza', 8, '1990/07/09', 'give'), (4, 'PAUL', 'dirac$', 521, 'pizza', 8, '1954/07/10', 'you'), (5, 'Albert', 'Einstein', 634, 'pizza', 8, '1990/07/11', 'up'), (6, 'Galileo', '             GALiLEI', 672, 'arepa', 5, '1930/08/12', 'never'), (7, 'CaRL', 'Ga%%%uss', 323, 'taco', 3, '1970/07/13', 'gonna'), (8, 'David', 'H$$$ilbert', 624, 'taaaccoo', 3, '1950/07/14', 'let'), (9, 'Johannes', 'KEPLER', 735, 'taco', 3, '1920/04/22', 'you'), (10, 'JaMES', 'M$$ax%%well', 875, 'taco', 3, '1923/03/12', 'down'), (11, 'Isaac', 'Newton', 992, 'pasta', 9, '1999/02/15', 'never '), (12, 'Emmy%%', 'Nöether$', 234, 'pasta', 9, '1993/12/08', 'gonna'), (13, 'Max!!!', 'Planck!!!', 111, 'hamburguer', 4, '1994/01/04', 'run '), (14, 'Fred', 'Hoy&&&le', 553, 'pizzza', 8, '1997/06/27', 'around'), (15, '(((   Heinrich )))))', 'Hertz', 116, 'pizza', 8, '1956/11/30', 'and'), (16, 'William', 'Gilbert###', 886, 'BEER', 2, '1958/03/26', 'desert'), (17, 'Marie', 'CURIE', 912, 'Rice', 1, '2000/03/22', 'you'), (18, 'Arthur', 'COM%%%pton', 812, '110790', 5, '1899/01/01', '#'), (19, 'JAMES', 'Chadwick', 467, 'null', 10, '1921/05/03', '#')])
		assert (expected_df.collect() == actual_df.collect())
	@staticmethod
	def test_save_csv():
		source_df=op.create.df([('names', StringType(), True),('height(ft)', ShortType(), True),('function', StringType(), True),('rank', ByteType(), True),('age', IntegerType(), True),('weight(t)', FloatType(), True),('japanese name', ArrayType(StringType(),True), True),('last position seen', StringType(), True),('date arrival', StringType(), True),('last date seen', StringType(), True),('attributes', ArrayType(FloatType(),True), True),('Date Type', DateType(), True),('timestamp', TimestampType(), True),('Cybertronian', BooleanType(), True),('function(binary)', BinaryType(), True),('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10, 5000000, 4.300000190734863, ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10', '2016/09/10', [8.53439998626709, 4300.0], datetime.date(2016, 9, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Leader'), None), ('bumbl#ebéé  ', 17, 'Espionage', 7, 5000000, 2.0, ['Bumble', 'Goldback'], '10.642707,-71.612534', '1980/04/10', '2015/08/10', [5.334000110626221, 2000.0], datetime.date(2015, 8, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Espionage'), None), ('ironhide&', 26, 'Security', 7, 5000000, 4.0, ['Roadbuster'], '37.789563,-122.400356', '1980/04/10', '2014/07/10', [7.924799919128418, 4000.0], datetime.date(2014, 6, 24), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Security'), None), ('Jazz', 13, 'First Lieutenant', 8, 5000000, 1.7999999523162842, ['Meister'], '33.670666,-117.841553', '1980/04/10', '2013/06/10', [3.962399959564209, 1800.0], datetime.date(2013, 6, 24), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'First Lieutenant'), None), ('Megatron', None, 'None', 10, 5000000, 5.699999809265137, ['Megatron'], None, '1980/04/10', '2012/05/10', [None, 5700.0], datetime.date(2012, 5, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'None'), None), ('Metroplex_)^$', 300, 'Battle Station', 8, 5000000, None, ['Metroflex'], None, '1980/04/10', '2011/04/10', [91.44000244140625, None], datetime.date(2011, 4, 10), datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Battle Station'), None), (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)])
		actual_df =source_df.save.csv('test.csv')
		
	@staticmethod
	def test_save_json():
		actual_df =source_df.save.json('test.json')
		
	@staticmethod
	def test_save_parquet():
		actual_df =source_df.save.parquet('test.parquet')
		
