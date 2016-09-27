from .database import session, Person
from sqlalchemy import select, or_, and_
import re

people = session.query(Person)

def query_handler(search_query):

    # passed back to viewpeople view if no results are returned from search 
    #noresult = True

    people = session.query(Person)
    print("query_handler called")
    
    #search_results = people.filter_by(firstname = search_query).first() or people.filter_by(lastname = search_query).first() or people.filter_by(dob = search_query).first() or people.filter_by(zipcode = search_query).first()
    
    #regex is checking for DOB based on format of search_query, either dd/mm/yyyy or dd.mm.yyyy yyyy-mm-dd or some derivation thereof
    try:
        print("try hit")
        regcheck = re.search(r'\d+/\d+/\d+', search_query) or re.search(r'\d+.\d+.d+', search_query) or re.search(r'\d+-\d+-\d+', search_query)
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
        print("isalpha() hit")
       
        # and_ only returns result for entry that meets both cases vs using each query and Python and operator
        #search_results = people.filter(and_(Person.firstname == search_query, Person.lastname == search_query))
        
        #search_results = session.query(Person).filter_by(firstname = search_query) and session.query(Person).filter_by(lastname = search_query)

        search_results = session.query(Person).filter(or_(Person.firstname.like(search_query), Person.lastname.like(search_query)))

        count = session.query(Person).filter(or_(Person.firstname.like(search_query), Person.lastname.like(search_query))).count()

        print(count)

        for results in search_results:
            print results.__dict__

        if count == 0:
            return None
        else:
            return (search_results, count)


    # last option could be zipcode in either 12345 format or 1212-2334 format, etc
    else:
        search_results = people.filter_by(zipcode=search_query)
        count = people.filter_by(zipcode = search_query).count()
        
        if count == 0:
            return None
        return (search_results, count)

