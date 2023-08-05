Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var keyRow_1 = tslib_1.__importDefault(require("./keyRow"));
var ProjectKeys = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectKeys, _super);
    function ProjectKeys() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Optimistically remove key
         */
        _this.handleRemoveKey = function (data) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var oldKeyList, _a, orgId, projectId, _err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        oldKeyList = tslib_1.__spreadArray([], tslib_1.__read(this.state.keyList));
                        indicator_1.addLoadingMessage(locale_1.t('Revoking key\u2026'));
                        this.setState(function (state) { return ({
                            keyList: state.keyList.filter(function (key) { return key.id !== data.id; }),
                        }); });
                        _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/keys/" + data.id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Revoked key'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        this.setState({
                            keyList: oldKeyList,
                        });
                        indicator_1.addErrorMessage(locale_1.t('Unable to revoke key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleToggleKey = function (isActive, data) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var oldKeyList, _a, orgId, projectId, _err_2;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        oldKeyList = tslib_1.__spreadArray([], tslib_1.__read(this.state.keyList));
                        indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
                        this.setState(function (state) {
                            var keyList = state.keyList.map(function (key) {
                                if (key.id === data.id) {
                                    return tslib_1.__assign(tslib_1.__assign({}, key), { isActive: !data.isActive });
                                }
                                return key;
                            });
                            return { keyList: keyList };
                        });
                        _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/keys/" + data.id + "/", {
                                method: 'PUT',
                                data: { isActive: isActive },
                            })];
                    case 2:
                        _b.sent();
                        indicator_1.addSuccessMessage(isActive ? locale_1.t('Enabled key') : locale_1.t('Disabled key'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_2 = _b.sent();
                        indicator_1.addErrorMessage(isActive ? locale_1.t('Error enabling key') : locale_1.t('Error disabling key'));
                        this.setState({ keyList: oldKeyList });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleCreateKey = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, orgId, projectId, data_1, _err_3;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/keys/", {
                                method: 'POST',
                            })];
                    case 2:
                        data_1 = _b.sent();
                        this.setState(function (state) { return ({
                            keyList: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(state.keyList)), [data_1]),
                        }); });
                        indicator_1.addSuccessMessage(locale_1.t('Created a new key.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_3 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to create new key. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectKeys.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Client Keys'), projectId, false);
    };
    ProjectKeys.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectKeys.prototype.renderEmpty = function () {
        return (<panels_1.Panel>
        <emptyMessage_1.default icon={<icons_1.IconFlag size="xl"/>} description={locale_1.t('There are no keys active for this project.')}/>
      </panels_1.Panel>);
    };
    ProjectKeys.prototype.renderResults = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, routes = _a.routes, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        var access = new Set(organization.access);
        return (<react_1.Fragment>
        {this.state.keyList.map(function (key) { return (<keyRow_1.default api={_this.api} access={access} key={key.id} orgId={orgId} projectId={"" + projectId} data={key} onToggle={_this.handleToggleKey} onRemove={_this.handleRemoveKey} routes={routes} location={location} params={params}/>); })}
        <pagination_1.default pageLinks={this.state.keyListPageLinks}/>
      </react_1.Fragment>);
    };
    ProjectKeys.prototype.renderBody = function () {
        var access = new Set(this.props.organization.access);
        var isEmpty = !this.state.keyList.length;
        return (<div data-test-id="project-keys">
        <settingsPageHeader_1.default title={locale_1.t('Client Keys')} action={access.has('project:write') ? (<button_1.default onClick={this.handleCreateKey} size="small" priority="primary" icon={<icons_1.IconAdd size="xs" isCircled/>}>
                {locale_1.t('Generate New Key')}
              </button_1.default>) : null}/>
        <textBlock_1.default>
          {locale_1.tct("To send data to Sentry you will need to configure an SDK with a client key\n          (usually referred to as the [code:SENTRY_DSN] value). For more\n          information on integrating Sentry with your application take a look at our\n          [link:documentation].", {
                link: <externalLink_1.default href="https://docs.sentry.io/"/>,
                code: <code />,
            })}
        </textBlock_1.default>

        {isEmpty ? this.renderEmpty() : this.renderResults()}
      </div>);
    };
    return ProjectKeys;
}(asyncView_1.default));
exports.default = withOrganization_1.default(ProjectKeys);
//# sourceMappingURL=index.jsx.map