from bottle import route, run


if __name__ == "__main__":

    @route('/add/<first>/<second>', method='GET')
    @route('/<first>/plus/<second>', method='GET')
    def add(first, second):
        try:
            first = int(first)
            second = int(second)
        except:
            return {'success': False}
        return {'success': True, 'result': first + second}


    run(port=8096)

