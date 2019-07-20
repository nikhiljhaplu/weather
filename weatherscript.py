import requests
from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app)

#app.route("/")
import datetime
import sqlite3
import re
class DbWrapper:
    def __init__(self):
        self.conn = sqlite3.connect('owm.db')
        self.c = self.conn.cursor()

    def create(self, table_name, column):
        query = "create table if not exists {0}({1});".format(table_name, column)
        self.c.execute(query)
#        self.conn.commit()
    def alter(self):
        query = "alter table owm_table alter column date_time"
        self.c.execute(query)

    def Insert(self, table_name, column, value):
        query = "insert into {0}({1}) values ({2});".format(table_name, column, value)

        self.c.execute(query)
        #    return query
#        print("insert query :- ",query)
        self.conn.commit()
        #except:
         #   return "data already present!!!"

    def update(self, table_name, column1, value1, column2, value2):
        query = '''update {0} set {1} = {2} where {3} = "{4}"; '''.format(table_name, column1, value1, column2, value2)
        # print(query)
#        print(query)
        self.c.execute(query)
        self.conn.commit()
    # eg - UPDATE COMPANY(0) SET ADDRESS(1) = 'Texas'(2) WHERE ID(3) = 6(4);

    def select(self, table_name, field, key= None, val = None, order = False , like = False):
        query = "select {0} from {1}".format(field, table_name)
        if key and val:
            if like:
                q = " where {0} like '%{1}%'".format(key, val)
                query = query + q
                self.c.execute(query)

            else:
                q = " where {0} = '{1}'".format(key,val)
                query = query + q
                self.c.execute(query)
        elif order:
            q = " order by {0} ASC;".format(field)
            query = query + q
            self.c.execute(query)
        else:
            return self.c.execute(query)
#        rows = self.c.fetchall()
#        return rows[len(rows)-limit if limit else 0:]

        self.conn.commit()

# def select_partial(self, column, table_name, where, condition,  value):
#      query = "select {0} from {1} where {2} {3} '{4}'".format(column, table_name,where, condition, value)
    #    self.c.execute(query)


    def myWeatherCityName(self, CityName):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CityName},in&appid=ef88d5fc275e999988a44df6b416e1c0"
        response = requests.get(url)
        return response.json()

    def myWeatherZipcode(self, zip_code):
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},in&appid=ef88d5fc275e999988a44df6b416e1c0"
        response = requests.get(url)
        return response.json()
   # userInput = input()


    def fetchApi(self, userInput):
        matchZip = re.match(r"[0-9]{6}", userInput)
        matchCity = re.match(r"^[A-Za-z]+$", userInput)

        if matchZip:
            print("you enterd zip code please enter city name")
            return "enter city"
#            data = self.myWeatherZipcode(userInput)
#            print(data['name'],data['main'])
        elif matchCity:
            data = self.myWeatherCityName(userInput)
            #print(data)
            try:
                self.Insert("owm_table", "city, temp, pressure, humidity , temp_min, temp_max, date_time",
                        '"{0}",{1},{2},{3},{4},{5},"{6}"'.format(data['name'], data['main']['temp'], data['main']['pressure'],
                                                           data['main']['humidity'], data['main']['temp_min'],
                                                           data['main']['temp_max'],str(datetime.datetime.now())))
            except:
                self.update("owm_table", "temp",data['main']['temp'], "city",data['name'])
                self.update("owm_table", "pressure", data['main']['pressure'], "city", data['name'])
                self.update("owm_table", "humidity", data['main']['humidity'], "city", data['name'])
                self.update("owm_table", "temp_min", data['main']['temp_min'], "city", data['name'])
                self.update("owm_table", "temp_max", data['main']['temp_max'], "city", data['name'])
                self.update("owm_table", "date_time", '"'+str(datetime.datetime.now())+'"', "city", data['name'])

#                print(data['name'],data['main'])
        else:
            print("enter correct option")


        #   update{0}set{1} = {2}where{3} = {4};
        # eg - UPDATE COMPANY(0) SET ADDRESS(1) = 'Texas'(2) WHERE ID(3) = 6(4);
        self.conn.commit()
    def print(self):
        a = self.c.fetchall()
        return str(a[0])
#        print("results = ",a)
    def printall(self):
        b = self.c.fetchall()
        return {"result" : b}

obj = DbWrapper()
obj.create("owm_table", "  city string primary key, temp float,  pressure float, humidity float,temp_min float, temp_max float")
#obj.fetchApi(input("enter zip code or city name - "))
#obj.Insert("weather","temp, pressure, humidity , temp_min, temp_max",data)
# obj.select_partial("* ", "new_test", "id", '=', "2")
#obj.alter()

# obj.select("owm_table","*")
# obj.printall()

@app.route("/")
def home():
    return render_template("index.html")
# route to take input from user and show data from database =
@app.route("/db")
def select():
    obj1 = DbWrapper()
#    obj.select("owm_table", "*","city",input("enter city name = "))
    city =  request.args["city"]
    obj1.select("owm_table", "*","city",city)
    return obj1.print()
#route to take input and fetch from wheather Api and store in db and show results from db
@app.route("/insert")
def insert():
    obj2 = DbWrapper()
    city = request.args["city"]
    obj2.fetchApi(city)
    obj2.select("owm_table", "*", "city", city)
    return obj2.print()
@app.route("/data")
def full():
    obj3 = DbWrapper()
#    obj.select("owm_table", "*","city",input("enter city name = "))
#    city =  request.args["city"]
    obj3.select("owm_table", "*")
    return obj3.printall()
"""
    zipcde = request.args["zipcode"]
    return obj.myWeatherZipcode(zipcde)
    return obj.myWeatherCityName(city)
"""

"""obj.print()
print("to fetch online enter 1 or to exit enter 2 = ")
action = int(input())
if action == 1:
    enter_city = input("enter zip code or city name - ")
    obj.fetchApi(enter_city)
    obj.select("owm_table", "*","city",enter_city)
    obj.print()

else:
    print("thankyou!")
"""

if __name__ == "__main__":
    app.run( port=80 ,debug = True)

# db name = own
# table name = owm_table