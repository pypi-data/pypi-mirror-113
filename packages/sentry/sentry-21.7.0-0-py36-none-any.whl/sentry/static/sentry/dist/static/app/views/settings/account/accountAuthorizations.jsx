Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var AccountAuthorizations = /** @class */ (function (_super) {
    tslib_1.__extends(AccountAuthorizations, _super);
    function AccountAuthorizations() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRevoke = function (authorization) {
            var oldData = _this.state.data;
            _this.setState(function (state) { return ({
                data: state.data.filter(function (_a) {
                    var id = _a.id;
                    return id !== authorization.id;
                }),
            }); }, function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _err_1;
                return tslib_1.__generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, , 3]);
                            return [4 /*yield*/, this.api.requestPromise('/api-authorizations/', {
                                    method: 'DELETE',
                                    data: { authorization: authorization.id },
                                })];
                        case 1:
                            _a.sent();
                            indicator_1.addSuccessMessage(locale_1.t('Saved changes'));
                            return [3 /*break*/, 3];
                        case 2:
                            _err_1 = _a.sent();
                            this.setState({
                                data: oldData,
                            });
                            indicator_1.addErrorMessage(locale_1.t('Unable to save changes, please try again'));
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            }); });
        };
        return _this;
    }
    AccountAuthorizations.prototype.getEndpoints = function () {
        return [['data', '/api-authorizations/']];
    };
    AccountAuthorizations.prototype.getTitle = function () {
        return 'Approved Applications';
    };
    AccountAuthorizations.prototype.renderBody = function () {
        var _this = this;
        var data = this.state.data;
        var isEmpty = data.length === 0;
        return (<div>
        <settingsPageHeader_1.default title="Authorized Applications"/>
        <Description>
          {locale_1.tct('You can manage your own applications via the [link:API dashboard].', {
                link: <react_router_1.Link to="/settings/account/api/"/>,
            })}
        </Description>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Approved Applications')}</panels_1.PanelHeader>

          <panels_1.PanelBody>
            {isEmpty && (<emptyMessage_1.default>
                {locale_1.t("You haven't approved any third party applications.")}
              </emptyMessage_1.default>)}

            {!isEmpty && (<div>
                {data.map(function (authorization) { return (<PanelItemCenter key={authorization.id}>
                    <ApplicationDetails>
                      <ApplicationName>{authorization.application.name}</ApplicationName>
                      {authorization.homepageUrl && (<Url>
                          <a href={authorization.homepageUrl}>
                            {authorization.homepageUrl}
                          </a>
                        </Url>)}
                      <Scopes>{authorization.scopes.join(', ')}</Scopes>
                    </ApplicationDetails>
                    <button_1.default size="small" onClick={function () { return _this.handleRevoke(authorization); }} icon={<icons_1.IconDelete />}/>
                  </PanelItemCenter>); })}
              </div>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return AccountAuthorizations;
}(asyncView_1.default));
exports.default = AccountAuthorizations;
var Description = styled_1.default('p')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, space_1.default(4));
var PanelItemCenter = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n"], ["\n  align-items: center;\n"])));
var ApplicationDetails = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"])));
var ApplicationName = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  margin-bottom: ", ";\n"], ["\n  font-weight: bold;\n  margin-bottom: ", ";\n"])), space_1.default(0.5));
/**
 * Intentionally wrap <a> so that it does not take up full width and cause
 * hit box issues
 */
var Url = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.fontSizeRelativeSmall; });
var Scopes = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeRelativeSmall; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=accountAuthorizations.jsx.map