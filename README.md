# IdleBot
Discord Bot That Joins And Leaves Voice Channels
- Join Calls
- Leave Calls

# Set Up + Self Hosting
## Oracle Cloud Free Tier
https://www.oracle.com/cloud/

## Bitvise SSH Client
https://bitvise.com/ssh-client-download

## Discord Developer 
https://discord.com/developers/applications


## Unclear Unorganized Instructions 
1. [Discord Developer] Create New Discord Application Through Discord Developer & Retrieve Bot Token 
2. [Bitvise SSH Client] Download Bitvise SSH Client
3. [Oracle Cloud] Sign Up For Oracle Cloud & Create An Ubuntu Instance (Using 1 Of 2 Oracle Cloud Free Tier)
4. [Oracle Cloud -> Bitvise SSH Client] Start The Instance & Connect Through Bitvise SSH Client Via The Oracle Instance's Public IP Address, Client Key,
5. [Bitvise SSH Client] Client Key Manager -> Import -> convertedkey.ppk
6. [Bitvise SSH Client] Host: Public IP Address / Port: 22 / Username: ubuntu / Initial Method: publickey / Client Key: Global 1 
7. [Bitvise SSH Client] Log In -> New Terminal Console + New SFTP Window
8. [Bitvise SFTP] Import Files Into Remote Files & Edit .env To Include DISCORD BOT TOKEN
9. [Bitvise Terminal] Install All Required Packages & Resources -> Test If bot.py Works -> Make bot.py Run Forever
10. Done! 

