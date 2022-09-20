from flask import Flask, Response, request,render_template,redirect
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 3000
    )
    db = mongo.database
      
    mongo.server_info()
except:
    print("Error - Cannot connect to Database")


@app.route('/api/test')
def Test():
    return render_template('about.html')


@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/api/')
def BackHome():
    return render_template('index.html')

@app.route('/api/bytitle')
def ByTitle():
    return render_template('get_film_title.html')

@app.route('/api/byactor')
def ByActor():
    return render_template('get_film_actor.html')

@app.route('/api/create', methods=['GET','POST'])
def create_film():
    try:
        if request.method == 'GET':
            return render_template('create_film.html')
 
        if request.method == 'POST':
            film_data = {
                "id":request.form["id"],
                "title":request.form["title"],
                "type":str(request.form["type"].split(",")),
                "description":request.form["description"],
                "release_year":request.form["release_year"],
                "age_certification":request.form["age_certification"],
                "runtime":request.form["runtime"],
                "genres":request.form["genres"],
                "production_countries":request.form["production_countries"],
                "imdb_score":request.form["imdb_score"]
            }

            dbResponse = db.netflix.insert_one(film_data)
            
            return redirect("/")
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps(
                {
                    "message":"Film insertion failed"
                    }
            ),
            status = 500,
            mimetype = "application/json"
        )



@app.route('/api/update', methods=['POST'])
def update_film():
    try:
        film_data = {
            "id":request.form["id"],
            "title":request.form["title"],
            "type":str(request.form["type"].split(",")),
            "description":request.form["description"],
            "release_year":request.form["release_year"],
            "age_certification":request.form["age_certification"],
            "runtime":request.form["runtime"],
            "genres":request.form["genres"],
            "production_countries":request.form["production_countries"],
            "imdb_score":request.form["imdb_score"]
        }
        print(film_data)
        dbResponse = db.netflix.update_one(
            {"title":film_data["title"]},
            {"$set":film_data}
        )
        
        return redirect("/")
    except Exception as ex:
        return Response(
            response = json.dumps(
                {
                    "message":"Film updation failed"
                }
            ),
            status = 500,
            mimetype = "application/json"
        )

       

@app.route('/api/delete/<string:fname>')
def delete_film(fname):
    try:

        dbResponse = db.netflix.delete_one({"title":fname})
        
        if dbResponse.deleted_count == 1:

            return redirect("/")

    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps(
                {
                    "message":"Film updation failed"
                }
            ),
            status = 500,
            mimetype = "application/json"
        )



@app.route('/api/getall', methods=['GET'])
def get_films():
    try:
        data= list(db.netflix.find())
        for res in data:
            res["_id"] = str(res["_id"])
        return render_template('all_data.html',data = data)

    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps(
                {
                    "message":"Cannot get movie details"
                }
            ),
            status = 500,
            mimetype = "application/json"
        )



@app.route('/api/getbytitle', methods=['POST'])
def get_film_by_title():
    try:
        data= db.netflix.find_one({"title": request.form["title"]})
        data["_id"] = str(data["_id"])
        
        return render_template('data.html',data = data)

    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps(
                {
                    "message":"Cannot get film details"
                }
            ),
            status = 500,
            mimetype = "application/json"
        )




@app.route('/api/<string:id>/edit', methods=['GET'])
def get_film_by_id(id):
    try:
        data= db.netflix.find_one({"_id":ObjectId(id)})
        data["_id"] = str(data["_id"])
        data["title"] = data["title"]
        data["description"] = data["description"]
        data["imdb_score"] = data["imdb_score"]
        return render_template('update.html',data = data)

    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps(
                {
                    "message":"Cannot get film details"
                }
            ),
            status = 500,
            mimetype = "application/json"
        )



@app.route('/api/getbyactor', methods=['POST'])
def get_film_by_actor():
    try:
        fname = request.form["actor"]
        data= list(db.netflix.find({"list_actors": {"$regex": fname}}))
        for res in data:
            res["_id"] = str(res["_id"])
    
        return render_template('datalist.html',data = data)

   
    except Exception as ex:
        return Response(
            response = json.dumps(
                {
                    "message":"Cannot get film details"
                }
            ),
            status = 500,
            mimetype = "application/json"
        )



if __name__ == "__main__":
    app.run(host="localhost",port=5000,debug=True)  