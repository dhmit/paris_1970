# Renews our Let's Encrypt issued certs via Certbot
# Run via sudo's crontab on Sundays at 7 UTC
# See docs at https://certbot.eff.org/ if any problems

# Needs to bind to port 80 to verify our ownership of the server, which is why
# we take down the server temporarily.

date
service nginx stop
certbot certonly --standalone --preferred-challenges http -d www.REPO_NAME --force-renewal
certbot certonly --standalone --preferred-challenges http -d REPO_NAME --force-renewal
service nginx start
