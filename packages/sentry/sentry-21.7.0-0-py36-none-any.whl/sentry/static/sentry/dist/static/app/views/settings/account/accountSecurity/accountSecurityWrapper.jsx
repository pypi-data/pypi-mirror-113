Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var indicator_1 = require("app/actionCreators/indicator");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var ENDPOINT = '/users/me/authenticators/';
var AccountSecurityWrapper = /** @class */ (function (_super) {
    tslib_1.__extends(AccountSecurityWrapper, _super);
    function AccountSecurityWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDisable = function (auth) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!auth || !auth.authId) {
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + ENDPOINT + auth.authId + "/", { method: 'DELETE' })];
                    case 2:
                        _a.sent();
                        this.remountComponent();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        this.setState({ loading: false });
                        indicator_1.addErrorMessage(locale_1.t('Error disabling %s', auth.name));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRegenerateBackupCodes = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _err_2;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ loading: true });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + ENDPOINT + this.props.params.authId + "/", {
                                method: 'PUT',
                            })];
                    case 2:
                        _a.sent();
                        this.remountComponent();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_2 = _a.sent();
                        this.setState({ loading: false });
                        indicator_1.addErrorMessage(locale_1.t('Error regenerating backup codes'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRefresh = function () {
            _this.fetchData();
        };
        return _this;
    }
    AccountSecurityWrapper.prototype.getEndpoints = function () {
        return [
            ['authenticators', ENDPOINT],
            ['organizations', '/organizations/'],
            ['emails', '/users/me/emails/'],
        ];
    };
    AccountSecurityWrapper.prototype.renderBody = function () {
        var children = this.props.children;
        var _a = this.state, authenticators = _a.authenticators, organizations = _a.organizations, emails = _a.emails;
        var enrolled = (authenticators === null || authenticators === void 0 ? void 0 : authenticators.filter(function (auth) { return auth.isEnrolled && !auth.isBackupInterface; })) || [];
        var countEnrolled = enrolled.length;
        var orgsRequire2fa = (organizations === null || organizations === void 0 ? void 0 : organizations.filter(function (org) { return org.require2FA; })) || [];
        var deleteDisabled = orgsRequire2fa.length > 0 && countEnrolled === 1;
        var hasVerifiedEmail = !!(emails === null || emails === void 0 ? void 0 : emails.find(function (_a) {
            var isVerified = _a.isVerified;
            return isVerified;
        }));
        // This happens when you switch between children views and the next child
        // view is lazy loaded, it can potentially be `null` while the code split
        // package is being fetched
        if (!utils_1.defined(children)) {
            return null;
        }
        return React.cloneElement(this.props.children, {
            onDisable: this.handleDisable,
            onRegenerateBackupCodes: this.handleRegenerateBackupCodes,
            authenticators: authenticators,
            deleteDisabled: deleteDisabled,
            orgsRequire2fa: orgsRequire2fa,
            countEnrolled: countEnrolled,
            hasVerifiedEmail: hasVerifiedEmail,
            handleRefresh: this.handleRefresh,
        });
    };
    return AccountSecurityWrapper;
}(asyncComponent_1.default));
exports.default = AccountSecurityWrapper;
//# sourceMappingURL=accountSecurityWrapper.jsx.map