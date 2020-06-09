import mongoengine as me

me.connect('reviews_bd')


class State(me.Document):
    chat_id = me.IntField(required=True, unique=True)
    state = me.IntField(required=True, default=0)


class Review(me.Document):
    name = me.StringField(min_length=1, max_length=128, required=True)
    last_name = me.StringField(min_length=1, max_length=128, required=True)
    email = me.StringField(min_length=10, max_length=50, required=True)
    phone = me.StringField(min_length=10, max_length=50, required=True)
    review = me.StringField(min_length=2, max_length=4096, required=True)
