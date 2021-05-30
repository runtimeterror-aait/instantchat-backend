from flask_restful import Resource, abort, reqparse

TODO = {
    1 : "Hello, world",
    2 : "Another One",
    3 : "one two" 
}

parser = reqparse.RequestParser()
parser.add_argument('task')


class Todo(Resource):
    def get(self, id):
        if id not in TODO.keys():
            abort(404, message="Todo {} doesn't exist".format(todo_id))
        else:
            return Todo[id]
    def delete(self, todo_id):
        del TODO[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()

        task = {'task': args['task']}
        TODO[todo_id] = task
        return task, 201

class TodoList(Resource):
    def get(self):
        return TODO

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODO.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODO[todo_id] = {'task': args['task']}
        return TODO[todo_id], 201