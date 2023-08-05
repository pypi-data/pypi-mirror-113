Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
// Export route to make these forms searchable by label/help
var locale_1 = require("app/locale");
exports.route = '/settings/:orgId/projects/:projectId/processing-issues/';
var formGroups = [
    {
        // Form "section"/"panel"
        title: 'Settings',
        fields: [
            {
                name: 'sentry:reprocessing_active',
                type: 'boolean',
                label: locale_1.t('Reprocessing active'),
                disabled: function (_a) {
                    var access = _a.access;
                    return !access.has('project:write');
                },
                disabledReason: locale_1.t('Only admins may change reprocessing settings'),
                help: locale_1.t("If reprocessing is enabled, Events with fixable issues will be\n                held back until you resolve them. Processing issues will then\n                show up in the list above with hints how to fix them.\n                If reprocessing is disabled, Events with unresolved issues will\n                also show up in the stream.\n                "),
                saveOnBlur: false,
                saveMessage: function (_a) {
                    var value = _a.value;
                    return value
                        ? locale_1.t('Reprocessing applies to future events only.')
                        : locale_1.t("All events with errors will be flushed into your issues stream.\n                Beware that this process may take some time and cannot be undone.");
                },
                getData: function (form) { return ({ options: form }); },
            },
        ],
    },
];
exports.default = formGroups;
//# sourceMappingURL=processingIssues.jsx.map