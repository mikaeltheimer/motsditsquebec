from django.shortcuts import render


def defaultview(request, template):
    '''Simply renders the supplied template'''
    reviews = [
        ('hownowstephen', 'This is a great review that spans over multiple lines because I am awesome and great at writing nice long reviews that look great. If you were to ask me just how long this review can get, I would probably tell you that it can get pretty long, because that would be the truth. And I would ramble on and on about how long the review gets, and you would probably be bored to tears, but this is all just to see what the review looks like in longform, so who cares. Just for the fun of it, might as well see what happens if i add in yet another couple of lines, should give me a quick idea of what happens to the image on the left..'),
        ('HugoDubs', 'This review is by Hugo and he did not have much to say'),
        ('MikaelTheimer', 'Mikael has more to say than Hugo, but less that Stephen. Mostly because I want to see how the interplay between the different stylings of reviews goes down. Hopefully it looks nice!')
    ]

    mots = [
        ('Cronuts', 'cronut.jpeg'),
        ('Habitation 69', 'habitation.jpeg'),
        ('Just for Laughs', 'justforlaughs.jpg'),
        ('St Lawrence Cruises', 'cruise.jpeg'),
        ('Hotel De Ville', 'hoteldeville.jpeg'),
        ('The Metro', 'metro.jpg'),
        ('Biosphere', 'biosphere.jpeg'),
        ('Downtown', 'downtown-montreal.jpg'),
    ]

    return render(request, '{}.html'.format(template), {'reviews': reviews, 'mots': mots})
