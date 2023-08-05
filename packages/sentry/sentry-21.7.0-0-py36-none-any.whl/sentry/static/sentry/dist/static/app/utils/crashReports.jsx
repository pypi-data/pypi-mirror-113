Object.defineProperty(exports, "__esModule", { value: true });
exports.getStoreCrashReportsValues = exports.SettingScope = exports.formatStoreCrashReports = void 0;
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
function formatStoreCrashReports(value, organizationValue) {
    if (value === null && utils_1.defined(organizationValue)) {
        return locale_1.tct('Inherit organization settings ([organizationValue])', {
            organizationValue: formatStoreCrashReports(organizationValue),
        });
    }
    if (value === -1) {
        return locale_1.t('Unlimited');
    }
    if (value === 0) {
        return locale_1.t('Disabled');
    }
    return locale_1.tct('[value] per issue', { value: value });
}
exports.formatStoreCrashReports = formatStoreCrashReports;
var SettingScope;
(function (SettingScope) {
    SettingScope[SettingScope["Organization"] = 0] = "Organization";
    SettingScope[SettingScope["Project"] = 1] = "Project";
})(SettingScope = exports.SettingScope || (exports.SettingScope = {}));
function getStoreCrashReportsValues(settingScope) {
    var values = [
        0,
        1,
        5,
        10,
        20,
        -1, // unlimited
    ];
    if (settingScope === SettingScope.Project) {
        values.unshift(null); // inherit option
    }
    return values;
}
exports.getStoreCrashReportsValues = getStoreCrashReportsValues;
//# sourceMappingURL=crashReports.jsx.map