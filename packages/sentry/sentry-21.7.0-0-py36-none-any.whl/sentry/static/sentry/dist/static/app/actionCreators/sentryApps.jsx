Object.defineProperty(exports, "__esModule", { value: true });
exports.removeSentryApp = void 0;
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
/**
 * Remove a Sentry Application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 */
function removeSentryApp(client, app) {
    indicator_1.addLoadingMessage();
    var promise = client.requestPromise("/sentry-apps/" + app.slug + "/", {
        method: 'DELETE',
    });
    promise.then(function () {
        indicator_1.addSuccessMessage(locale_1.t('%s successfully removed.', app.slug));
    }, function () {
        indicator_1.clearIndicators();
        indicator_1.addErrorMessage(locale_1.t('Unable to remove %s integration', app.slug));
    });
    return promise;
}
exports.removeSentryApp = removeSentryApp;
//# sourceMappingURL=sentryApps.jsx.map