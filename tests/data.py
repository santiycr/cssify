#!/usr/bin/python

SUPPORTED = [
    ('//a', 'a'),
    ('//a[2]', 'a:nth-of-type(2)'),
    ('/html/body/h1', 'html > body > h1'),
    ('//a[@id="myId"]', 'a#myId'),
    ("//a[@id='myId']", 'a#myId'),
    ('//a[@id="myId"][4]', 'a#myId:nth-of-type(4)'),
    ('//*[@id="myId"]', '#myId'),
    ('id(myId)', '#myId'),
    ('id("myId")/a', '#myId > a'),
    ('//a[@class="myClass"]', 'a.myClass'),
    ('//*[@class="myClass"]', '.myClass'),
    ('//a[@class="multiple classes"]', 'a.multiple.classes'),
    ('//a[@href="bleh"]', 'a[href=bleh]'),
    ('//a[@href="bleh bar"]', 'a[href="bleh bar"]'),
    ('//a[@href="/bleh"]', 'a[href=/bleh]'),
    ('//a[@class="class-bleh"]', 'a.class-bleh'),
    ('//a[.="my text"]', 'a:contains(^my text$)'),
    ('//a[text()="my text"]', 'a:contains(^my text$)'),
    ('//a[contains(@id, "bleh")]', 'a[id*=bleh]'),
    ('//a[contains(text(), "bleh")]', 'a:contains(bleh)'),
    ('//div[@id="myId"]/span[@class="myClass"]//a[contains(text(), "bleh")]//img',
     'div#myId > span.myClass a:contains(bleh) img'),
]

UNSUPPORTED = [
    'fail',
    'a[[]]',
    '(//a)[2]',
]
