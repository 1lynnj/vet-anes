# Veterinary Anesthesia Protocol BACKEND

A web application to reduce drug calculation errors with veterinary anesthetic protocols. 

Popular tools currently in use:
- blank forms where medical staff manually write in and calculate drug dosages using a calculator
- excel spreadsheets where some calculations can be automated but are prone to user error through spreadsheet interference 

The app goes further by pulling drug interactions from the National Institutes of Health drug interactions API to warn the anesthetist of possible drug interactions. Includes all drugs administered within 12 hours of the anesthetic event and are present in the NIH Database.

## Features

- Allows custom protocols for cats and dogs by entering each required drug and the required dose individually. 
 - Auto populates protocols for healthy cats and dogs with the click of a button.
 - Drug Interactions check from the National Institutes Of Health drug interactions API.
 - Calculates drug dosages for anesthesia, Fentanyl (pain) continuous rate infusion, fluid rates, and emergency drugs.

## Setup and Dependencies

**Create project directory**
```
mkdir <projectname>
cd <projectname>
```




## Frontend

This app uses a postgreSQL database of a limited number of drugs with a backend written in Django.

[Veterinary Anesthesia Protocol - Frontend](https://github.com/1lynnj/vet-anes.git)
  
## Future Versions

- Ability by user to add standard protocols to autopopulate form.
- Ability by user to store protocols for individual patients to recall for reference or usage at a later time.
- Ability by user to add drugs to the database.
- User login and authentication to allow above actions.
- Printable document with generated protocol and monitoring grid for use by anesthetist on the medical floor.