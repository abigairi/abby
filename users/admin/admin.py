from flask import Blueprint, render_template, redirect, request, flash, session
from database import mysql

admin = Blueprint('admin', __name__)

# functions
def notify(receiver, title, sms):
    cursor = mysql.connection.cursor()
    status = 'unreaded'
    if 'all' in receiver:
        cursor.execute('insert into notification values(null,%s,%s,%s,%s)', (receiver,title,sms, status))
        mysql.connection.commit()
    else:
        cursor.execute('insert into notification values(null,%s,%s,%s,%s)', (receiver,title,sms, status))
        mysql.connection.commit()


@admin.route('/')
def home():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('select count(ID) from user')
    user = cursor.fetchone()
    return render_template('admin/dashboard.html', total_users=user)

@admin.route('/create/student', methods=['GET','POST'])
def create_student():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    if request.method== 'POST':
        regno = request.form['regno']
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']
        programme = request.form['programme']

        # find if user with that email already exist
        cursor.execute('select * from user where email=%s', [email])
        found = cursor.fetchone()
        if found:
            flash('Failed because user with that email already exist')
            return redirect('/admin/create/student')

        cursor.execute('insert into user values(null,%s,%s,%s,%s,%s)', (regno,firstname,surname,email,phone))
        mysql.connection.commit()

        # insert role details
        # find user id
        cursor.execute('select * from user order by ID desc limit 1')
        user_id = cursor.fetchone()

        cursor.execute('insert into student values(null,%s,%s)', (user_id[0],programme))
        mysql.connection.commit()

        # insert login details
        username = regno
        password = surname
        role = 'student'

        cursor.execute('insert into login_details values(null,%s,%s,%s,%s)', (user_id[0],username,password,role))
        mysql.connection.commit()
        flash('new user have been added successfully')
        return redirect('/admin/create/student')

    else:
        cursor.execute('select * from programme')
        programmes = cursor.fetchall()
        return render_template('admin/create_student.html', programmes=programmes)


@admin.route('/create/lecturer', methods=['GET','POST'])
def create_lecturer():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    if request.method== 'POST':
        regno = request.form['regno']
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']
        modules = request.form.getlist('modules[]')

        # find if user with that email already exist
        cursor.execute('select * from user where email=%s', [email])
        found = cursor.fetchone()
        if found:
            flash('Failed because user with that email already exist')
            return redirect('/admin/create/lecturer')

        cursor.execute('insert into user values(null,%s,%s,%s,%s,%s)', (regno,firstname,surname,email,phone))
        mysql.connection.commit()

        # insert roles details
        # find user id
        cursor.execute('select * from user order by ID desc limit 1')
        user_id = cursor.fetchone()
        # find module ID
        for module in modules:
            # check module ID
            cursor.execute('select * from module where ID=%s',[module])
            module_id = cursor.fetchone()

            if module_id:
                # check if lecturer already assigned that module
                cursor.execute('select * from lecturer where module_id=%s',[module_id[0]])
                found = cursor.fetchone()
                if found:
                    flash('Failed because lecturer with that/those modules exists')
                    return redirect('/admin/create/lecturer')

            else:
                flash("Error occured module with that name not found")
                return redirect('/admin/create/lecturer')


        data = list([(user_id[0], x) for x in modules])
        q = "insert into lecturer values(null,%s,%s)"
        cursor.executemany(q, data)
        mysql.connection.commit()

        # insert login details
        username = regno
        password = surname
        role = 'lecturer'


        cursor.execute('insert into login_details values(null,%s,%s,%s,%s)', (user_id[0],username,password,role))
        mysql.connection.commit()
        flash('new user have been added successfully')
        return redirect('/admin/create/lecturer')

    else:
        cursor.execute('select * from module')
        modules = cursor.fetchall()

        cursor.execute('select * from user as u inner join lecturer as l on u.ID=l.user_id group by l.user_id')
        lecturer = cursor.fetchall()
        return render_template('admin/create_lecturer.html', modules=modules, lecturer=lecturer)




@admin.route('/create/programme', methods=['GET','POST'])
def create_programme():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    if request.method== 'POST':
        programme = request.form['programme']
        modules = request.form.getlist('modules')

        # find if user with that programme already exist
        cursor.execute('select * from programme where name=%s', [programme])
        found = cursor.fetchone()
        if found:
            flash('Failed because programme with that name already exists')
            return redirect('/admin/create/programme')

        cursor.execute('insert into programme values(null,%s)', [programme])
        mysql.connection.commit()

        # insert modules in programme_modules table
        # find user id
        cursor.execute('select * from programme order by ID desc limit 1')
        programme_id = cursor.fetchone()

        data = list([(programme_id[0], x) for x in modules])
        q = "insert into programme_modules values(null,%s,%s)"
        cursor.executemany(q, data)
        mysql.connection.commit()
        flash('new programme have been added successfully')
        return redirect('/admin/create/programme')

    else:
        cursor.execute('select * from module')
        modules = cursor.fetchall()
        cursor.execute('select * from programme')
        programme = cursor.fetchall()
        return render_template('admin/create_programme.html', modules=modules, programme=programme)


@admin.route('/create/module', methods=['GET','POST'])
def create_module():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    if request.method== 'POST':
        module = request.form['module']

        # find if user with that programme already exist
        cursor.execute('select * from module where name=%s', [module])
        found = cursor.fetchone()
        if found:
            flash('Failed because module with that name already exists')
            return redirect('/admin/create/module')

        cursor.execute('insert into module values(null,%s)', [module])
        mysql.connection.commit()
        flash('new module have been added successfully')
        return redirect('/admin/create/module')

    else:
        cursor.execute('select * from module')
        modules = cursor.fetchall()
        return render_template('admin/create_module.html', modules=modules)


@admin.route('/read/lecturer/<id>', methods=['GET','POST'])
def read_lecturer(id):
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('select * from lecturer as l inner join module as m on l.module_id=m.ID where l.user_id=%s',[id])
    lecturer = cursor.fetchall()
    return render_template('admin/read_lecturer.html',lecturer=lecturer)


@admin.route('/user/read', methods=['GET','POST'])
def read():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('select * from user')
    user = cursor.fetchall()
    return render_template('admin/read_user.html', user=user)


@admin.route('/read/programme', methods=['GET','POST'])
def read_programme():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('select * from programme')
    programme = cursor.fetchall()
    return render_template('admin/read_programme.html', programme=programme)



@admin.route('/user/update/<id>', methods=['GET','POST'])
def update():
    pass


@admin.route('/delete/module/<id>', methods=['GET','POST'])
def delete_module(id):
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('delete from module where ID=%s', [id])
    mysql.connection.commit()

    # also delete programme module table with this module
    cursor.execute('delete from programme_modules where module_id=%s', [id])
    mysql.connection.commit()
    return redirect('/admin/read/module')


@admin.route('/delete/lecturer/module/<id>', methods=['GET','POST'])
def delete_lecturer_module(id):
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('delete from lecturer where module_id=%s', [id])
    mysql.connection.commit()

    cursor.execute('select * from lecturer as l inner join module as m on l.module_id=m.ID where l.user_id=%s',[id])
    lecturer = cursor.fetchall()
    return render_template('admin/read_lecturer.html', lecturer=lecturer)


@admin.route('/delete/programme/<id>', methods=['GET','POST'])
def delete_programme(id):
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('delete from programme where ID=%s', [id])
    mysql.connection.commit()

    # also delete programme module table with this programme
    cursor.execute('delete from programme_modules where programme_id=%s', [id])
    mysql.connection.commit()
    return redirect('/admin/read/programme')


@admin.route('/delete/user/<id>', methods=['GET','POST'])
def delete_user(id):
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('delete from user where ID=%s', [id])
    mysql.connection.commit()

    # also delete user in login details
    cursor.execute('delete from login_details where user_id=%s', [id])
    mysql.connection.commit()
    return redirect('/admin/user/read')


@admin.route('/profile', methods=['GET','POST'])
def profile():
    if "role" not in session:
        return redirect('/auth/login')
    cursor = mysql.connection.cursor()
    cursor.execute('select * from user where ID=%s', [session['id']])
    user = cursor.fetchone()
    return render_template('admin/profile.html', user=user)
