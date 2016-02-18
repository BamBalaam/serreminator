all: dev prod

prod: static/app.min.js
dev: static/app.js static/dev.html

COMPILER = node_modules/browserify/bin/cmd.js
COMPILE_DEV = --debug -g reactify
COMPILE_PROD = -g reactify -g uglifyify

components/${COMPILER}:
	cd components && npm install

static/%.js: components/%.js components/${COMPILER} components/*.js
	cd components && ${COMPILER} ${COMPILE_DEV} -o ../$@ ../$<

static/%.min.js: components/%.js components/${COMPILER} components/*.js
	cd components && ${COMPILER} ${COMPILE_PROD} -o ../$@ ../$<

static/dev.html: static/index.html
	sed -E 's/"(.+)\.min\.(js|css)"/"\1.\2"/g' < $< > $@

clean:
	rm -f static/app.min.js static/app.js static/dev.html

mrproper: clean
	rm -rf components/node_modules
