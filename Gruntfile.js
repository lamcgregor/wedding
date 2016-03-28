var rewriteRulesSnippet = require("grunt-connect-rewrite/lib/utils").rewriteRequest;
module.exports = function (grunt) {
    'use strict';
    var serveStatic = require('serve-static');
    var serveIndex = require('serve-index');
    grunt.registerTask('listItems', 'Lists the handlebars pages', function () {
        var sourceUrl = 'source/html/pages/';
        var files = grunt.file.expand(sourceUrl + '**/*.{hbs,handlebars}');
        if (files.length > 0) {
            var contents = '<h2>List of pages:</h2><ul>';
            for (var i = 0; i < files.length; i++) {
                var temp = files[i].split(sourceUrl);
                var title;
                if (temp[1].indexOf('handlebars') < 0) {
                    title = temp[1].split('.hbs');
                } else {
                    title = temp[1].split('.handlebars');
                }
                contents += '<li><a href="' + title[0] + '">' + title[0] + '</li>';
            }
            contents += '</ul>';
        }
        grunt.file.write('source/html/partials/fileList.handlebars', contents);
    });
    grunt.loadNpmTasks('grunt-assemble');
    grunt.loadNpmTasks('grunt-newer');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-stylus');
    grunt.loadNpmTasks('grunt-contrib-coffee');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks("grunt-connect-rewrite");
    grunt.loadNpmTasks('grunt-contrib-connect');
    grunt.loadNpmTasks('grunt-connect-proxy');
    grunt.initConfig({
        config: {
            source: 'source/',
            dest: 'dist/'
        },
        connect: {
            options: {
                port: 9012,
                livereload: 35729,
                hostname: 'localhost'
            },
            rules: [{
                from: '(^((?!css|html|js|images|png|jpg|fonts|\/$).)*$)',
                to: "$1.html"
            }],
            livereload: {
                options: {
                    open: true,
                    base: '<%= config.dest %>',
                    middleware: function (connect, options) {
                        if (!Array.isArray(options.base)) {
                            options.base = [options.base];
                        }

                        // Setup the proxy
                        var middlewares = [require('grunt-connect-proxy/lib/utils').proxyRequest, rewriteRulesSnippet];

                        // Serve static files.
                        options.base.forEach(function(base) {
                            middlewares.push(serveStatic(base));
                        });

                        // Make directory browse-able.
                        var directory = options.directory || options.base[options.base.length - 1];
                        middlewares.push(serveIndex(directory));

                        return middlewares;
                    }
                }
            },
            dist: {
                options: {
                    open: true,
                    base: '<%= config.dest %>',
                    livereload: false
                }
            },
            proxies: [
                {
                    context: '/api',
                    host: 'localhost',
                    port: 8000,
                },
                {
                    context: '/admin',
                    host: 'localhost',
                    port: 8000,
                },
                {
                    context: '/static/admin',
                    host: 'localhost',
                    port: 8000,
                }
            ]
        },
        stylus: {
            dev: {
                options: {
                    linenos: true,
                    compress: false
                },
                files: { '<%= config.dest %>css/global.css': '<%= config.source %>css/core.styl' }
            }
        },
        coffee: {
            compile: {
                options: {
                  join: true,
                },
                files: { '<%= config.dest %>js/app.js': '<%= config.source %>js/**/*.coffee' }
            }
        },
        copy: {
            files: {
                files: [
                    {
                        src: ['*.*'],
                        dest: '<%= config.dest %>images/',
                        cwd: '<%= config.source %>images/',
                        expand: true
                    },
                    {
                        src: ['*.*'],
                        dest: '<%= config.dest %>css/images/',
                        cwd: '<%= config.source %>css/images/',
                        expand: true
                    },
                    {
                        src: ['*.*'],
                        dest: '<%= config.dest %>css/fonts/',
                        cwd: '<%= config.source %>fonts/',
                        expand: true
                    }
                ]
            },
            js: {
                files: [{
                        src: ['**/*.js'],
                        dest: '<%= config.dest %>js/',
                        cwd: '<%= config.source %>js/',
                        expand: true
                    }]
            }
        },
        watch: {
            scripts: {
                options: { livereload: true },
                files: ['<%= config.source %>js/*.js'],
                tasks: ['copy:js']
            },
            html: {
                options: { livereload: true },
                files: [
                    '<%= config.source %>html/**/*.{html,hbs,handlebars,json,yml}',
                    '!<%= config.source %>html/partials/fileList.{hbs,handlebars}'
                ],
                tasks: [
                    'listItems',
                    'assemble'
                ]
            },
            js: {
                options: { livereload: true },
                files: ['<%= config.source %>js/**/*.coffee'],
                tasks: ['coffee:compile']
            },
            css: {
                options: { livereload: true },
                files: ['<%= config.source %>css/**/*.styl'],
                tasks: ['stylus:dev']
            },
            files: {
                options: { livereload: true },
                files: [
                    '<%= config.source %>fonts/*.*',
                    '<%= config.source %>css/images/*.*',
                    '<%= config.source %>images/*.*'
                ],
                tasks: ['copy:files']
            }
        },
        assemble: {
            options: {
                flatten: false,
                partials: ['<%= config.source %>html/partials/**/*.{hbs,handlebars}'],
                layout: ['<%= config.source %>html/layouts/default.handlebars'],
                data: ['<%= config.source %>html/data/**/*.{json,yml}'],
                stripHbsWhitespace:true
            },
            pages: {
                files: [{
                        expand: true,
                        cwd: '<%= config.source %>html/pages/',
                        dest: '<%= config.dest %>',
                        src: ['**/*.{hbs,handlebars}'],
                        ext: '.html'
                    }]
            }
        }
    });
    grunt.registerTask('build', [
        'listItems',
        'assemble',
        'stylus:dev',
        'coffee:compile',
        'copy:js',
        'copy:files'
    ]);
    grunt.registerTask('dev', [
        'listItems',
        'assemble',
        'stylus:dev',
        'coffee:compile',
        'copy:js',
        'copy:files'
    ]);
    grunt.registerTask('default', [
        'dev',
        'configureProxies:server',
        'configureRewriteRules',
        'connect:livereload',
        'watch'
    ]);
};