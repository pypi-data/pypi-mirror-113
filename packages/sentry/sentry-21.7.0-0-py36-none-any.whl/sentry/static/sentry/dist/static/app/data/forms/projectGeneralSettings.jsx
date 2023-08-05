Object.defineProperty(exports, "__esModule", { value: true });
exports.fields = exports.route = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var platformicons_1 = require("platformicons");
var platforms_1 = tslib_1.__importDefault(require("app/data/platforms"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var slugify_1 = tslib_1.__importDefault(require("app/utils/slugify"));
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/projects/:projectId/';
var getResolveAgeAllowedValues = function () {
    var i = 0;
    var values = [];
    while (i <= 720) {
        values.push(i);
        if (i < 12) {
            i += 1;
        }
        else if (i < 24) {
            i += 3;
        }
        else if (i < 36) {
            i += 6;
        }
        else if (i < 48) {
            i += 12;
        }
        else {
            i += 24;
        }
    }
    return values;
};
var RESOLVE_AGE_ALLOWED_VALUES = getResolveAgeAllowedValues();
var ORG_DISABLED_REASON = locale_1.t("This option is enforced by your organization's settings and cannot be customized per-project.");
exports.fields = {
    slug: {
        name: 'slug',
        type: 'string',
        required: true,
        label: locale_1.t('Name'),
        placeholder: locale_1.t('my-service-name'),
        help: locale_1.t('A unique ID used to identify this project'),
        transformInput: slugify_1.default,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: locale_1.t('You will be redirected to the new project slug after saving'),
    },
    platform: {
        name: 'platform',
        type: 'select',
        label: locale_1.t('Platform'),
        choices: function () {
            return platforms_1.default.map(function (_a) {
                var id = _a.id, name = _a.name;
                return [
                    id,
                    <PlatformWrapper key={id}>
          <StyledPlatformIcon platform={id}/>
          {name}
        </PlatformWrapper>,
                ];
            });
        },
        help: locale_1.t('The primary platform for this project'),
    },
    subjectPrefix: {
        name: 'subjectPrefix',
        type: 'string',
        label: locale_1.t('Subject Prefix'),
        placeholder: locale_1.t('e.g. [my-org]'),
        help: locale_1.t('Choose a custom prefix for emails from this project'),
    },
    resolveAge: {
        name: 'resolveAge',
        type: 'range',
        allowedValues: RESOLVE_AGE_ALLOWED_VALUES,
        label: locale_1.t('Auto Resolve'),
        help: locale_1.t("Automatically resolve an issue if it hasn't been seen for this amount of time"),
        formatLabel: function (val) {
            val = Number(val);
            if (val === 0) {
                return locale_1.t('Disabled');
            }
            if (val > 23 && val % 24 === 0) {
                // Based on allowed values, val % 24 should always be true
                val = val / 24;
                return locale_1.tn('%s day', '%s days', val);
            }
            return locale_1.tn('%s hour', '%s hours', val);
        },
        saveOnBlur: false,
        saveMessage: locale_1.tct('[Caution]: Enabling auto resolve will immediately resolve anything that has ' +
            'not been seen within this period of time. There is no undo!', {
            Caution: <strong>Caution</strong>,
        }),
        saveMessageAlertType: 'warning',
    },
    allowedDomains: {
        name: 'allowedDomains',
        type: 'string',
        multiline: true,
        autosize: true,
        maxRows: 10,
        rows: 1,
        placeholder: locale_1.t('https://example.com or example.com'),
        label: locale_1.t('Allowed Domains'),
        help: locale_1.t('Separate multiple entries with a newline'),
        getValue: function (val) { return utils_1.extractMultilineFields(val); },
        setValue: function (val) { return utils_1.convertMultilineFieldValue(val); },
    },
    scrapeJavaScript: {
        name: 'scrapeJavaScript',
        type: 'boolean',
        // if this is off for the organization, it cannot be enabled for the project
        disabled: function (_a) {
            var organization = _a.organization, name = _a.name;
            return !organization[name];
        },
        disabledReason: ORG_DISABLED_REASON,
        // `props` are the props given to FormField
        setValue: function (val, props) { return props.organization && props.organization[props.name] && val; },
        label: locale_1.t('Enable JavaScript source fetching'),
        help: locale_1.t('Allow Sentry to scrape missing JavaScript source context when possible'),
    },
    securityToken: {
        name: 'securityToken',
        type: 'string',
        label: locale_1.t('Security Token'),
        help: locale_1.t('Outbound requests matching Allowed Domains will have the header "{token_header}: {token}" appended'),
        setValue: function (value) { return getDynamicText_1.default({ value: value, fixed: '__SECURITY_TOKEN__' }); },
    },
    securityTokenHeader: {
        name: 'securityTokenHeader',
        type: 'string',
        placeholder: locale_1.t('X-Sentry-Token'),
        label: locale_1.t('Security Token Header'),
        help: locale_1.t('Outbound requests matching Allowed Domains will have the header "{token_header}: {token}" appended'),
    },
    verifySSL: {
        name: 'verifySSL',
        type: 'boolean',
        label: locale_1.t('Verify TLS/SSL'),
        help: locale_1.t('Outbound requests will verify TLS (sometimes known as SSL) connections'),
    },
};
var PlatformWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledPlatformIcon = styled_1.default(platformicons_1.PlatformIcon)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectGeneralSettings.jsx.map