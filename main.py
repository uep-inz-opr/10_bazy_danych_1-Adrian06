import csv, sqlite3

class ReportGenerator:
  def __init__(self,connection, filename):
    self.connection = connection
    self.filename = filename

  def generate_report(self):
  	cursor = self.connection.cursor()
  	cursor.execute("Select sum(duration) from polaczenia;")
  	result = cursor.fetchall()
  	self.report_text = int(result[0][0])

  def get_report(self):	
    return self.report_text


if __name__ == "__main__":
	sqlite_con = sqlite3.connect("polaczenia.db")
	cur = sqlite_con.cursor()

	cur.execute('''CREATE TABLE polaczenia (from_subscriber data_type INTEGER, 
	                  to_subscriber data_type INTEGER, 
	                  datetime data_type timestamp, 
	                  duration data_type INTEGER , 
	                  celltower data_type INTEGER);''')

	file = input()

	with open(file,'r') as fin:
	    reader = csv.reader(fin, delimiter = ";")
	    next(reader, None)
	    rows = [x for x in reader]
	    cur.executemany("INSERT INTO polaczenia (from_subscriber, to_subscriber, datetime, duration , celltower) VALUES (?, ?, ?, ?, ?);", rows)
	    sqlite_con.commit()

	rp = ReportGenerator(sqlite_con, file)
	rp.generate_report()
	print(rp.get_report())