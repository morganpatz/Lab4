from flask import Flask, request, redirect, url_for
import sqlite3

dbFile = 'todo.db'
conn = None

# only use __name__ when its just one file
# if its a package, use the package name
app = Flask(__name__)


def get_conn():
   # not defining a new conn var
   global conn
   if conn is None:
      conn = sqlite3.connect(dbFile)
      conn.row_factory = sqlite3.Row
   return conn

@app.teardown_appcontext
def close_connection(exception):
   global conn
   if conn is not None:
      conn.close()
      conn = None

def query_db(query, args=(), one=False):
   cur = get_conn().cursor()
   cur.execute(query, args)
   r = cur.fetchall()
   cur.close()
   return (r[0] if r else None) if one else r

def add_task(category, priority, description):
   tasks = query_db('INSERT INTO tasks (category, priority, description) VALUES (?, ?, ?)', [category, priority, description], one=True)
   get_conn().commit()

def print_tasks():
   tasks = query_db('SELECT * FROM tasks')
   for task in tasks:
      print("Task(category): %s " % task['category'])
   print("%d tasks in total." % len(tasks))
"""
if __name__ == '__main__':
   query_db("DELETE FROM tasks")
   print_tasks()
   add_task("CMPUT 410")
   add_task("Shopping")
   add_task("Coding")
   print_tasks()
"""


# if this is added to the end of a url, the next method should be run
# '/' is used for no params following host
@app.route('/')
def welcome():
   return '<h1>Welcome to Flask Lab!</h1>'

@app.route('/task', methods = ['GET', 'POST'])
def task():
   
   # POST
   if request.method == 'POST':
      category = request.form['category']
      priority = request.form['priority']   
      description = request.form['description']
      add_task(category, priority, description)
         
      #tasks.append({'category':category, 'priority':priority, 'description':description})        
      return redirect('/task')
      #return redirect(url_for('task'))
    
   # GET
   resp = """
   <form action="" method =post>
   <p>Category: <input type=text name=category></p>
   <p>Priority: <input type=number name=priority></p>
   <p>Description: <input type=text name=description></p>
   <p><input type=submit value=Add></p>
   </form>
   """
   # Show the table
   resp = resp + """
   <table border="1" cellpadding="3">
       <tbody>
           <tr>
               <th>Category</th>
               <th>Priority</th>
               <th>Description</th>
           </tr>
           """
   
   tasks = query_db('SELECT * FROM tasks')
   for task in tasks:
      resp = resp + "<tr><td>%s</td>" % (task['category'])
      resp = resp + "<td>%s</td>" % (task['priority'])
      resp = resp + "<td>%s</td></tr>" % (task['description'])
      
   return resp


if __name__ == '__main__':
   app.debug = True
   app.run()