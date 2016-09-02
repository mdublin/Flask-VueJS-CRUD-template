
from flask import render_template, jsonify

from blog import app
from .database import session, Person

PAGINATE_BY = 10 # PAGINATE_BY is a module constant that indicates how many should be on each page

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
        # count is just acting as a key for the value, which is every person dict row entry representation
        count = 0
        for person in session.query(Person).all():
            print person.__dict__
            count += 1
            db_dict = person.__dict__
            del db_dict['_sa_instance_state']
            display_entries[count] = db_dict
         
        return(jsonify(display_entries))    
        #return ("<h1>POST OKAY</h1>")
        #return redirect(url_for("people"))
    return render_template("addperson.html")





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


'''
@app.route("/addperson/", methods=["POST"])
def addperson_post():
    people = session.query(Person)
    people = Person(
        firstname=request.form["firstname"],
        lastname=request.form["lastname"],
        dob=request.form["DOB"],
        zipcode=request.form["zipcode"]
    )
    session.add(people)
    session.commit()
    return redirect(url_for("people"))
'''



@app.route("/viewpeople", methods=["GET", "POST"])
@app.route("/viewpeople/page/<int:page>")
def viewpeople(page=1):
    search_query = request.args.get('search_for')
    people = session.query(Person)
    search_results = people.filter_by(firstname = search_query).first()
    
    if search_query is None:
        return render_template("viewpeople.html")

    else:
        search_results = people.filter_by(firstname = search_query).first()
        
        if search_results is not None:
            search_results = people.filter_by(firstname = search_query)
            # getting results count, which will be used for pagination below
            count = people.filter_by(firstname = search_query).count()
            # Zero-indexed page
            page_index = page - 1 #page_index is page number - 1 = 0 for zero-based index
            #count = session.query(Person).count() #using count method of query object to determine number of enties in total
            start = page_index * PAGINATE_BY # start = 0 X 10 = 0  index of first item displayed
            end = start + PAGINATE_BY # end = 0 + 10 = 10  index of last item displayed
            total_pages = (count - 1) / PAGINATE_BY + 1 # total number of pages of content
            has_next = page_index < total_pages - 1 # this is a boolean statement --> if True, then there's a next page
            has_prev = page_index > 0 # this is a boolean statement
            people = people.order_by(Person.lastname) #order entries by datetime column
            people = people[start:end] # slicing query to only return entries between start and end indices
            print("STUFF: ")
            print(people, has_next, has_prev, page, total_pages)
            return render_template("viewpeople.html",
                                   people=search_results,
                                   search_for=search_query,
                                   has_next=has_next,
                                   has_prev=has_prev,
                                   page=page,
                                   total_pages=total_pages
                                   )
        else:
            noresult = True
            return render_template("viewpeople.html", noresult=noresult)
    
    '''
    print("search_results: {}".format(dir(search_results)))

    new = search_results.__iter__()
    print(dir(new))
    print(type(new))

    boo = next(new)

    print(type(boo))

    for results in search_results:
        print results


    if request.method == "POST":
        print("POST request made")
        print(request.get_data())
        print(request.form)
        search_submission = request.form["search_for_input"]

        #search_Person = people.filter_by( firstname = search_submission, lastname = search_submission, dob = search_submission, zipcode = search_submission )
        
        # searching Person table entries by firstname column
        search_Person = people.filter_by( firstname = search_submission )
        
# iterating through returned search_Person results object, printing contents of objects via internal __dict__ of SQLAlchemyn object
        #for results in search_Person:
        #    print(results.__dict__)
        #
        print(search_Person)

        return redirect(url_for("searchresults", search_Person=search_Person))          

    '''

@app.route('/searchresults/<string:search_Person>')
def searchresults(search_Person):
    #print(request.args.get('search_for_input'))
    
    print(search_Person)

    #for results in search_Person:
    #    print(results.__dict__)
    #    print(results.__dict__["firstname"])
    
    return render_template('searchresults.html')

@app.route("/vuetest/")
def vuetest():
    message="shitty"
    return render_template('vuetest.html')



'''

# edit entry option from single entry display page
@app.route("/editentry/<int:id>", methods=["GET"]) #we don't necessarily need to have GET here, but adding to be uniform with add_entry function above
@login_required
def editentry(id=1):
    entries = session.query(Entry)
    for entry in entries:
        if entry.id == id:
            dbentry = entry
            entry.content
            author = entry.author_id
        else:
            pass

    # post edit entry changes with current user control logic below for allowing/prohbiting access to EDIT and DELETE buttons.
    # not using these lines because there is a jinja2 conditional statement builtin the entry.html template that checks if current_user == the author of the post.
    #currentUser = current_user.id #using current_user object to find current user courtesy of Flask-login
    #if author != currentUser:
    #    return render_template("edit_access_error.html")
    #else:
    #    return render_template("editentry.html", dbentry=dbentry, current_user=current_user, author=author)
#        else:
#            pass
    return render_template("editentry.html", dbentry=dbentry)


# post edit entry changes
@app.route("/editentry/<int:id>", methods=["POST"])
@login_required
def editentry_post(id=1):
    # using Flask's request.form dictionary to access the data submitted with your form and assign it to the correct fields in the entry.
    updated_title=request.form["title"]
    updated_content=request.form["content"]

   # nice little SQLAlchemy query/filter/update statement to update existing post with new data
    update_dbentry = session.query(Entry).filter_by(id=id).update({"title": "%s" %(updated_title), "content": "%s" % (updated_content)})
    
    entries = session.query(Entry)
    for entry in entries:
        if entry.id == id:
            dbentry = entry
            entry.content
        else:
            pass
    # rendering entry.html with updated content
    return render_template("entry.html", dbentry=dbentry)




# confirm delete entry
@app.route("/delete/<int:id>")
@login_required
def delete(id=1):
    #entry_to_delete = request.form["value"]
    #print entry_to_delete
    entries = session.query(Entry)
    for entry in entries:
        if entry.id == id:
            dbentry = entry
            entry.content
        else:
            pass
    return render_template("delete.html", dbentry=dbentry)


# delete entry
@app.route("/delete/<int:id>", methods=['POST'])
@login_required
def delete_entry(id=1):
    entry_to_delete = request.form["content"]
    print entry_to_delete
    #entries = session.query(Entry)
    delete_entry_by_id = session.query(Entry).filter_by(id=entry_to_delete).delete()
        #    for entry in entries:
        #if entry.id == id:
        #    dbentry = entry
        #    entry.content
        #else:
        #    pass
    return redirect(url_for("deleted_confirmation"))


@app.route("/deleted")
def deleted_confirmation():
    return render_template("deleted_confirmation.html")

'''
