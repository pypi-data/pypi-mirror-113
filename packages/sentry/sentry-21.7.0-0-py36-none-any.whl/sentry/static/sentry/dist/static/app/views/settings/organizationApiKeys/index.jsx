Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var organizationApiKeysList_1 = tslib_1.__importDefault(require("./organizationApiKeysList"));
/**
 * API Keys are deprecated, but there may be some legacy customers that still use it
 */
var OrganizationApiKeys = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationApiKeys, _super);
    function OrganizationApiKeys() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemove = function (id) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var oldKeys, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        oldKeys = tslib_1.__spreadArray([], tslib_1.__read(this.state.keys));
                        this.setState(function (state) { return ({
                            keys: state.keys.filter(function (_a) {
                                var existingId = _a.id;
                                return existingId !== id;
                            }),
                        }); });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + this.props.params.orgId + "/api-keys/" + id + "/", {
                                method: 'DELETE',
                                data: {},
                            })];
                    case 2:
                        _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        this.setState({ keys: oldKeys, busy: false });
                        indicator_1.addErrorMessage(locale_1.t('Error removing key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleAddApiKey = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var data, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({
                            busy: true,
                        });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + this.props.params.orgId + "/api-keys/", {
                                method: 'POST',
                                data: {},
                            })];
                    case 2:
                        data = _b.sent();
                        if (data) {
                            this.setState({ busy: false });
                            react_router_1.browserHistory.push(recreateRoute_1.default(data.id + "/", {
                                params: this.props.params,
                                routes: this.props.routes,
                            }));
                            indicator_1.addSuccessMessage(locale_1.t("Created a new API key \"" + data.label + "\""));
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        this.setState({ busy: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    OrganizationApiKeys.prototype.getEndpoints = function () {
        return [['keys', "/organizations/" + this.props.params.orgId + "/api-keys/"]];
    };
    OrganizationApiKeys.prototype.getTitle = function () {
        return routeTitle_1.default(locale_1.t('API Keys'), this.props.organization.slug, false);
    };
    OrganizationApiKeys.prototype.renderLoading = function () {
        return this.renderBody();
    };
    OrganizationApiKeys.prototype.renderBody = function () {
        return (<organizationApiKeysList_1.default loading={this.state.loading} busy={this.state.busy} keys={this.state.keys} onRemove={this.handleRemove} onAddApiKey={this.handleAddApiKey} {...this.props}/>);
    };
    return OrganizationApiKeys;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationApiKeys);
//# sourceMappingURL=index.jsx.map