# Proyect 1

## Before starting

### Installation

Run the following commands in your terminal:

```sh
pip install xmpppy
pip install slixmpp
```

### Run

To run the application you need use this command:

```sh
python ./main.py
```

## Description
This project is an implementation of the protocol XMPP using the Slixmpp
library. Using multithreading for the connection to th eserver and few
async. You can send messages, add users to the contact list and much more.
The following list shows the features that were implemented in this project:

## Features
- Show all contacts and check their status
- Add one user to roster
- Show details of a contact
- 1 to 1 messenger
- Group messages
- Change status
- Send notifications
- Receive notifications

# Difficult tasks
The most challanging task was to make all the user flow and the low documentation
of the library. There were a lot of methods that were in the library but in the
web page wasn't. The examples were really basic and you had to guess a lot of params
that the methods recieved.

That's why the the user flow was so hard, there was no documentation in the library
and instead I used another library to create the user, and the rest in slixmpp.

# Learned lessons
The things that I learned in this project where the basic stanzas, and the meaning
of many concepts like JID and roster. The structure of the stanzas for the precense,
messages, MUC and roster. 

The most important leasson of this project is to check different protocols and not
only HTTP, because it's the most popular of them. The protocol is really different
I have worked with JSON requests and responses, but not in XML and it was a really
fun experience.
