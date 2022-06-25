import sqlalchemy
import datetime

month_dir = {
    "Jan_2022":1,
    "Fab_2022":2,
    "Mar_2022":3
}

def create_query(session, metadata, engine, month, time, start, end, column):
    if month == "all":
        months = ["Jan_2022", "Fab_2022", "Mar_2022"]
        results = []
        for m in months:
            table = sqlalchemy.Table(m, metadata, autoload=True, autoload_with=engine)
            if column=='1': # total amount
                query = session.query(table).with_entities(table.columns.total_amount)
            elif column=='2': # travel distance
                query = session.query(table).with_entities(table.columns.trip_distance)
            elif column=='3': # payment type
                query = session.query(table).with_entities(table.columns.payment_type)
            elif column=='4': # total case
                query = session.query(table)
            
            if time=="all":
                query = query.filter(table.columns.total_amount > 0)
            else:
                start_time = datetime.datetime(2022, month_dir[m], start)
                end_time = datetime.datetime(2022, month_dir[m], end, hour=23, minute=59)
                query.filter(table.columns.total_amount > 0, table.columns.tpep_pickup_datetime > start_time, table.columns.tpep_pickup_datetime < end_time)
            
            results.extend(query.all())
    else:
        table = sqlalchemy.Table(month, metadata, autoload=True, autoload_with=engine)
        if column=='1': # total amount
            query = session.query(table).with_entities(table.columns.total_amount)
        elif column=='2': # travel distance
            query = session.query(table).with_entities(table.columns.trip_distance)
        elif column=='3': # payment type
            query = session.query(table).with_entities(table.columns.payment_type)
        elif column=='4': # total case
            query = session.query(table).with_entities(table.columns.payment_type)
        
        if time=="all":
            query = query.filter(table.columns.total_amount > 0)
        else:
            start_time = datetime.datetime(2022, month_dir[month], start)
            end_time = datetime.datetime(2022, month_dir[month], end, hour=23, minute=59)
            query.filter(table.columns.total_amount > 0, table.columns.tpep_pickup_datetime > start_time, table.columns.tpep_pickup_datetime < end_time)
        
        results = query.all()

    return results
