from flask import render_template, redirect, session, request
from flask_app import app

from flask_app.models import user, job


#Visible routes
@app.route("/dashboard")
def all_jobs_page():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user_logged = user.User.get_user_by_id(data), all_jobs = job.Job.get_all_jobs_with_users())

@app.route("/new/job")
def requested_job_page():
    if 'user_id' not in session:
        return redirect("/")
    data ={
        'id': session['user_id']
    }
    return render_template("job_request.html", user_logged = user.User.get_user_by_id(data))

@app.route("/edit/<int:id>")
def edit_job_page(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
    }
    return render_template("edit_job.html", this_job = job.Job.get_one_job_with_user(data))


@app.route("/show/<int:id>")
def job_info_page(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': id,
    }
    form_data = {
        'id': session['user_id']
    }
    print(request.form)
    return render_template("show_job.html", user_logged = user.User.get_user_by_id(form_data), this_job = job.Job.get_one_job_with_user(data))


@app.route("/user/account")
def users_account_page():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    return render_template("view_account.html", user = user.User.get_by_id(data))


# Hidden routes
@app.route("/jobs/<int:id>/delete")
def destroy(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': id
    }
    job.Job.destroy(data)
    return redirect('/dashboard')

@app.route("/jobs/add_to_db", methods=["POST"])
def add_job_to_db():
    if 'user_id' not in session:
        return redirect('/')
    if not job.Job.validate_job(request.form):
        return redirect('/new/job')

    data = {
        'user_id': session['user_id'],
        'customer': request.form['customer'],
        'location': request.form['location'],
        'description': request.form['description'],
        'date_performed': request.form['date_performed'],
    }
    job.Job.save(data)
    return redirect('/dashboard')

@app.route("/jobs/<int:id>/edit_in_db", methods=["POST"])
def update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not job.Job.validate_job(request.form):
        return redirect(f'/edit/{id}')

    data = {
        'id': id,
        'customer': request.form['customer'],
        'location': request.form['location'],
        'description': request.form['description'],
        'date_performed': request.form['date_performed'],
    }
    job.Job.update(data)
    return redirect('/user/account')