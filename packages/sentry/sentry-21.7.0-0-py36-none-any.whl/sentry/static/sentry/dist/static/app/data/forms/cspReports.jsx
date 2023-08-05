Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
// Export route to make these forms searchable by label/help
var locale_1 = require("app/locale");
exports.route = '/settings/:orgId/projects/:projectId/csp/';
var formGroups = [
    {
        // Form "section"/"panel"
        title: 'CSP Settings',
        fields: [
            {
                name: 'sentry:csp_ignored_sources_defaults',
                type: 'boolean',
                label: locale_1.t('Use default ignored sources'),
                help: locale_1.t('Our default list will attempt to ignore common issues and reduce noise.'),
                getData: function (data) { return ({ options: data }); },
            },
            // XXX: Org details endpoints accept these multiline inputs as a list,
            // where as it looks like project details accepts it as a string with newlines
            {
                name: 'sentry:csp_ignored_sources',
                type: 'string',
                multiline: true,
                autosize: true,
                rows: 4,
                placeholder: 'e.g.\nfile://*\n*.example.com\nexample.com',
                label: locale_1.t('Additional ignored sources'),
                help: locale_1.t('Discard reports about requests from the given sources. Separate multiple entries with a newline.'),
                extraHelp: locale_1.t('Separate multiple entries with a newline.'),
                getData: function (data) { return ({ options: data }); },
            },
        ],
    },
];
exports.default = formGroups;
//# sourceMappingURL=cspReports.jsx.map