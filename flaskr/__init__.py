# import os

from flask import Flask, redirect, url_for, request, render_template
# from flask_sqlalchemy import SQLAlchemy
import random
from functools import reduce

OP_MAP = [' => ', ' -> ']

def collatz_create_seq(n):
    l = 0
    seq = []
    ops = []
    max_n = n
    while n > 1:
        ops.append(n % 2)
        n = 3 * n + 1 if n % 2 else n // 2

        l += 1
        seq.append(n)
        max_n = max(max_n, n)
    return (l, seq, ops, max_n)

def collatz_str(n, seq, ops):
    seq_max = max(seq)

    def rf(xs):
        (n, op) = xs
        return (OP_MAP[op]) + str(n)

    # return ' -> '.join((map(lambda n: f'{n}' if n == seq_max else f'{n}', seq)))
    return str(n) + reduce(lambda r, xs: r + rf(xs), zip(seq, ops), str())

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # app.secret_key = "dev"
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost:5432/collatz.sqlite3"
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # db = SQLAlchemy(app)
    # class collatz_seq(db.Model):
    #     n = db.Column(db.Integer, primary_key=True)
    #     seq = db.Column()
    #     max_n = db.Column(db.Integer)

    #     def __init__(self, n, max_n):
    #         self.n = n
    #         self.max_n = max_n

    # db.create_all()

    @app.route('/')
    @app.route('/collatz', strict_slashes=False)
    def index():
        r = random.randint(1, 1000)
        return redirect(url_for('collatz', n=r))

    @app.route('/collatz/<int:n>')
    def collatz(n):
        (l, seq, ops, max_n) = collatz_create_seq(n)
        # db.session.add(collatz_seq(n, max_n))
        # db.session.commit()


        seq_str = collatz_str(n, seq, ops)
        return render_template('collatz.html', n=n, len=l, seq=seq_str, max_n=max_n, op_map=OP_MAP)

    return app