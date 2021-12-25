from app_core import *
from application.models import *
import datetime as dt

i=0

@app.route('/', methods= ['POST','GET'])
def user():
  session["warning"] = ""
  if request.method == 'GET':
    if "username" not in session:
      return render_template("login.html",trig='')
    else:
      return redirect(url_for('dashboard',username = session["username"]))
  elif request.method == 'POST':
    try:
      userid = request.form['ID']
      pwd = request.form['Password']
      cur_user = User.query.filter_by(username=userid).first()
      if pwd == cur_user.password:
        session['username'] = cur_user.username
        session['name'] = cur_user.name
        session['warning'] = ""
        return redirect(url_for('dashboard',username = session["username"]))
      else:
        return render_template("login.html",trig='Wrong Password')
    except Exception as exception:
      return render_template("login.html",trig='Wrong User ID')

@app.route('/<username>')
def dashboard(username):
  if "username" not in session or session["username"] != username:
    return redirect(url_for('user'))
  else:
    decks = Deck.query.filter_by(username=session["username"])
    return render_template("dashboard.html",decks = decks,i=1)

@app.route('/newdeck', methods= ['POST'])
def new_deck():
  if request.method == 'POST':
    try:
      deckname = request.form['DeckName']
      new_deck = Deck(deck_name=deckname,username=session["username"])
      db.session.add(new_deck)
      db.session.commit()
      session["warning"] = ""
      return redirect(url_for('dashboard',username = session["username"]))
    except:
      session["warning"] = "Deck exists!"
      return redirect(url_for('dashboard',username = session["username"]))

@app.route('/newuser', methods= ['POST','GET'])
def new_user():
  if request.method == 'GET':
    session["warning"] = ""
    return render_template("new_user.html")
  elif request.method == 'POST':
    try:
      new_user = User(username = request.form['ID'],password = request.form['Password'],name = request.form['Name'])
      db.session.add(new_user)
      db.session.commit()
      session["warning"] = "Submitted!"
    except:
      session["warning"] = type(exception).__name__
    finally:
      return render_template("new_user.html")
      conn.close()

@app.route('/<username>/<deckname>')
def deck_view(username,deckname):
  if ("username" not in session or session["username"] != username) or (deckname not in [d.deck_name for d in Deck.query.filter_by(username=session["username"])]):
    session["warning"] = "Deck not found!"
    return redirect(url_for('user'))
  else:
    cards = Card.query.filter_by(deck_id = Deck.query.filter_by(deck_name = deckname,username=session["username"]).first().deck_id)
    session["num"] = 0
    return render_template("dash_deck.html",deckname=deckname,cards = cards)

@app.route('/<username>/<deckname>/newcard', methods= ['POST'])
def new_card(username,deckname):
  if request.method == 'POST':
    try:
      front = request.form['Front']
      back = request.form['Back']
      D = Deck.query.filter_by(deck_name = deckname,username=session["username"]).first()
      new_card = Card(front=front,back=back,deck_id=D.deck_id)
      D.num_of_cards += 1
      db.session.add(new_card)
      db.session.add(D)
      db.session.commit()
      session["warning"] = ""
      return redirect(url_for('deck_view',username = session["username"],deckname=deckname))
    except:
      session["warning"] = "Card exists!"
      return redirect(url_for('deck_view',username = session["username"],deckname=deckname))

@app.route('/<username>/<deckname>/deletedeck')
def del_deck(username,deckname):
  if ("username" not in session or session["username"] != username) or (deckname not in [d.deck_name for d in Deck.query.filter_by(username=session["username"])]):
    session["warning"] = "Deck not found!"
    return redirect(url_for('user'))
  else:
    cards = Card.query.filter_by(deck_id = Deck.query.filter_by(deck_name = deckname,username=session["username"]).first().deck_id)
    for c in cards:
      db.session.delete(c)
    deck = Deck.query.filter_by(deck_name = deckname,username=session["username"]).first()
    db.session.delete(deck)
    db.session.commit()
    session["warning"] = "Deck %s deleted!" % deckname
    return redirect(url_for('user'))

@app.route('/<username>/<deckname>/<crd>/delete')
def del_card(username,deckname,crd):
  if ("username" not in session or session["username"] != username) or (deckname not in [d.deck_name for d in Deck.query.filter_by(username=session["username"])]) or (int(crd) not in [c.card_id for c in Card.query.filter_by(deck_id = Deck.query.filter_by(deck_name = deckname,username=session["username"]).first().deck_id)]):
    session["warning"] = [c.card_id for c in Card.query.filter_by(deck_id = Deck.query.filter_by(deck_name = deckname,username=session["username"]).first().deck_id)]
    return redirect(url_for('deck_view',username = session["username"],deckname=deckname))
  else:
    card = Card.query.filter_by(card_id=crd).first()
    db.session.delete(card)
    db.session.commit()
    session["warning"] = "Card %s deleted!" % card.front
    return redirect(url_for('deck_view',username = session['username'],deckname=deckname))

def rand_card(username,deckname):
  crds = [c for c in Card.query.filter_by(deck_id = Deck.query.filter_by(deck_name = deckname,username=session["username"]).first().deck_id)]
  n = 10 if len(crds)>10 else len(crds)
  cards = random.sample(crds,n)
  return cards

@app.route('/<username>/<deckname>/review',methods=['POST','GET'])
def review(username,deckname):
  cards = rand_card(username,deckname)
  session["deck"] = deckname
  fronts = [c.front for c in cards]
  backs = [c.back for c in cards]
  return render_template("review.html",fronts=fronts,backs=backs,deckname=deckname)

@app.route('/<username>/<deckname>/processing',methods=['POST','GET'])
def processing(username,deckname):
  D = Deck.query.filter_by(deck_name = deckname,username=session["username"]).first()
  D.last_score = request.form['finscore']
  if D.last_date == None:
    D.average_score = float(D.last_score)
  else:
    D.average_score = (D.average_score + float(D.last_score))/2
  D.last_date = dt.datetime.now()
  db.session.add(D)
  db.session.commit()
  return redirect(url_for('deck_view',username = session["username"],deckname=deckname))

@app.route('/logout')
def log_out():
  session.pop('username',None)
  return redirect(url_for('user'))