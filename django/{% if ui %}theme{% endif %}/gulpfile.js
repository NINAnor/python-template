/*
=========================================================
* Volt Free - Bootstrap 5 Dashboard
=========================================================
* Product Page: https://themesberg.com/product/admin-dashboard/volt-premium-bootstrap-5-dashboard
* Copyright 2020 Themesberg (https://www.themesberg.com)
* License (https://themesberg.com/licensing)
* Designed and coded by https://themesberg.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Please contact us to request a removal.
*/

var autoprefixer = require('gulp-autoprefixer');
var browserSync = require('browser-sync').create();
var cleanCss = require('gulp-clean-css');
var gulp = require('gulp');
const npmDist = require('gulp-npm-dist');
var sass = require('gulp-sass')(require('sass'));
var wait = require('gulp-wait');
var sourcemaps = require('gulp-sourcemaps');

// Define paths

const paths = {
    dist: {
        base: './static/',
        css: './static/css',
        js: './static/js',
        img: './static/images',
        vendor: './static/vendor',
    },
    base: {
        base: './',
        node: './node_modules'
    },
    src: {
        base: './src/',
        js: './src/js/*.*',
        scss: './src/sass',
        node_modules: './node_modules/',
    }
};

// Compile SCSS
gulp.task('scss', function () {
    return gulp.src([paths.src.scss + '/custom/**/*.scss', paths.src.scss + '/volt/**/*.scss', paths.src.scss + '/volt.scss'])
        .pipe(wait(500))
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer({
            overrideBrowserslist: ['> 1%']
        }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(paths.dist.css))
        // .pipe(browserSync.stream());
});

gulp.task('js', function () {
    return gulp.src([paths.src.js])
        .pipe(gulp.dest(paths.dist.js))
        // .pipe(browserSync.stream());
});

gulp.task('vendor', function() {
    return gulp.src(npmDist(), { base: paths.src.node_modules })
      .pipe(gulp.dest(paths.dist.vendor));
});

gulp.task('serve', gulp.series('scss', 'js', 'vendor', function() {
    // browserSync.init({
    //     server: paths.src.base
    // });

    gulp.watch([paths.src.scss + '/volt/**/*.scss', paths.src.scss + '/custom/**/*.scss', paths.src.scss + '/volt.scss'], gulp.series('scss'));
    gulp.watch([paths.src.js], gulp.series('js'));
    // gulp.watch([paths.src.vendor], gulp.series('vendor'));
}));

// Minify CSS
gulp.task('minify:css', function () {
    return gulp.src([
        paths.dist.css + '/volt.css'
    ])
    .pipe(cleanCss())
    .pipe(gulp.dest(paths.dist.css))
});

// Compile and copy scss/css
gulp.task('dist:css', function () {
    return gulp.src([paths.src.scss + '/volt/**/*.scss', paths.src.scss + '/custom/**/*.scss', paths.src.scss + '/volt.scss'])
        .pipe(wait(500))
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer({
            overrideBrowserslist: ['> 1%']
        }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(paths.dist.css))
});


// Copy assets
gulp.task('dist:js', function () {
    return gulp.src(paths.src.js)
        .pipe(gulp.dest(paths.dist.js))
});

// Copy node_modules to vendor
gulp.task('dist:vendor', function() {
    return gulp.src(npmDist(), { base: paths.src.node_modules })
      .pipe(gulp.dest(paths.dist.vendor));
});

gulp.task('build', gulp.series('dist:css', 'dist:js', 'minify:css', 'dist:vendor'));

// Default
gulp.task('default', gulp.series('serve'));
