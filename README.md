# `intakt`: D-guild's tool for creating intäktsräknignar 
`intakt` is a tool to generate intäktsräkningar from the sales of Zettle and Swish. 

This project were started in 2021 by the treasurer of the time, Joel Bäcker, and has been updated during 2022 by the same person. 
For the time beeing it is only available in terminal form, and some credentials are needed to create intäktsräkningar.

The work is currently focused on connecting the front end to the backend as well as reformating the code.
If you want to contribute, get in contact with Joel Bäcker.

# How to use

There is two ways the program can be ran.
## Terminal

The terminal bassed approach works a bit diffrently whether you want a Zettle or a Swish report.

You need to choose which source to retrieve the data from using `-s` or `--source`.

### Zettle 

#### Set up credentials

To use the Zettle API you need an API key

[Click this link to create a key](https://my.zettle.com/apps/api-keys?scopes=READ:PURCHASE)

The client id and key should be put in the file `main/credentials/access.json` (create the credentials folder if it doesn't exist) and should look like this:
```json
{
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "client_id": "<CLIENT_ID>",
    "assertion": "<API KEY>"
}
```

#### Use the program

The available option for the Zettle parser is:
- `-sd` / `--start-date`
- `-ed` / `--end-date`

If end date is left empty then is will produce a report until the current day, start day is not optional.

To use the parser:

Ex. 1:
```
./main/main.py -s "zettle" -sd 2022-06-01 -ed 2022-08-30
```

Ex. 2:
```
./main/main.py --start-date 2022-04-04 --end-date 2022-05-04
```

### Swish

Swish is used  in a similar manor.
The available arguments are:
- `-inp` / `--input-fp`

To use the swish parser:

Ex. 1

```
./main/main.py --source "swish" -inp swish/jan_aug.csv
```

## Front end

To start the web page you need to run 

```
make webpage
```

or 

```
python3 webpage/index.py
```

in the top folder of this project. 
This page is then ran on `localhost:1999`.

This page is currently not connected to the backend, but you can look at it and admire a beautiful web page #komochkodamedDWWW. 
