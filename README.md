# What is this repo about?
This is custom fork of the original python mirror bot with custom added mirrors. 

Follow the instructions on the main repo to deploy.

# Added or changed features
## Change upload location
- Change folder id of gdrive for upload location temporarily until restart.

Usage: `/changeroot <googledrive_folder_id>`
 
## mirror_many
- Added mirroring multiple links in one command using default settings

Usage: `/mirror_many <single|batch> <link1,link2,link3>`

`single: add as as each individual task`

`batch: add all links as one task`
 
## XDCC
- Added downloading from xdcc

Usage: `/xdcc [server[:port]],]<channel> /msg <bot> xdcc <send|batch> <1|1-5>`

Eg: `/xdcc irc.xertion.org,MK /msg Rory|XDCC xdcc send #22969`

Default server is `irc.rizon.net`

## Onedrive
- Added recursive downloading from given url for certain onedrive indexes
- Currently supported mirrors - (Can't find github page for it)

##### To Do
```
- [ ] Add support more indexes
- [ ] Add proper help
- [ ] Add proper error handling
```

## Fembed
- Added downloading from fembed-like websites - https://fembed.com/
