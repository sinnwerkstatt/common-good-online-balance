'use strict';

module.exports = function (grunt) {

    // load all grunt tasks
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    var dataFileDe = require('./ecg_balancing/templates/ecg_balancing/dustjs/gwoe-matrix-data_de.js');
    var dataFileEn = require('./ecg_balancing/templates/ecg_balancing/dustjs/gwoe-matrix-data_en.js');

    var base = 'static';

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            options: {
                livereload: true
            },
            dusthtml: {
                files: [
                    'ecg_balancing/templates/ecg_balancing/dustjs/company_balance_overview_de.html',
                    'ecg_balancing/templates/ecg_balancing/dustjs/company_balance_overview_en.html'
                ],
                tasks: ['dusthtml:dist', 'dusthtml:dist2']
            },
            livereload: {
                files: ['**/*.html', '**/*.js']
            },
            sass: {
                files: '**/*.s[ac]ss',
                tasks: ['sass:dev']
            }
        },
        sass: {                              // Task
            dev: {                             // Another target
                options: {                       // Target options
                    style: 'expanded',
                    trace: true
                    /* lineNumbers: true */
                },
                files: {
                    'static/css/main.css': base + '/sass/main.scss',
                    'static/css/bootstrap3-ecg.css': base + '/sass/vendor/bootstrap/bootstrap.scss',
                    'ecg_balancing/static/ecg_balancing/css/company_balance.css': 'ecg_balancing/static/ecg_balancing/sass/company_balance.scss',
                    'ecg_balancing/static/ecg_balancing/css/profiles.css': 'ecg_balancing/static/ecg_balancing/sass/profiles.scss'
                }
            }
        },
        browser_sync: {
            dev: {
                bsFiles: {
                    src : [
                        base + 'css/main.css',
                        'templates/*.html',
                    ]
                },
                options: {
                    watchTask: true,
                    ghostMode: {
                        clicks: true,
                        scroll: true,
                        links: true,
                        forms: true
                    }
                }
            }
        },
        dusthtml: {
            dist: {
                src: 'ecg_balancing/templates/ecg_balancing/dustjs/company_balance_overview_de.html',
                dest: 'ecg_balancing/templates/ecg_balancing/dustjs/company_balance_overview-output_de.html',

                options: {
                    module: 'dustjs-helpers',
                    context: dataFileDe.Data.matrix
                }
            },
            dist2: {
                src: 'ecg_balancing/templates/ecg_balancing/dustjs/company_balance_overview_en.html',
                dest: 'ecg_balancing/templates/ecg_balancing/dustjs/company_balance_overview-output_en.html',

                options: {
                    module: 'dustjs-helpers',
                    context: dataFileDe.Data.matrix
                }
            }
        }
    });
    grunt.registerTask('default', [
        'sass', 'browser_sync', 'watch'
    ]);

    grunt.registerTask('renderdust', [
        'dusthtml'
    ]);
};
