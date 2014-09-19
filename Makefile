deploy:
	git push heroku master

local_to_heroku_clone:
	heroku pg:transfer --from 'postgres://zinc_saucier:zinc_saucier@localhost/foodb' --to `heroku config:get DATABASE_URL`  --confirm zinc-saucier
