from flask import Flask, g, current_app
app = Flask(__name__)

#nested wrong way
# with app.app_context():
#     print('in app context, before first request context')
#     print('setting g.foo to abc')
#     g.foo = 'abc'
#     print('g.foo should be abc, is: {0}'.format(g.foo))

#     with app.test_request_context():
#         # this reuses g from the current context
#         print('in first request context')
#         print('g.foo should be abc, is: {0}'.format(g.foo))
#         print('setting g.foo to xyz')
#         # this is the same g, so it will be replaced
#         g.foo = 'xyz'
#         print('g.foo should be xyz, is: {0}'.format(g.foo))

#     print('in app context, after first request context')
#     print('g.foo should be abc, is: {0}'.format(g.foo))

#     with app.test_request_context():
#         print('in second request context')
#         print('g.foo should be abc, is: {0}'.format(g.foo))
#         print('setting g.foo to pqr')
#         g.foo = 'pqr'
#         print('g.foo should be pqr, is: {0}'.format(g.foo))

#     print('in app context, after second request context')
#     print('g.foo should be abc, is: {0}'.format(g.foo))
    
    
    


with app.app_context():
    print('in app context, before first request context')
    print('setting g.foo to abc')
    g.foo = 'abc'
    print('g.foo should be abc, is: {0}'.format(g.foo))
    current_app.config['foo'] = 'abc'
    print(current_app.name)

with app.test_request_context():
    print('in first request context')
    print('g.foo should be None, is: {0}'.format(g.get('foo')))
    print('setting g.foo to xyz')
    g.foo = 'xyz'
    print('g.foo should be xyz, is: {0}'.format(g.foo))
    print(current_app.config.get('foo'))

with app.test_request_context():
    print('in second request context')
    print('g.foo should be None, is: {0}'.format(g.get('foo')))
    print('setting g.foo to pqr')
    g.foo = 'pqr'
    print('g.foo should be pqr, is: {0}'.format(g.foo))
    print(current_app.config.get('foo'))
