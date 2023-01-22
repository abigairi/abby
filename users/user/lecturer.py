from flask import Blueprint, render_template, session, redirect,request, current_app, flash
from database import mysql
from werkzeug.utils import secure_filename
import os

lecturer = Blueprint('lecturer', __name__)

@lecturer.route('/')
def home():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    # get modules taught by this lecturer which
    cursor.execute('select count(assignment.ID) from assignment inner join lecturer on assignment.module_id=lecturer.module_id where assignment.deadline_date>addtime(NOW(),"03:00:00") and lecturer.ID=%s', [session['id']])
    total_assignments = cursor.fetchone()

    cursor.execute('select count(assignment.ID) from assignment inner join lecturer on assignment.module_id=lecturer.module_id where assignment.deadline_date<addtime(NOW(),"03:00:00") and lecturer.ID=%s', [session['id']])
    deadline_assignments = cursor.fetchone()
    return render_template('lecturer/dashboard.html', total_assignments=total_assignments, deadline_assignments=deadline_assignments)


@lecturer.route('/upload/assignment', methods=['GET','POST'])
def upload_assignment():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        module_id = request.form['module']
        file = request.files['file']
        title = request.form['title']
        deadline =request.form['deadline']


        filename = secure_filename(file.filename)
        workingdir = os.path.abspath(os.getcwd())
        filepath = workingdir + '/mysite/static/uploads/'
        file.save(os.path.join(filepath,filename))
        cursor.execute('insert into assignment values(null,%s,%s,%s,addtime(NOW(),"03:00:00"),%s)', (module_id,filepath,title,deadline))
        mysql.connection.commit()
        flash('Assignment Uploaded Successfully')
        return redirect('/lecturer/upload/assignment')
    else:
        cursor.execute('select * from module inner join lecturer on lecturer.module_id=module.ID where lecturer.user_id=%s', [session['id']])
        modules = cursor.fetchall()
        return render_template('lecturer/upload_assignment.html', modules = modules)


@lecturer.route('/read/assignment')
def read_assignment():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('select * from assignment as a inner join module as m on a.module_id=m.ID inner join lecturer as l on l.module_id=m.ID where l.user_id=%s', [session['id']])
    assignments = cursor.fetchall()
    return render_template('lecturer/read_assignment.html', assignments=assignments)


@lecturer.route('/delete/assignment/<id>')
def delete_assignment(id):
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('delete from assignment where ID=%s', [id])
    mysql.connection.commit()
    return redirect('/lecturer/read/assignment')



