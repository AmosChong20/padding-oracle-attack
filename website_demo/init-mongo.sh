#!/bin/bash
set -e

mongosh -u root -p admin <<EOF
use website_demo

db.createUser(
  {
    user: 'user',
    pwd: 'password',
    roles: [
      {
        role: 'readWrite',
        db: 'website_demo'
      }
    ]
  }
)

db.createCollection('users')
EOF

echo "MongoDB setup complete"