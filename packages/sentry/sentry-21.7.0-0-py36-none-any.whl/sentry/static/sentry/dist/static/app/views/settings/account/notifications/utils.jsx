Object.defineProperty(exports, "__esModule", { value: true });
exports.getParentField = exports.getStateToPutForParent = exports.getStateToPutForDefault = exports.getStateToPutForProvider = exports.getParentData = exports.getParentValues = exports.getParentIds = exports.isEverythingDisabled = exports.decideDefault = exports.getCurrentDefault = exports.getCurrentProviders = exports.getUserDefaultValues = exports.mergeNotificationSettings = exports.backfillMissingProvidersWithFallback = exports.getChoiceString = exports.providerListToString = exports.getFallBackValue = exports.groupByOrganization = exports.getParentKey = exports.isGroupedByProject = void 0;
var tslib_1 = require("tslib");
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var locale_1 = require("app/locale");
var constants_1 = require("app/views/settings/account/notifications/constants");
var fields2_1 = require("app/views/settings/account/notifications/fields2");
var parentLabel_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/parentLabel"));
// Which fine-tuning parts are grouped by project
var isGroupedByProject = function (notificationType) {
    return ['alerts', 'email', 'workflow'].includes(notificationType);
};
exports.isGroupedByProject = isGroupedByProject;
var getParentKey = function (notificationType) {
    return exports.isGroupedByProject(notificationType) ? 'project' : 'organization';
};
exports.getParentKey = getParentKey;
var groupByOrganization = function (projects) {
    return projects.reduce(function (acc, project) {
        var orgSlug = project.organization.slug;
        if (acc.hasOwnProperty(orgSlug)) {
            acc[orgSlug].projects.push(project);
        }
        else {
            acc[orgSlug] = {
                organization: project.organization,
                projects: [project],
            };
        }
        return acc;
    }, {});
};
exports.groupByOrganization = groupByOrganization;
var getFallBackValue = function (notificationType) {
    switch (notificationType) {
        case 'alerts':
            return 'always';
        case 'deploy':
            return 'committed_only';
        case 'workflow':
            return 'subscribe_only';
        default:
            return '';
    }
};
exports.getFallBackValue = getFallBackValue;
var providerListToString = function (providers) {
    return providers.sort().join('+');
};
exports.providerListToString = providerListToString;
var getChoiceString = function (choices, key) {
    if (!choices) {
        return 'default';
    }
    var found = choices.find(function (row) { return row[0] === key; });
    if (!found) {
        throw new Error("Could not find " + key);
    }
    return found[1];
};
exports.getChoiceString = getChoiceString;
var backfillMissingProvidersWithFallback = function (data, providerList, fallbackValue, scopeType) {
    /**
     * Transform `data`, a mapping of providers to values, so that all providers
     * in `providerList` are "on" in the resulting object. The "on" value is
     * determined by checking `data` for non-"never" values and falling back to
     * the value `fallbackValue`. The "off" value is either "default" or "never"
     * depending on whether `scopeType` is "parent" or "user" respectively.
     */
    // First pass: determine the fallback value.
    var fallback = Object.values(data).reduce(function (previousValue, currentValue) {
        return currentValue === 'never' ? previousValue : currentValue;
    }, fallbackValue);
    // Second pass: fill in values for every provider.
    return Object.fromEntries(Object.keys(constants_1.ALL_PROVIDERS).map(function (provider) { return [
        provider,
        providerList.includes(provider)
            ? fallback
            : scopeType === 'user'
                ? 'never'
                : 'default',
    ]; }));
};
exports.backfillMissingProvidersWithFallback = backfillMissingProvidersWithFallback;
var mergeNotificationSettings = function () {
    var objects = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        objects[_i] = arguments[_i];
    }
    /** Deeply merge N notification settings objects (usually just 2). */
    var output = {};
    objects.map(function (settingsByType) {
        return Object.entries(settingsByType).map(function (_a) {
            var _b = tslib_1.__read(_a, 2), type = _b[0], settingsByScopeType = _b[1];
            return Object.entries(settingsByScopeType).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), scopeType = _b[0], settingsByScopeId = _b[1];
                return Object.entries(settingsByScopeId).map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), scopeId = _b[0], settingsByProvider = _b[1];
                    set_1.default(output, [type, scopeType, scopeId].join('.'), settingsByProvider);
                });
            });
        });
    });
    return output;
};
exports.mergeNotificationSettings = mergeNotificationSettings;
var getUserDefaultValues = function (notificationType, notificationSettings) {
    var _a;
    /**
     * Get the mapping of providers to values that describe a user's parent-
     * independent notification preferences. The data from the API uses the user
     * ID rather than "me" so we assume the first ID is the user's.
     */
    return (Object.values(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a.user) || {}).pop() ||
        Object.fromEntries(Object.entries(constants_1.ALL_PROVIDERS).map(function (_a) {
            var _b = tslib_1.__read(_a, 2), provider = _b[0], value = _b[1];
            return [
                provider,
                value === 'default' ? exports.getFallBackValue(notificationType) : value,
            ];
        })));
};
exports.getUserDefaultValues = getUserDefaultValues;
var getCurrentProviders = function (notificationType, notificationSettings) {
    /** Get the list of providers currently active on this page. Note: this can be empty. */
    var userData = exports.getUserDefaultValues(notificationType, notificationSettings);
    return Object.entries(userData)
        .filter(function (_a) {
        var _b = tslib_1.__read(_a, 2), _ = _b[0], value = _b[1];
        return !['never'].includes(value);
    })
        .map(function (_a) {
        var _b = tslib_1.__read(_a, 2), provider = _b[0], _ = _b[1];
        return provider;
    });
};
exports.getCurrentProviders = getCurrentProviders;
var getCurrentDefault = function (notificationType, notificationSettings) {
    /** Calculate the currently selected provider. */
    var providersList = exports.getCurrentProviders(notificationType, notificationSettings);
    return providersList.length
        ? exports.getUserDefaultValues(notificationType, notificationSettings)[providersList[0]]
        : 'never';
};
exports.getCurrentDefault = getCurrentDefault;
var decideDefault = function (notificationType, notificationSettings) {
    var _a;
    /**
     * For a given notificationType, are the parent-independent setting "never"
     * for all providers and are the parent-specific settings "default" or
     * "never". If so, the API is telling us that the user has opted out of
     * all notifications.
     */
    var compare = function (a, b) { return constants_1.VALUE_MAPPING[a] - constants_1.VALUE_MAPPING[b]; };
    var parentIndependentSetting = Object.values(exports.getUserDefaultValues(notificationType, notificationSettings))
        .sort(compare)
        .pop() || 'never';
    if (parentIndependentSetting !== 'never') {
        return parentIndependentSetting;
    }
    var parentSpecificSetting = Object.values(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a[exports.getParentKey(notificationType)]) || {})
        .flatMap(function (settingsByProvider) { return Object.values(settingsByProvider); })
        .sort(compare)
        .pop() || 'default';
    return parentSpecificSetting === 'default' ? 'never' : parentSpecificSetting;
};
exports.decideDefault = decideDefault;
var isEverythingDisabled = function (notificationType, notificationSettings) {
    /**
     * For a given notificationType, are the parent-independent setting "never"
     * for all providers and are the parent-specific settings "default" or
     * "never"? If so, the API is telling us that the user has opted out of
     * all notifications.
     */
    return ['never', 'default'].includes(exports.decideDefault(notificationType, notificationSettings));
};
exports.isEverythingDisabled = isEverythingDisabled;
var getParentIds = function (notificationType, notificationSettings) {
    var _a;
    /**
     * Extract either the list of project or organization IDs from the
     * notification settings in state. This assumes that the notification settings
     * object is fully backfilled with settings for every parent.
     */
    return Object.keys(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a[exports.getParentKey(notificationType)]) || {});
};
exports.getParentIds = getParentIds;
var getParentValues = function (notificationType, notificationSettings, parentId) {
    var _a, _b;
    return (((_b = (_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a[exports.getParentKey(notificationType)]) === null || _b === void 0 ? void 0 : _b[parentId]) || {
        email: 'default',
    });
};
exports.getParentValues = getParentValues;
var getParentData = function (notificationType, notificationSettings, parents) {
    /** Get a mapping of all parent IDs to the notification setting for the current providers. */
    var provider = exports.getCurrentProviders(notificationType, notificationSettings)[0];
    return Object.fromEntries(parents.map(function (parent) { return [
        parent.id,
        exports.getParentValues(notificationType, notificationSettings, parent.id)[provider],
    ]; }));
};
exports.getParentData = getParentData;
var getStateToPutForProvider = function (notificationType, notificationSettings, changedData) {
    var _a, _b;
    /**
     * I don't need to update the provider for EVERY once of the user's projects
     * and organizations, just the user and parents that have explicit settings.
     */
    var providerList = changedData.provider.split('+');
    var fallbackValue = exports.getFallBackValue(notificationType);
    var updatedNotificationSettings;
    if (Object.keys(notificationSettings).length) {
        updatedNotificationSettings = (_a = {},
            _a[notificationType] = Object.fromEntries(Object.entries(notificationSettings[notificationType]).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), scopeType = _b[0], scopeTypeData = _b[1];
                return [
                    scopeType,
                    Object.fromEntries(Object.entries(scopeTypeData).map(function (_a) {
                        var _b = tslib_1.__read(_a, 2), scopeId = _b[0], scopeIdData = _b[1];
                        return [
                            scopeId,
                            exports.backfillMissingProvidersWithFallback(scopeIdData, providerList, fallbackValue, scopeType),
                        ];
                    })),
                ];
            })),
            _a);
    }
    else {
        // If the user has no settings, we need to create them.
        updatedNotificationSettings = (_b = {},
            _b[notificationType] = {
                user: {
                    me: Object.fromEntries(providerList.map(function (provider) { return [provider, fallbackValue]; })),
                },
            },
            _b);
    }
    return updatedNotificationSettings;
};
exports.getStateToPutForProvider = getStateToPutForProvider;
var getStateToPutForDefault = function (notificationType, notificationSettings, changedData, parentIds) {
    /**
     * Update the current providers' parent-independent notification settings
     * with the new value. If the new value is "never", then also update all
     * parent-specific notification settings to "default". If the previous value
     * was "never", then assume providerList should be "email" only.
     */
    var _a;
    var newValue = Object.values(changedData)[0];
    var providerList = exports.getCurrentProviders(notificationType, notificationSettings);
    if (!providerList.length) {
        providerList = ['email'];
    }
    var updatedNotificationSettings = (_a = {},
        _a[notificationType] = {
            user: {
                me: Object.fromEntries(providerList.map(function (provider) { return [provider, newValue]; })),
            },
        },
        _a);
    if (newValue === 'never') {
        updatedNotificationSettings[notificationType][exports.getParentKey(notificationType)] =
            Object.fromEntries(parentIds.map(function (parentId) { return [
                parentId,
                Object.fromEntries(providerList.map(function (provider) { return [provider, 'default']; })),
            ]; }));
    }
    return updatedNotificationSettings;
};
exports.getStateToPutForDefault = getStateToPutForDefault;
var getStateToPutForParent = function (notificationType, notificationSettings, changedData, parentId) {
    /** Get the diff of the Notification Settings for this parent ID. */
    var _a, _b, _c;
    var providerList = exports.getCurrentProviders(notificationType, notificationSettings);
    var newValue = Object.values(changedData)[0];
    return _a = {},
        _a[notificationType] = (_b = {},
            _b[exports.getParentKey(notificationType)] = (_c = {},
                _c[parentId] = Object.fromEntries(providerList.map(function (provider) { return [provider, newValue]; })),
                _c),
            _b),
        _a;
};
exports.getStateToPutForParent = getStateToPutForParent;
var getParentField = function (notificationType, notificationSettings, parent, onChange) {
    /** Render each parent and add a default option to the the field choices. */
    var _a;
    var defaultFields = fields2_1.NOTIFICATION_SETTING_FIELDS[notificationType];
    return Object.assign({}, defaultFields, {
        label: <parentLabel_1.default parent={parent} notificationType={notificationType}/>,
        getData: function (data) { return onChange(data, parent.id); },
        name: parent.id,
        choices: (_a = defaultFields.choices) === null || _a === void 0 ? void 0 : _a.concat([
            [
                'default',
                locale_1.t('Default') + " (" + exports.getChoiceString(defaultFields.choices, exports.getCurrentDefault(notificationType, notificationSettings)) + ")",
            ],
        ]),
        defaultValue: 'default',
        help: undefined,
    });
};
exports.getParentField = getParentField;
//# sourceMappingURL=utils.jsx.map