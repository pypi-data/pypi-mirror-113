Object.defineProperty(exports, "__esModule", { value: true });
exports.getForm = exports.getOptionField = exports.getOptionDefault = exports.getOption = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var keyBy_1 = tslib_1.__importDefault(require("lodash/keyBy"));
var forms_1 = require("app/components/forms");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
// This are ordered based on their display order visually
var sections = [
    {
        key: 'system',
    },
    {
        key: 'mail',
        heading: locale_1.t('Outbound email'),
    },
    {
        key: 'auth',
        heading: locale_1.t('Authentication'),
    },
    {
        key: 'beacon',
        heading: locale_1.t('Beacon'),
    },
];
// This are ordered based on their display order visually
var definitions = [
    {
        key: 'system.url-prefix',
        label: locale_1.t('Root URL'),
        placeholder: 'https://sentry.example.com',
        help: locale_1.t('The root web address which is used to communicate with the Sentry backend.'),
        defaultValue: function () { return document.location.protocol + "//" + document.location.host; },
    },
    {
        key: 'system.admin-email',
        label: locale_1.t('Admin Email'),
        placeholder: 'admin@example.com',
        help: locale_1.t('The technical contact for this Sentry installation.'),
        // TODO(dcramer): this should not be hardcoded to a component
        component: forms_1.EmailField,
        defaultValue: function () { return configStore_1.default.get('user').email; },
    },
    {
        key: 'system.support-email',
        label: locale_1.t('Support Email'),
        placeholder: 'support@example.com',
        help: locale_1.t('The support contact for this Sentry installation.'),
        // TODO(dcramer): this should not be hardcoded to a component
        component: forms_1.EmailField,
        defaultValue: function () { return configStore_1.default.get('user').email; },
    },
    {
        key: 'system.security-email',
        label: locale_1.t('Security Email'),
        placeholder: 'security@example.com',
        help: locale_1.t('The security contact for this Sentry installation.'),
        // TODO(dcramer): this should not be hardcoded to a component
        component: forms_1.EmailField,
        defaultValue: function () { return configStore_1.default.get('user').email; },
    },
    {
        key: 'system.rate-limit',
        label: locale_1.t('Rate Limit'),
        placeholder: 'e.g. 500',
        help: locale_1.t('The maximum number of events the system should accept per minute. A value of 0 will disable the default rate limit.'),
    },
    {
        key: 'auth.allow-registration',
        label: locale_1.t('Allow Registration'),
        help: locale_1.t('Allow anyone to create an account and access this Sentry installation.'),
        component: forms_1.BooleanField,
        defaultValue: function () { return false; },
    },
    {
        key: 'auth.ip-rate-limit',
        label: locale_1.t('IP Rate Limit'),
        placeholder: 'e.g. 10',
        help: locale_1.t('The maximum number of times an authentication attempt may be made by a single IP address in a 60 second window.'),
    },
    {
        key: 'auth.user-rate-limit',
        label: locale_1.t('User Rate Limit'),
        placeholder: 'e.g. 10',
        help: locale_1.t('The maximum number of times an authentication attempt may be made against a single account in a 60 second window.'),
    },
    {
        key: 'api.rate-limit.org-create',
        label: 'Organization Creation Rate Limit',
        placeholder: 'e.g. 5',
        help: locale_1.t('The maximum number of organizations which may be created by a single account in a one hour window.'),
    },
    {
        key: 'beacon.anonymous',
        label: 'Usage Statistics',
        component: forms_1.RadioBooleanField,
        // yes and no are inverted here due to the nature of this configuration
        noLabel: 'Send my contact information along with usage statistics',
        yesLabel: 'Please keep my usage information anonymous',
        yesFirst: false,
        help: locale_1.tct('If enabled, any stats reported to sentry.io will exclude identifying information (such as your administrative email address). By anonymizing your installation the Sentry team will be unable to contact you about security updates. For more information on what data is sent to Sentry, see the [link:documentation].', {
            link: <a href="https://develop.sentry.dev/self-hosted/"/>,
        }),
    },
    {
        key: 'mail.from',
        label: locale_1.t('Email From'),
        component: forms_1.EmailField,
        defaultValue: function () { return "sentry@" + document.location.hostname; },
        help: locale_1.t('Email address to be used in From for all outbound email.'),
    },
    {
        key: 'mail.host',
        label: locale_1.t('SMTP Host'),
        placeholder: 'localhost',
        defaultValue: function () { return 'localhost'; },
    },
    {
        key: 'mail.port',
        label: locale_1.t('SMTP Port'),
        placeholder: '25',
        defaultValue: function () { return '25'; },
    },
    {
        key: 'mail.username',
        label: locale_1.t('SMTP Username'),
        defaultValue: function () { return ''; },
    },
    {
        key: 'mail.password',
        label: locale_1.t('SMTP Password'),
        // TODO(mattrobenolt): We don't want to use a real password field unless
        // there's a way to reveal it. Without being able to see the password, it's
        // impossible to confirm if it's right.
        // component: PasswordField,
        defaultValue: function () { return ''; },
    },
    {
        key: 'mail.use-tls',
        label: locale_1.t('Use STARTTLS? (exclusive with SSL)'),
        component: forms_1.BooleanField,
        defaultValue: function () { return false; },
    },
    {
        key: 'mail.use-ssl',
        label: locale_1.t('Use SSL? (exclusive with STARTTLS)'),
        component: forms_1.BooleanField,
        defaultValue: function () { return false; },
    },
];
var definitionsMap = keyBy_1.default(definitions, function (def) { return def.key; });
var disabledReasons = {
    diskPriority: 'This setting is defined in config.yml and may not be changed via the web UI.',
    smtpDisabled: 'SMTP mail has been disabled, so this option is unavailable',
};
function getOption(option) {
    return definitionsMap[option];
}
exports.getOption = getOption;
function getOptionDefault(option) {
    var meta = getOption(option);
    return meta.defaultValue ? meta.defaultValue() : undefined;
}
exports.getOptionDefault = getOptionDefault;
function optionsForSection(section) {
    return definitions.filter(function (option) { return option.key.split('.')[0] === section.key; });
}
function getOptionField(option, field) {
    var meta = tslib_1.__assign(tslib_1.__assign({}, getOption(option)), field);
    var Field = meta.component || forms_1.TextField;
    return (<Field {...meta} name={option} key={option} defaultValue={getOptionDefault(option)} required={meta.required && !meta.allowEmpty} disabledReason={meta.disabledReason && disabledReasons[meta.disabledReason]}/>);
}
exports.getOptionField = getOptionField;
function getSectionFieldSet(section, fields) {
    return (<fieldset key={section.key}>
      {section.heading && <legend>{section.heading}</legend>}
      {fields}
    </fieldset>);
}
function getForm(fieldMap) {
    var e_1, _a, e_2, _b;
    var sets = [];
    try {
        for (var sections_1 = tslib_1.__values(sections), sections_1_1 = sections_1.next(); !sections_1_1.done; sections_1_1 = sections_1.next()) {
            var section = sections_1_1.value;
            var set = [];
            try {
                for (var _c = (e_2 = void 0, tslib_1.__values(optionsForSection(section))), _d = _c.next(); !_d.done; _d = _c.next()) {
                    var option = _d.value;
                    if (fieldMap[option.key]) {
                        set.push(fieldMap[option.key]);
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
                }
                finally { if (e_2) throw e_2.error; }
            }
            if (set.length) {
                sets.push(getSectionFieldSet(section, set));
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (sections_1_1 && !sections_1_1.done && (_a = sections_1.return)) _a.call(sections_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return sets;
}
exports.getForm = getForm;
//# sourceMappingURL=options.jsx.map