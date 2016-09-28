
from . import main
from .. import db

from flask import render_template, jsonify, url_for, request, redirect, current_app

from ..database import Person
from sqlalchemy import select, or_, and_

import re

from query_handler import query_handler

# PAGINATE_BY is a module constant that indicates how many should be on
# each page
PAGINATE_BY = 10

from flask.ext.login import login_required


@main.route("/")
def home():
    return render_template("index.html")


from flask.ext.login import current_user



@main.route("/addperson/", methods=["GET", "POST"])
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
        db.session.add(people)
        db.session.commit()
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

    return render_template("addperson.html")


@main.route("/successconfirm/")
def success_confirm():
    return render_template("successconfirm.html")


# API GET endpoint for people
@main.route("/listpeople/")
def getperson():
    print(request)

    page_num = request.args.get('page')

    results_slice_stop = (PAGINATE_BY * int(page_num))
    results_slice_start = (PAGINATE_BY * (int(page_num) - 1))
    display_entries = {}
    count = 0
    query_results = db.session.query(Person).all()

    # getting query results count to pass to include with server Ajax response
    display_entries = {'results_count': len(query_results)}

    query_results = query_results[results_slice_start:results_slice_stop]

   # for person in session.query(Person).all():
    for person in query_results:
        print person.__dict__
        count += 1
        db_dict = person.__dict__
        del db_dict['_sa_instance_state']
        display_entries[count] = db_dict

    return(jsonify(display_entries))


current_search_query = None


@main.route("/searchpeople", methods=["GET", "POST"])
@main.route("/searchpeople/page/<int:page>")
def searchpeople(page=1):
    print(request)
    # if no search_query in URL will evaluate to None
    search_query = request.args.get('search_for')
    print(search_query)

    print(request.form)

    # for general db display, returns all entries, paginated
    if (search_query is None or search_query == u"") and request.method == "GET":
        print("inside if search_query is None")

        get_all_entries = db.session.query(Person).all()
        count = db.session.query(Person).count()

        print("Total db entries count: {}".format(count))

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

        # all_entries = get_all_entries.order_by(Person.lastname)  # order entries by
        # slicing query to only return entries between start and end
        # indices
        all_entries = get_all_entries[start:end]
        return render_template("searchpeople.html",
                               people=all_entries,
                               has_next=has_next,
                               has_prev=has_prev,
                               page=page,
                               total_pages=total_pages
                               )


    people = db.session.query(Person)

    # DELETE request handler
    if request.method == "POST":
        if "delete_id" in request.form:
            print("inside if")
            print(request.form)
            print(request.get_data())
            person_to_delete = request.form["delete_id"]
            delete_person_by_id = db.session.query(
                Person).filter_by(id=person_to_delete).delete()
            db.session.commit()
            deleteconfirmation = True
            confirm_message = {
                'delete_confirmation': 'id: {}'.format(person_to_delete)}
            return jsonify(confirm_message)

            # return render_template(
            #    "searchpeople.html",
            #    deleteconfirmation=deleteconfirmation)

        else:
            print("making update to entry")
            print(request.form)
            print(request.get_data())

            id = request.form["db_id"]

            # checking for values in the submitted form
            if request.form["firstname"] != '':
                update_dbentry = db.session.query(Person).filter_by(id=id).update(
                    {"firstname": "%s" % (request.form["firstname"])})

            if request.form["lastname"] != '':
                update_dbentry = db.session.query(Person).filter_by(id=id).update(
                    {"lastname": "%s" % (request.form["lastname"])})

            if request.form["DOB"] != '':
                update_dbentry = db.session.query(Person).filter_by(
                    id=id).update({"dob": "%s" % (request.form["DOB"])})

            if request.form["zipcode"] != '':
                update_dbentry = db.session.query(Person).filter_by(id=id).update(
                    {"zipcode": "%s" % (request.form["zipcode"])})

            # getting updated entry to pass back to Ajax caller, which will
            # pass to vue to update item

            db.session.commit()

            updated_entry = {}
            vueEntryIndex = request.form["vue_page_index"]
            updated_entry["entry_vue_page_$index"] = vueEntryIndex

            get_updated_entry = db.session.query(Person).filter_by(id=id)
            for result in get_updated_entry:
                result = result.__dict__
                del result['_sa_instance_state']
                updated_entry[vueEntryIndex] = result

            print(jsonify(updated_entry))
            return jsonify(updated_entry)

    # when page is initially loaded
    # if search_query is None:
    #    return render_template("searchpeople.html")

    else:
        print("SEARCH QUERY")
        # NEW SEARCH QUERY CHECK LOGIC
        # check if there is already a query paramter in the URL with pagination
# use case is if user has paginated through initial returns query results, and then goes to try another search. Search query results will be presented with the most recent page, instead of staring from first results first page in query results.
        # regex to compare current path to original URL route

        current_url = request.path
        print("current_url: {}".format(current_url))
        regex = re.compile(r'/searchpeople/page/[0-9]')
        if regex.match(current_url) is not None and (
                current_search_query != search_query):
            print("regex match")
            # return redirect(url_for('searchpeople',
            # search_query=search_query))
            return redirect('/searchpeople?search_for={}'.format(search_query))

        # END OF NEW SEARCH QUERY CHECK LOGIC

        print("submitting search_query to query_handler....")
        call_query_handler = query_handler(search_query)

        # if no results found, call_query_handler returns True for noresults
        if call_query_handler is None:
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

        global current_search_query
        current_search_query = search_query

        display_entries = {'results_count': count}
        for person in search_results:
            print person.__dict__
            count += 1
            db_dict = person.__dict__
            del db_dict['_sa_instance_state']
            display_entries[count] = db_dict

        print("display_entries: ")
        print(display_entries)

        return(jsonify(display_entries))

        # return render_template("searchpeople.html",
        #                       people=search_results,
        #                       search_for=search_query,
        #                       has_next=has_next,
        #                       has_prev=has_prev,
        #                       page=page,
        #                       total_pages=total_pages
        #                       )


@main.route('/searchresults/<string:search_Person>')
def searchresults(search_Person):
    # print(request.args.get('search_for_input'))

    print(search_Person)

    # for results in search_Person:
    #    print(results.__dict__)
    #    print(results.__dict__["firstname"])

    return render_template('searchresults.html')


@main.route("/viewpeople/")
def viewpeople():
    #view all people in db
    return render_template('viewpeople.html')


@main.route("/vuetest/")
def vuetest():
    message = "testestestest"
    return render_template('vuetest.html')


@main.route('/vuetest_2/')
def vuetest_2():
    return render_template('vuetest_2.html')


@main.route('/ajaxtest/')
def ajaxtest():
    return render_template('ajaxtest.html')


# Version of searchpeople view with Ajax pagination

@main.route("/searchpeople_ajax", methods=["GET", "POST"])
@main.route("/searchpeople_ajax/page/<int:page>")
def searchpeople_ajax():
    search_query = request.args.get('search_for')

    # print(request.form)
    # print(search_query)

    if search_query is None:
        get_all_entries = db.session.query(Person).all()
        count = db.session.query(Person).count()

        print("Total db entries count: {}".format(count))

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

        # all_entries = get_all_entries.order_by(Person.lastname)  # order entries by
        # slicing query to only return entries between start and end
        # indices
        all_entries = get_all_entries[start:end]
        return render_template("searchpeople_ajax.html",
                               people=all_entries,
                               has_next=has_next,
                               has_prev=has_prev,
                               page=page,
                               total_pages=total_pages
                               )

        # return render_template("searchpeople.html")

    # checking if unicode string is empty (i.e. someone just clicked search
    # p
    # with an empty search field)

    if not search_query:
        noresult = True
        return render_template("searchpeople_ajax.html", noresult=noresult)
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
            delete_person_by_id = db.session.query(
                Person).filter_by(id=person_to_delete).delete()
            db.session.commit()
            deleteconfirmation = True
            return render_template(
                "searchpeople_ajax.html",
                deleteconfirmation=deleteconfirmation)

        else:
            print(request.form)
            print(request.get_data())

            id = request.form["db_id"]

            if request.form["firstname"] != '':
                update_dbentry = db.session.query(Person).filter_by(id=id).update(
                    {"firstname": "%s" % (request.form["firstname"])})
            if request.form["lastname"] != '':
                update_dbentry = db.session.query(Person).filter_by(id=id).update(
                    {"lastname": "%s" % (request.form["lastname"])})
            if request.form["DOB"] != '':
                update_dbentry = db.session.query(Person).filter_by(
                    id=id).update({"dob": "%s" % (request.form["DOB"])})
            if request.form["zipcode"] != '':
                update_dbentry = db.session.query(Person).filter_by(id=id).update(
                    {"zipcode": "%s" % (request.form["zipcode"])})

            db.session.commit()
            # return (request.url)
            # return ("entry updated")

    if search_query is None:
        return render_template("searchpeople_ajax.html")

    else:
        print("calling query_handler....")
        call_query_handler = query_handler(search_query)

        # if no results found, call_query_handler returns True for noresults
        if call_query_handler is None:
            noresult = True
            return render_template("searchpeople_ajax.html", noresult=noresult)

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
        return render_template("searchpeople_ajax.html",
                               people=search_results,
                               search_for=search_query,
                               has_next=has_next,
                               has_prev=has_prev,
                               page=page,
                               total_pages=total_pages
                               )
