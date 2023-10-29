[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/qg4qXfSB)

## Asynchronous Concurrent Messaging System with Multithreaded Database Interaction

## Description: 

The "Asynchronous Concurrent Messaging System" is a robust and scalable software solution designed for asynchronous communication across multiple PostgreSQL database servers. The system allows users to send and receive messages concurrently, providing real-time messaging capabilities.

## Guide:

Python is cross-platform programming language, and code itself checked in case of any portability issues. Code should work on most of the operating systems like macOS and Linux in the same way. 

```diff 
+ How to install? 
```

To run the application, you need to have python installed on your computer (latest versions reccommended, like python3.11). You can install it from here. https://www.python.org/downloads/

Install project's repository (ex. in zip format) from github. You can use this link:  https://github.com/ADA-GWU/processes-and-asynchronous-messaging-aliamrahli
(click green "code" button and download zip)

```diff 
+ How to compile?
```
- First, you need to be sure that you have the required setup. This system uses the psycopg2 package to interact with PostgreSQL databases. Install it using pip, the Python package manager, by running the following command in your terminal or command prompt:
pip install psycopg2

- Modify the db_ips list in the sender and reader scripts to include the IP addresses or hostnames of your PostgreSQL database servers.

Open 2 different terminal windows, and navigate to the folder's location. Run the reader_software and sender_software using python with following commands:

python sender_software.py
python reader_software.py

```diff 
+ How to run?
```

Enter messages in the sender script to see them processed by the reader script. The system will handle asynchronous messaging using the PostgreSQL database.
