from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dummy data to store projects and tasks
projects = []
tasks = {}

# Route for rendering the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.get_json()
    project_name = data.get('name')

    if not project_name:
        return jsonify({'status': 'error', 'message': 'Project name is required'}), 400

    project_id = len(projects) + 1
    projects.append({'id': project_id, 'name': project_name, 'tasks': []})

    return jsonify({'status': 'success', 'message': 'Project created successfully', 'project_id': project_id})

# Route for retrieving all projects
@app.route('/get_projects', methods=['GET'])
def get_projects():
    return jsonify({'status': 'success', 'projects': projects})

# Route for creating a new task within a project
@app.route('/create_task', methods=['POST'])
def create_task():
    data = request.get_json()
    project_id = data.get('project_id')
    task_content = data.get('content')

    if not project_id or not task_content:
        return jsonify({'status': 'error', 'message': 'Project ID and task content are required'}), 400

    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return jsonify({'status': 'error', 'message': 'Project not found'}), 404

    task_id = len(project['tasks']) + 1
    project['tasks'].append({'id': task_id, 'content': task_content})

    return jsonify({'status': 'success', 'message': 'Task created successfully', 'task_id': task_id})

# Route for retrieving all tasks within a project
@app.route('/get_tasks/<int:project_id>', methods=['GET'])
def get_tasks(project_id):
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return jsonify({'status': 'error', 'message': 'Project not found'}), 404

    return jsonify({'status': 'success', 'tasks': project['tasks']})

# Route for updating a task
@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    new_content = data.get('content')

    if not new_content:
        return jsonify({'status': 'error', 'message': 'New task content is required'}), 400

    for project in projects:
        for task in project['tasks']:
            if task['id'] == task_id:
                task['content'] = new_content
                return jsonify({'status': 'success', 'message': 'Task updated successfully'})

    return jsonify({'status': 'error', 'message': 'Task not found'}), 404

# Route for deleting a task
@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for project in projects:
        for task in project['tasks']:
            if task['id'] == task_id:
                project['tasks'].remove(task)
                return jsonify({'status': 'success', 'message': 'Task deleted successfully'})

    return jsonify({'status': 'error', 'message': 'Task not found'}), 404

# Route for deleting a project
@app.route('/delete_project/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return jsonify({'status': 'error', 'message': 'Project not found'}), 404

    projects.remove(project)
    return jsonify({'status': 'success', 'message': 'Project deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
