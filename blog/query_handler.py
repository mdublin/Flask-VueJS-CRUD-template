from .database import session, Person
from sqlalchemy import select, or_, and_
import re

people = session.query(Person)

def query_handler(search_query):
    print("query_handler called")
    
    #search_results = people.filter_by(firstname = search_query).first() or people.filter_by(lastname = search_query).first() or people.filter_by(dob = search_query).first() or people.filter_by(zipcode = search_query).first()
    
    #regex is checking for DOB based on format of search_query, either dd/mm/yyyy or dd.mm.yyyy
    try:
        regcheck = re.search(r'\d+/\d+/\d+', search_query) or re.search(r'\d+.\d+.d+', search_query)
        search_query = regcheck.group()
        print "a DOB was submitted {}".format(search_query)
        search_results = people.filter_by(dob = search_query)
        count = people.filter_by(dob = search_query).count()
        people = search_results
        #people = people.order_by(Person.lastname) #order entries by datetime column
        return (search_results, count)
    except AttributeError as e:
        print(e)
    
    # checking for name or last name query
    if search_query.isalpha() == True:
        search_results = people.filter(and_(Person.firstname == search_query, Person.lastname == search_query))
        count = people.filter(and_(Person.firstname == search_query, Person.lastname == search_query)).count()
        return (search_results, count)

    # last option could be zipcode in either 12345 format or 1212-2334 format, etc
    else:
        search_results = people.filter_by(zipcode=search_query)
        count = people.filter_by(dob = search_query).count()
        return (search_results, count)







