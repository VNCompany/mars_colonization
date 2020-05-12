import flask
from flask import jsonify, request
from data.db_session import create_session
from data.jobs import Jobs


bp = flask.Blueprint("jobs_api", __name__, template_folder="templates")


@bp.route("/api/jobs")
def get_jobs():
    session = create_session()
    jobs = session.query(Jobs).all()
    return jsonify({
        "jobs": [job.to_dict(only=[
                "id", "team_leader", "job", "work_size",
                "collaborators", "start_date", "end_date",
                "is_finished"]) for job in jobs]
    })


@bp.route("/api/jobs/<int:job_id>")
def get_job(job_id: int):
    session = create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({
            "error": "Job not found"
        })
    else:
        return jsonify({
            "job": job.to_dict(only=[
                "id", "team_leader", "job", "work_size",
                "collaborators", "start_date", "end_date",
                "is_finished"])
        })


@bp.route("/api/jobs", methods=['POST'])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = create_session()
    if session.query(Jobs).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished']
    )
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})


@bp.route("/api/jobs/<int:job_id>", methods=['DELETE'])
def delete_job(job_id: int):
    session = create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@bp.route("/api/jobs/edit/<int:job_id>", methods=['POST'])
def edit_job(job_id: int):
    valid = ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id)
    if not job.first():
        return jsonify({'error': 'Not found'})
    edits = {}
    for j in request.json:
        if j in valid:
            edits[j] = request.json[j]
    job.update(edits)
    session.commit()
    return jsonify({'success': 'OK'})
