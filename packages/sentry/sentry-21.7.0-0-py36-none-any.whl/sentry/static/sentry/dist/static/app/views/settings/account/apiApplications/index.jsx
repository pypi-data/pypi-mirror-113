Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var row_1 = tslib_1.__importDefault(require("app/views/settings/account/apiApplications/row"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var ROUTE_PREFIX = '/settings/account/api/';
var ApiApplications = /** @class */ (function (_super) {
    tslib_1.__extends(ApiApplications, _super);
    function ApiApplications() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCreateApplication = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var app_1, _err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        indicator_1.addLoadingMessage();
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise('/api-applications/', {
                                method: 'POST',
                            })];
                    case 2:
                        app_1 = _a.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Created a new API Application'));
                        this.props.router.push(ROUTE_PREFIX + "applications/" + app_1.id + "/");
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to remove application. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRemoveApplication = function (app) {
            _this.setState({
                appList: _this.state.appList.filter(function (a) { return a.id !== app.id; }),
            });
        };
        return _this;
    }
    ApiApplications.prototype.getEndpoints = function () {
        return [['appList', '/api-applications/']];
    };
    ApiApplications.prototype.getTitle = function () {
        return locale_1.t('API Applications');
    };
    ApiApplications.prototype.renderBody = function () {
        var _this = this;
        var action = (<button_1.default priority="primary" size="small" onClick={this.handleCreateApplication} icon={<icons_1.IconAdd size="xs" isCircled/>}>
        {locale_1.t('Create New Application')}
      </button_1.default>);
        var isEmpty = this.state.appList.length === 0;
        return (<div>
        <settingsPageHeader_1.default title="API Applications" action={action}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Application Name')}</panels_1.PanelHeader>

          <panels_1.PanelBody>
            {!isEmpty ? (this.state.appList.map(function (app) { return (<row_1.default api={_this.api} key={app.id} app={app} onRemove={_this.handleRemoveApplication}/>); })) : (<emptyMessage_1.default>
                {locale_1.t("You haven't created any applications yet.")}
              </emptyMessage_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return ApiApplications;
}(asyncView_1.default));
exports.default = ApiApplications;
//# sourceMappingURL=index.jsx.map