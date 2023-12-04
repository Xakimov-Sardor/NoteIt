from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from .models import Wall, db, Note


views = Blueprint('views', __name__)

@views.route('/')
# @login_required
def home():
    return render_template('home.html', c_user=current_user)

@views.route('/clear')
@login_required
def clear():
    return redirect(url_for('views.home'))

@views.route('/wall/create', methods=['POST', 'GET'])
@login_required
def create_wall():
    if request.method == 'POST':
        name = request.form.get('name')
        
        if len(name) >= 2:

            new_wall = Wall(name=name, user_id=current_user.id)
            db.session.add(new_wall)
            db.session.commit()

            flash('New wall created', category='ok')
            return redirect(url_for('views.home'))
        else:flash('Please longer')

        


    return render_template('create_wall.html', c_user=current_user)


@views.route('/wall/view/<id>')
@login_required
def wall_view(id):
    wall = Wall.query.filter_by(id=id, user_id=current_user.id).first()
    if wall:

        return render_template('wall_view.html', wall=wall, c_user=current_user)
    else:
        flash('Wall not found', category='error')
        return redirect(url_for('views.home'))


@views.route('/wall/update/<wall_id>', methods=['POST', 'GET'])
@login_required
def update_wall(wall_id):
        wall = Wall.query.filter_by(id=wall_id, user_id=current_user.id).first()
        if request.method == 'POST':
            
            if wall:
                new_name = request.form.get('name')

                if len(new_name) >= 2:
                    wall.name = new_name

                
                    db.session.commit()

                    db.session.refresh(wall)


                    return redirect(url_for('views.wall_view', id=wall.id))
                else:
                    flash('Please longer', category='error')
    

        return render_template('update_wall.html', c_user=current_user, wall=wall)

@views.route('/wall/delete/<wall_id>')
@login_required
def delete_wall(wall_id):

    wall = Wall.query.filter_by(id=wall_id, user_id=current_user.id).first()
    
    if wall:
        for note in wall.notes:
            note = Note.query.filter_by(wall_id=wall_id).first()
            db.session.delete(note)

        db.session.delete(wall)
        db.session.commit()

        flash('Wall deleted', category='ok')
    else:
        flash('Wall does not exist')

    return redirect(url_for('views.home'))

@views.route('/wall/clear/<wall_id>')
@login_required
def clear_wall(wall_id):
    wall = Wall.query.filter_by(id=wall_id, user_id=current_user.id).first()

    if wall:
        for note in wall.notes:
            note = Note.query.filter_by(wall_id=wall_id).first()
            db.session.delete(note)
        
        db.session.commit()



    return redirect(url_for('views.wall_view', id=wall_id))

@views.route('/note/<wall_id>/create', methods=['POST', 'GET'])
@login_required
def create_note(wall_id):
    if  request.method == 'POST':
        wall = Wall.query.filter_by(id=wall_id, user_id=current_user.id).first()

        if wall:
            title = request.form.get('title')
            text = request.form.get('text')

            if len(title) >= 2 and len(text) > 5:
                note = Note(title=title, text=text, wall_id=wall_id)
                db.session.add(note)
                db.session.commit()

                return redirect(url_for('views.wall_view', id=wall_id))

            else:
                flash('Fill out the form sufficiently', category='error')
        else:
            flash('Wall not found', category='error')
    return render_template('create_note.html', c_user=current_user)

@views.route('/note/<wall_id>/update/<note_id>', methods=['POST', 'GET'])
@login_required
def update_note(wall_id, note_id):

    note = Note.query.filter_by(wall_id=wall_id, id=note_id).first()

    if request.method == 'POST':
        if note:
            title = request.form.get('title')
            text = request.form.get('text')

            if len(title) > 2 and len(text) > 5:
                note.title = title
                note.text = text

                db.session.commit()

                db.session.refresh()

                return redirect(url_for('views.wall_view', id=wall_id))
            else:
                flash('Please longer', category='error')


    return render_template('update_note.html')

@views.route('/note/<wall_id>/delete/<note_id>')
@login_required
def delete_note(wall_id, note_id):
    return redirect(url_for('views.home'))

@views.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@views.route('/delete_user')
@login_required
def delete_user():
    return render_template('delete_user')