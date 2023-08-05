Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var slugify_1 = tslib_1.__importDefault(require("app/utils/slugify"));
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/';
var formGroups = [
    {
        // Form "section"/"panel"
        title: locale_1.t('General'),
        fields: [
            {
                name: 'slug',
                type: 'string',
                required: true,
                label: locale_1.t('Organization Slug'),
                help: locale_1.t('A unique ID used to identify this organization'),
                transformInput: slugify_1.default,
                saveOnBlur: false,
                saveMessageAlertType: 'info',
                saveMessage: locale_1.t('You will be redirected to the new organization slug after saving'),
            },
            {
                name: 'name',
                type: 'string',
                required: true,
                label: locale_1.t('Display Name'),
                help: locale_1.t('A human-friendly name for the organization'),
            },
            {
                name: 'isEarlyAdopter',
                type: 'boolean',
                label: locale_1.t('Early Adopter'),
                help: locale_1.t("Opt-in to new features before they're released to the public"),
            },
        ],
    },
    {
        title: 'Membership',
        fields: [
            {
                name: 'defaultRole',
                type: 'select',
                required: true,
                label: locale_1.t('Default Role'),
                // seems weird to have choices in initial form data
                choices: function (_a) {
                    var _b, _c;
                    var _d = _a === void 0 ? {} : _a, initialData = _d.initialData;
                    return (_c = (_b = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _b === void 0 ? void 0 : _b.map(function (r) { return [r.id, r.name]; })) !== null && _c !== void 0 ? _c : [];
                },
                help: locale_1.t('The default role new members will receive'),
                disabled: function (_a) {
                    var access = _a.access;
                    return !access.has('org:admin');
                },
            },
            {
                name: 'openMembership',
                type: 'boolean',
                required: true,
                label: locale_1.t('Open Membership'),
                help: locale_1.t('Allow organization members to freely join or leave any team'),
            },
            {
                name: 'eventsMemberAdmin',
                type: 'boolean',
                label: locale_1.t('Let Members Delete Events'),
                help: locale_1.t('Allow members to delete events (including the delete & discard action) by granting them the `event:admin` scope.'),
            },
            {
                name: 'alertsMemberWrite',
                type: 'boolean',
                label: locale_1.t('Let Members Create and Edit Alerts'),
                help: locale_1.t('Allow members to create, edit, and delete alert rules by granting them the `alerts:write` scope.'),
            },
            {
                name: 'attachmentsRole',
                type: 'select',
                choices: function (_a) {
                    var _b, _c;
                    var _d = _a.initialData, initialData = _d === void 0 ? {} : _d;
                    return (_c = (_b = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _b === void 0 ? void 0 : _b.map(function (r) { return [r.id, r.name]; })) !== null && _c !== void 0 ? _c : [];
                },
                label: locale_1.t('Attachments Access'),
                help: locale_1.t('Role required to download event attachments, such as native crash reports or log files.'),
                visible: function (_a) {
                    var features = _a.features;
                    return features.has('event-attachments');
                },
            },
            {
                name: 'debugFilesRole',
                type: 'select',
                choices: function (_a) {
                    var _b, _c;
                    var _d = _a.initialData, initialData = _d === void 0 ? {} : _d;
                    return (_c = (_b = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _b === void 0 ? void 0 : _b.map(function (r) { return [r.id, r.name]; })) !== null && _c !== void 0 ? _c : [];
                },
                label: locale_1.t('Debug Files Access'),
                help: locale_1.t('Role required to download debug information files, proguard mappings and source maps.'),
            },
        ],
    },
];
exports.default = formGroups;
//# sourceMappingURL=organizationGeneralSettings.jsx.map