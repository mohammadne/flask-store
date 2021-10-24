from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


class Item:
    def __init__(self, name, price) -> None:
        self.name = name
        self.price = price

    def toJSON(self):
        return {
            'name': self.name,
            'price': self.price,
        }


class Store:
    def __init__(self, name, items) -> None:
        self.name = name
        self.items = items

    def toJSON(self):
        return {
            'name': self.name,
            'items': list(map(lambda x: x.toJSON(), self.items)),
        }


stores = [
    Store(
        'wonderful-store',
        [
            Item('my-item', 15.99),
        ],
    ),
]


def jsonify_stores() -> map:
    result = map(lambda x: x.toJSON(), stores)
    return jsonify({'stores': list(result)})


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/store')
def get_stores():
    return jsonify_stores()


@app.route('/store', methods=['POST'])
def create_store():
    data = request.get_json()
    store = Store(data['name'], [])
    stores.append(store)
    return jsonify_stores()


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store.name == name:
            return store.toJSON()
    return jsonify({'message': 'not found'})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    for store in stores:
        if store.name == name:
            data = request.get_json()
            item = Item(data['name'], data['price'])
            store.items.append(item)
            return store.toJSON()

    return jsonify({'message': 'not found'})


@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store.name == name:
            result = map(lambda x: x.toJSON(), store.items)
            return jsonify({'items': list(result)})
    return jsonify({'message': 'not found'})


app.run(port=8080)
