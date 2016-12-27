"""pixi Views

"""
from subprocess import Popen, PIPE
import sqlite3
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

DB = 'db.sqlite3'

def migrate():
    """Create a guesses table if it doesn't exist already"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS guesses(id, content)')
    conn.commit()

def count():
    """Return a count of all unique instances in database guesses table"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT COUNT(id) FROM guesses')
    for row in cursor.fetchall():
        count = row
    return count[0]

def write(content):
    """Write image guess content to database"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO guesses(content) VALUES("%s")' % content)
    conn.commit()

def index(request):
    """Process image uploads through Darknet subprocess to return stdout in template"""
    migrate()

    if request.method == 'POST' and request.FILES['image']:
        #setup fs for temp storage of uploaded image
        image = request.FILES['image']
        temp = FileSystemStorage()
        name = temp.save(image.name, image)
        filepath = temp.url(name)
        # run darknet subprocess with given image
        darknet = 'cd darknet && ./darknet classify cfg/tiny.cfg tiny.weights '
        process = Popen(darknet + '../pixi' + filepath, shell=True, stdout=PIPE, stderr=PIPE)
        #store stdout to output array
        output = []
        while True:
            line = process.stdout.readline()
            if line != '':
                output.append(line.rstrip())
            else:
                break
        del output[0]
        # store record and remove uploaded image from temp storage
        write(', '.join(output).strip(':'))
        temp.delete(image.name)
        # render output
        return render(request, 'thanks.html', {
            'output': output,
            'count': count()
        })
    #render index
    return render(request, 'index.html', {'count': count()})
