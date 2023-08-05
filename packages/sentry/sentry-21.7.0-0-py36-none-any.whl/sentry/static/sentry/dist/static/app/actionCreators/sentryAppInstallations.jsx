Object.defineProperty(exports, "__esModule", { value: true });
exports.uninstallSentryApp = exports.installSentryApp = void 0;
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
/**
 * Install a sentry application
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {Object} app SentryApp
 */
function installSentryApp(client, orgId, app) {
    indicator_1.addLoadingMessage();
    var promise = client.requestPromise("/organizations/" + orgId + "/sentry-app-installations/", {
        method: 'POST',
        data: { slug: app.slug },
    });
    promise.then(function () { return indicator_1.clearIndicators(); }, function () { return indicator_1.addErrorMessage(locale_1.t("Unable to install " + app.name)); });
    return promise;
}
exports.installSentryApp = installSentryApp;
/**
 * Uninstall a sentry application
 *
 * @param {Object} client ApiClient
 * @param {Object} install SentryAppInstallation
 */
function uninstallSentryApp(client, install) {
    indicator_1.addLoadingMessage();
    var promise = client.requestPromise("/sentry-app-installations/" + install.uuid + "/", {
        method: 'DELETE',
    });
    promise.then(function () {
        indicator_1.addSuccessMessage(locale_1.t(install.app.slug + " successfully uninstalled."));
    }, function () { return indicator_1.clearIndicators(); });
    return promise;
}
exports.uninstallSentryApp = uninstallSentryApp;
//# sourceMappingURL=sentryAppInstallations.jsx.map