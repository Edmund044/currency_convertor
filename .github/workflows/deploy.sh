 #!/bin/sh
ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p $SSH_PORT -i ~/.ssh/id_rsa $SSH_USER@$HOST << EOF
    cd /var/www/html/currency_convertor
    git stash
    git pull origin develop 
    pip3 install -r requirements.txt
EOF