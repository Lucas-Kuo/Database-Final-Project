from turtle import distance
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import secret
import numpy as np
from query import create_query
from matplotlib import pyplot as plt


# load secrets
username = secret.USER
pwd = secret.PASSWORD
url = secret.URL
db = secret.DB_NAME

# build connection and engine
engine = sqlalchemy.create_engine(f"postgresql://{username}:{pwd}@{url}:5432/{db}")
Session = sessionmaker(bind = engine)
connection = engine.connect()
metadata = sqlalchemy.MetaData()

print("Welcome to New York City Yellow taxi records analysis!")
while True:
    # Asking for month
    while True:
        month_input = input("Enter a month from 1 to 3 (or all): ")
        if month_input == "all":
            month = "all"
            break
        elif month_input=='1':
            month = "Jan_2022"
            break
        elif month_input=='2':
            month = "Fab_2022"
            break
        elif month_input=='3':
            month = "Mar_2022"
            break
        else:
            print("Invalid month input:", month_input)
    # Asking for time restrictions
    while True:
        time_res = input("Enter time restricitons (all, partial): ")
        if time_res=="all":
            # all
            time = "all"
            start = None
            end = None
            break
        elif time_res=="partial":
            time = "partial"
            # partial
            while True:
                start = input("Enter the day to start (1 ~ 28): ")
                end = input("Enter the day to end (1 ~ 28): ")
                try:
                    start = int(start)
                    end = int(end)
                except:
                    print(f"Invalid start/end: {start}/{end}")
                if 1<=start<=28 and start<end<=28:
                    break
                else:
                    print(f"Invalid start/end: {start}/{end}")
            break
        else:
            print("Invalid input:", time_res)
    # Asking for analysis column
    while True:
        print("Analysis column selection--")
        print("1: total amount")
        print("2: travel distance")
        print("3: payment analysis")
        print("4: total case")
        analysis_column_input = input("Enter a column to analysis (1~4): ")
        if analysis_column_input=='1':
            column = "1"
            break
        elif analysis_column_input=='2':
            column = "2"
            break
        elif analysis_column_input=='3':
            column = "3"
            break
        elif analysis_column_input=='4':
            column = "4"
            break
        else:
            print("Invalid input:", analysis_column_input)
    
    print("[INFO] Processing query...")
    results = create_query(Session(), metadata, engine, month, time, start, end, column)
    print("[INFO] Retrieved query!")

    if column=='1':
        amounts = []
        for row in results:
            # if(row.total_amount > 2000):
            #     pass
            amounts.append(row.total_amount)
        amounts = np.array(amounts)

        # fig, axs = plt.subplots(1, 1, tight_layout=True)
        # axs.hist(amounts, bins=10)
        plt.plot(range(len(amounts)), amounts)
        plt.savefig(f"./results/{month}_total_amount_distribution.jpg")
        plt.show()
        print("Mean:", amounts.mean())
        print("Standard deviation:", amounts.std())

    elif column=='2':
        distances = []
        for row in results:
            # if(row.trip_distance > 2000):
            #     pass
            distances.append(row.trip_distance)
        distances = np.array(distances)

        # fig, axs = plt.subplots(1, 1, tight_layout=True)
        # axs.hist(distances, bins=10)
        plt.plot(range(len(distances)), distances)
        plt.savefig(f"./results/{month}_travel_distance_distribution.jpg")
        plt.show()
        print("Mean:", distances.mean())
        print("Standard deviation:", distances.std())

    elif column=='3':
        payment = [0, 0]
        for row in results:
            if row.payment_type==1:
                payment[0] += 1
            elif row.payment_type==2:
                payment[1] += 1

        fig1, ax1 = plt.subplots()
        labels = ["Credit Card", "Cash"]
        explode = (0, 0)  # no "explosion"
        ax1.pie(payment, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig(f"./results/{month}_payment_type_distribution.jpg")
        plt.show()

        credit_percentage = payment[0]/len(results) * 100
        cash_percentage = payment[1]/len(results) * 100
        print("%.2f percent passengers pay with credit cards" % credit_percentage)
        print("%.2f percent passengers pay with cash" % cash_percentage)
    elif column=='4':
        cases = len(results)
        if month=='all':
            print(f"There are a total of {cases} taxi usage cases in the three months of 2022 totally.")
        else:
            parsed_month = month[:3]
            print(f"There are a total of {cases} taxi usage cases in {parsed_month} 2022.")


    # Asking for more query
    again = input("One more time?(Y/n): ")
    if again.lower()=='n':
        print("Thanks for using this application!")
        break

connection.close()
engine.dispose()
