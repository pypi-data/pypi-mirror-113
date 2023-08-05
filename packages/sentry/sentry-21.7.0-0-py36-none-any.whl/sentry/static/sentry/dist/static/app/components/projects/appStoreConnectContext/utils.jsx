Object.defineProperty(exports, "__esModule", { value: true });
exports.getAppConnectStoreUpdateAlertMessage = exports.appStoreConnectAlertMessage = void 0;
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var locale_1 = require("app/locale");
exports.appStoreConnectAlertMessage = {
    iTunesSessionInvalid: locale_1.t('The iTunes session of your configured App Store Connect has expired.'),
    appStoreCredentialsInvalid: locale_1.t('The credentials of your configured App Store Connect are invalid.'),
    isTodayAfterItunesSessionRefreshAt: locale_1.t('The iTunes session of your configured App Store Connect will likely expire soon.'),
};
function getAppConnectStoreUpdateAlertMessage(appConnectValidationData) {
    if (appConnectValidationData.itunesSessionValid === false) {
        return exports.appStoreConnectAlertMessage.iTunesSessionInvalid;
    }
    if (appConnectValidationData.appstoreCredentialsValid === false) {
        return exports.appStoreConnectAlertMessage.appStoreCredentialsInvalid;
    }
    var itunesSessionRefreshAt = appConnectValidationData.itunesSessionRefreshAt;
    if (!itunesSessionRefreshAt) {
        return undefined;
    }
    var isTodayAfterItunesSessionRefreshAt = moment_1.default().isAfter(moment_1.default(itunesSessionRefreshAt));
    if (!isTodayAfterItunesSessionRefreshAt) {
        return undefined;
    }
    return exports.appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt;
}
exports.getAppConnectStoreUpdateAlertMessage = getAppConnectStoreUpdateAlertMessage;
//# sourceMappingURL=utils.jsx.map