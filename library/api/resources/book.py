from flask_restful import Resource, reqparse, request


parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted', location="path")
parser.add_argument('name')
# args = parser.parse_args()

class Book(Resource):
    def get(self, book_id):
        print(dir(request))
        # return {"title": "myTitle",
        #         "author_name": "",
        #         "author_surname": "",
        #         "publisher": "",
        #         "year_published": "",
        #         "amount": ""
        #         }

    def post(self):
        pass