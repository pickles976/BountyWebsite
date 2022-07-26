
# Foxhole Bounties

This is a website used for creating Bounties in Foxhole

## What is a Bounty?

A Bounty is just a cool-sounding name for a task you need done in game. Maybe a mine needs to be refueled, or a base needs to be satcheled, or a canyon pass reinforced. If you dont have access to a clan, you can post a Bounty here, and other players can accept it and complete it for points!

## Why not just use Sigil?

A few wars back (90) it was determined that a big weakness of Colonials was being unable to coordinate new players. For Wardens, new players are quickly snatched up by clans. For Colonials new players often go without instruction or direction, only to be fed to massive meat grinder battles with a pistol (and maybe an Argenti). Gamifying in-game tasks through a third-party application with a search function might make it easier for noobs or solo players to find meaningful ways to contribute.

## How do we know this website is safe?

For now only Colonials are able to access the website. I plan to add Warden support but they dont yet have a third-party verification API set up. First the app uses OAuth with Discord to link your Discord name to the app. Then it uses an API endpoint to check your verification status in Sigil. The app mass-unverifies everyone at the start of a new war. Once verified, Colonials can only view posts made my Colonials, and Wardens can only view posts made by Wardens. Unverified users can do neither.

## What do points do?

Nothing!



# Important Commands

Checks for a new war  

    python manage.py check_war_status

Sends a discord message to all users with recent relevant activity

    python manage.py send_messages

This will migrate the db and load fixtures. Good for a database reset in development  

    python manage.py makemigrations users  
    python manage.py makemigrations bounty  
    python manage.py migrate  
    python manage.py loaddata .\bounty\fixtures\teams.json  
    python manage.py loaddata .\bounty\fixtures\wars.json  

Bot permissions link: 

    https://discord.com/oauth2/authorize?client_id=1000844725445726270&scope=bot&permissions=0