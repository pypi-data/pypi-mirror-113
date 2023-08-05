Object.defineProperty(exports, "__esModule", { value: true });
exports.removeAuthenticator = exports.logout = exports.updateUser = exports.disconnectIdentity = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
function disconnectIdentity(identity) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var api, _a;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    api = new api_1.Client();
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/users/me/social-identities/" + identity.id + "/", {
                            method: 'DELETE',
                        })];
                case 2:
                    _b.sent();
                    indicator_1.addSuccessMessage("Disconnected " + identity.providerLabel);
                    return [3 /*break*/, 4];
                case 3:
                    _a = _b.sent();
                    indicator_1.addErrorMessage('Error disconnecting identity');
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.disconnectIdentity = disconnectIdentity;
function updateUser(user) {
    var previousUser = configStore_1.default.get('user');
    // If the user changed their theme preferences, we should also update
    // the config store
    if (previousUser.options.theme !== user.options.theme &&
        user.options.theme !== 'system') {
        configStore_1.default.set('theme', user.options.theme);
    }
    // Ideally we'd fire an action but this is gonna get refactored soon anyway
    configStore_1.default.set('user', user);
}
exports.updateUser = updateUser;
function logout(api) {
    return api.requestPromise('/auth/', { method: 'DELETE' });
}
exports.logout = logout;
function removeAuthenticator(api, userId, authId) {
    return api.requestPromise("/users/" + userId + "/authenticators/" + authId + "/", {
        method: 'DELETE',
    });
}
exports.removeAuthenticator = removeAuthenticator;
//# sourceMappingURL=account.jsx.map