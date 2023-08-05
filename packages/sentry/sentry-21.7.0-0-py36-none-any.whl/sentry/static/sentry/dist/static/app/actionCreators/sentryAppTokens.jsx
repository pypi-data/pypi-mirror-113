Object.defineProperty(exports, "__esModule", { value: true });
exports.removeSentryAppToken = exports.addSentryAppToken = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
/**
 * Install a sentry application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 */
function addSentryAppToken(client, app) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var token, err_1;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    indicator_1.addLoadingMessage();
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, client.requestPromise("/sentry-apps/" + app.slug + "/api-tokens/", {
                            method: 'POST',
                        })];
                case 2:
                    token = _a.sent();
                    indicator_1.addSuccessMessage(locale_1.t('Token successfully added.'));
                    return [2 /*return*/, token];
                case 3:
                    err_1 = _a.sent();
                    indicator_1.addErrorMessage(locale_1.t('Unable to create token'));
                    throw err_1;
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.addSentryAppToken = addSentryAppToken;
/**
 * Uninstall a sentry application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 * @param {String} token Token string
 */
function removeSentryAppToken(client, app, token) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var err_2;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    indicator_1.addLoadingMessage();
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, client.requestPromise("/sentry-apps/" + app.slug + "/api-tokens/" + token + "/", {
                            method: 'DELETE',
                        })];
                case 2:
                    _a.sent();
                    indicator_1.addSuccessMessage(locale_1.t('Token successfully deleted.'));
                    return [2 /*return*/];
                case 3:
                    err_2 = _a.sent();
                    indicator_1.addErrorMessage(locale_1.t('Unable to delete token'));
                    throw err_2;
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.removeSentryAppToken = removeSentryAppToken;
//# sourceMappingURL=sentryAppTokens.jsx.map