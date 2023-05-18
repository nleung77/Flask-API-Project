from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
db = PostgresqlDatabase(‘mlbplayer’, user=‘nelson’, password=‘123456’, host=‘localhost’, port=‘5432’)
class BaseModel(Model):
  class Meta:
    database = db
class MlbPlayer(BaseModel):
  name = CharField()
  age = IntegerField()
  height = CharField()
  position = CharField()
db.connect()
db.drop_tables([MlbPlayer])
db.create_tables([MlbPlayer])
MlbPlayer(name=‘Pete Alonso’, age=‘28’, height=‘6ft 3in’, position=‘First Base’).save()
MlbPlayer(name=‘Fernando Tatis Jr.’, age=‘24’, height=‘6ft 3in’, position=‘Short Stop’).save()
MlbPlayer(name=‘Jose Ramirez’, age=‘30’, height=‘5ft 9in’, position=‘Third Base’).save()
MlbPlayer(name=‘Aaron Judge’, age=‘26’, height=‘6ft 7in’, position=‘Outfield’).save()
app = Flask(__name__)
@app.route(‘/players/’, methods=[‘GET’, ‘POST’])
@app.route(‘/players/<id>’, methods=[‘GET’, ‘PUT’, ‘DELETE’])
def endpoint(id=None):
  if request.method == ‘GET’:
    if id:
        return jsonify(model_to_dict(MlbPlayer.get(MlbPlayer.id == id)))
    else:
        MlbPlayers_list = []
        for player in MlbPlayer.select():
            MlbPlayers_list.append(model_to_dict(player))
        return jsonify(MlbPlayers_list)
  if request.method ==‘PUT’:
    body = request.get_json()
    player.update(body).where(player.id == id).execute()
    return f’{id} has been updated.'
  if request.method == ‘POST’:
    new_player = dict_to_model(player, request.get_json())
    new_player.save()
    return jsonify({“success”: True})
  if request.method == ‘DELETE’:
    player.delete().where(player.id == id).execute()
    return f’{id} deleted.'
app.run(debug=True, port=5000)
