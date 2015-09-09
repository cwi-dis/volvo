var gulp = require('gulp');

var concat = require('gulp-concat');
var react = require('gulp-react');
var uglify = require('gulp-uglify');

gulp.task('build', function () {
    return gulp.src('public/js/components/**/*.jsx')
               .pipe(react())
               .pipe(concat('react_bundle.js'))
               .pipe(uglify())
               .pipe(gulp.dest('public/js'));
});

gulp.task('minify', ['build'], function () {
    return gulp.src(['public/js/*.js', '!public/js/bundle.js'])
               .pipe(concat('bundle.js'))
               .pipe(uglify())
               .pipe(gulp.dest('public/js'));
});

gulp.task('watch', function () {
    gulp.watch('public/js/components/**/*.jsx', ['build']);
});

gulp.task('default', ['build']);
