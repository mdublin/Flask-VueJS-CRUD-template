
from flask import render_template, jsonify

from CRUD import app
from .database import session, Person
from sqlalchemy import select, or_, and_

import re


from query_handler import query_handler


# PAGINATE_BY is a module constant that indicates how many should be on
# each page
PAGINATE_BY = 5

from flask.ext.login import login_required


@app.route("/")
def index():
    return render_template("index.html")


from flask import request, redirect, url_for
from flask.ext.login import current_user


@app.route("/addperson/", methods=["GET", "POST"])
def addperson():
    print(request)
    if request.method == "POST":
        print(request.get_data())
        print(request.form)

        people = Person(
            firstname=request.form["firstname"],
            lastname=request.form["lastname"],
            dob=request.form["DOB"],
            zipcode=request.form["postalCode"]
        )
        session.add(people)
        session.commit()
        display_entries = {}
        # count is just acting as a key for the value, which is every person
        # dict row entry representation
        count = 0
        for person in session.query(Person).all():
            print person.__dict__
            db_dict = person.__dict__
            del db_dict['_sa_instance_state']
            display_entries[count] = db_dict
            count += 1

        # return(jsonify(display_entries))
        # return ("<h1>POST OKAY</h1>")
        # return redirect(url_for("people"))
    return render_template("addperson.html")


@app.route("/successconfirm/")
def success_confirm():
    return render_template("successconfirm.html")


# API GET endpoint for people listing
@app.route("/listpeople/")
def getperson():
    display_entries = {}
    count = 0
    for person in session.query(Person).all():
        print person.__dict__
        count += 1
        db_dict = person.__dict__
        del db_dict['_sa_instance_state']
        display_entries[count] = db_dict
    return(jsonify(display_entries))


@app.route("/searchpeople", methods=["GET", "POST"])
@app.route("/searchpeople/page/<int:page>")
def searchpeople(page=1):
    search_query = request.args.get('search_for')

    # print(request.form)
    # print(search_query)

    if search_query is None:
        return render_template("searchpeople.html")

    # checking if unicode string is empty (i.e. someone just clicked search
    # with an empty search field)
    if not search_query:
        noresult = True
        return render_template("searchpeople.html", noresult=noresult)
    # cleaning up any possible trailing white space
    if search_query is not None:
        search_query = search_query.rstrip()

    # search_query is a unicode as Flask, Jinja2 are all Unicode based

    people = session.query(Person)
    #search_results = people.filter_by(firstname = search_query).first()

    print(request.method)

    # DELETE request handler
    if request.method == "POST":
        if "delete_id" in request.form:
            print("inside if")
            print(request.form)
            print(request.get_data())
            person_to_delete = request.form["delete_id"]
            delete_person_by_id = session.query(
                Person).filter_by(id=person_to_delete).delete()
            session.commit()
            deleteconfirmation = True
            return render_template(
                "searchpeople.html",
                deleteconfirmation=deleteconfirmation)

        else:
            print(request.form)
            print(request.get_data())

            id = request.form["db_id"]

            if request.form["firstname"] != '':
                update_dbentry = session.query(Person).filter_by(id=id).update(
                    {"firstname": "%s" % (request.form["firstname"])})
            if request.form["lastname"] != '':
                update_dbentry = session.query(Person).filter_by(id=id).update(
                    {"lastname": "%s" % (request.form["lastname"])})
            if request.form["DOB"] != '':
                update_dbentry = session.query(Person).filter_by(
                    id=id).update({"dob": "%s" % (request.form["DOB"])})
            if request.form["zipcode"] != '':
                update_dbentry = session.query(Person).filter_by(id=id).update(
                    {"zipcode": "%s" % (request.form["zipcode"])})

            session.commit()
            # return (request.url)
            # return ("entry updated")

    if search_query is None:
        return render_template("searchpeople.html")

    else:
        print("calling query_handler....")
        call_query_handler = query_handler(search_query)

        # if no results found, call_query_handler returns True for noresults
        if call_query_handler == None:
            noresult = True
            return render_template("searchpeople.html", noresult=noresult)

        search_results, count = call_query_handler

        # Zero-indexed page
        page_index = page - 1  # page_index is page number - 1 = 0 for zero-based index
        # query object to determine number of enties in total
        # start = 0 X 10 = 0  index of first item displayed
        start = page_index * PAGINATE_BY
        end = start + PAGINATE_BY  # end = 0 + 10 = 10  index of last item displayed
        # total number of pages of content
        total_pages = (count - 1) / PAGINATE_BY + 1
        # this is a boolean statement --> if True, then there's a next page
        has_next = page_index < total_pages - 1
        has_prev = page_index > 0  # this is a boolean statement

        search_results = search_results.order_by(
            Person.lastname)  # order entries by
        # slicing query to only return entries between start and end
        # indices
        search_results = search_results[start:end]
        return render_template("searchpeople.html",
                               people=search_results,
                               search_for=search_query,
                               has_next=has_next,
                               has_prev=has_prev,
                               page=page,
                               total_pages=total_pages
                               )


@app.route('/searchresults/<string:search_Person>')
def searchresults(search_Person):
    # print(request.args.get('search_for_input'))

    print(search_Person)

    # for results in search_Person:
    #    print(results.__dict__)
    #    print(results.__dict__["firstname"])

    return render_template('searchresults.html')


@app.route("/viewpeople/")
def viewpeople():
    '''
    view all people in db
    '''
    return render_template('viewpeople.html')


@app.route("/vuetest/")
def vuetest():
    message = "testestestest"
    return render_template('vuetest.html')
