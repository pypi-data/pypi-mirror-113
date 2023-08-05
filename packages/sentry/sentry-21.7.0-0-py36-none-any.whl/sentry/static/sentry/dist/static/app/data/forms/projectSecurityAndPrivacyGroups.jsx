Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
var tslib_1 = require("tslib");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var crashReports_1 = require("app/utils/crashReports");
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/projects/:projectId/security-and-privacy/';
var ORG_DISABLED_REASON = locale_1.t("This option is enforced by your organization's settings and cannot be customized per-project.");
// Check if a field has been set AND IS TRUTHY at the organization level.
var hasOrgOverride = function (_a) {
    var organization = _a.organization, name = _a.name;
    return organization[name];
};
exports.default = [
    {
        title: locale_1.t('Security & Privacy'),
        fields: [
            {
                name: 'storeCrashReports',
                type: 'select',
                label: locale_1.t('Store Native Crash Reports'),
                help: function (_a) {
                    var organization = _a.organization;
                    return locale_1.tct('Store native crash reports such as Minidumps for improved processing and download in issue details. Overrides [organizationSettingsLink: organization settings].', {
                        organizationSettingsLink: (<link_1.default to={"/settings/" + organization.slug + "/security-and-privacy/"}/>),
                    });
                },
                visible: function (_a) {
                    var features = _a.features;
                    return features.has('event-attachments');
                },
                placeholder: function (_a) {
                    var organization = _a.organization, value = _a.value;
                    // empty value means that this project should inherit organization settings
                    if (value === '') {
                        return locale_1.tct('Inherit organization settings ([organizationValue])', {
                            organizationValue: crashReports_1.formatStoreCrashReports(organization.storeCrashReports),
                        });
                    }
                    // HACK: some organization can have limit of stored crash reports a number that's not in the options (legacy reasons),
                    // we therefore display it in a placeholder
                    return crashReports_1.formatStoreCrashReports(value);
                },
                choices: function (_a) {
                    var organization = _a.organization;
                    return crashReports_1.getStoreCrashReportsValues(crashReports_1.SettingScope.Project).map(function (value) { return [
                        value,
                        crashReports_1.formatStoreCrashReports(value, organization.storeCrashReports),
                    ]; });
                },
            },
        ],
    },
    {
        title: locale_1.t('Data Scrubbing'),
        fields: [
            {
                name: 'dataScrubber',
                type: 'boolean',
                label: locale_1.t('Data Scrubber'),
                disabled: hasOrgOverride,
                disabledReason: ORG_DISABLED_REASON,
                help: locale_1.t('Enable server-side data scrubbing'),
                // `props` are the props given to FormField
                setValue: function (val, props) {
                    return (props.organization && props.organization[props.name]) || val;
                },
                confirm: {
                    false: locale_1.t('Are you sure you want to disable server-side data scrubbing?'),
                },
            },
            {
                name: 'dataScrubberDefaults',
                type: 'boolean',
                disabled: hasOrgOverride,
                disabledReason: ORG_DISABLED_REASON,
                label: locale_1.t('Use Default Scrubbers'),
                help: locale_1.t('Apply default scrubbers to prevent things like passwords and credit cards from being stored'),
                // `props` are the props given to FormField
                setValue: function (val, props) {
                    return (props.organization && props.organization[props.name]) || val;
                },
                confirm: {
                    false: locale_1.t('Are you sure you want to disable using default scrubbers?'),
                },
            },
            {
                name: 'scrubIPAddresses',
                type: 'boolean',
                disabled: hasOrgOverride,
                disabledReason: ORG_DISABLED_REASON,
                // `props` are the props given to FormField
                setValue: function (val, props) {
                    return (props.organization && props.organization[props.name]) || val;
                },
                label: locale_1.t('Prevent Storing of IP Addresses'),
                help: locale_1.t('Preventing IP addresses from being stored for new events'),
                confirm: {
                    false: locale_1.t('Are you sure you want to disable scrubbing IP addresses?'),
                },
            },
            {
                name: 'sensitiveFields',
                type: 'string',
                multiline: true,
                autosize: true,
                maxRows: 10,
                rows: 1,
                placeholder: locale_1.t('email'),
                label: locale_1.t('Additional Sensitive Fields'),
                help: locale_1.t('Additional field names to match against when scrubbing data. Separate multiple entries with a newline'),
                getValue: function (val) { return utils_1.extractMultilineFields(val); },
                setValue: function (val) { return utils_1.convertMultilineFieldValue(val); },
            },
            {
                name: 'safeFields',
                type: 'string',
                multiline: true,
                autosize: true,
                maxRows: 10,
                rows: 1,
                placeholder: locale_1.t('business-email'),
                label: locale_1.t('Safe Fields'),
                help: locale_1.t('Field names which data scrubbers should ignore. Separate multiple entries with a newline'),
                getValue: function (val) { return utils_1.extractMultilineFields(val); },
                setValue: function (val) { return utils_1.convertMultilineFieldValue(val); },
            },
        ],
    },
];
//# sourceMappingURL=projectSecurityAndPrivacyGroups.jsx.map