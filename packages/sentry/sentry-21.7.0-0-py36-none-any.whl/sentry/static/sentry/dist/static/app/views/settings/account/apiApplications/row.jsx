Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var ROUTE_PREFIX = '/settings/account/api/';
var Row = /** @class */ (function (_super) {
    tslib_1.__extends(Row, _super);
    function Row() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
        };
        _this.handleRemove = function () {
            if (_this.state.loading) {
                return;
            }
            var _a = _this.props, api = _a.api, app = _a.app, onRemove = _a.onRemove;
            _this.setState({
                loading: true,
            }, function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _err_1;
                return tslib_1.__generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            indicator_1.addLoadingMessage();
                            _a.label = 1;
                        case 1:
                            _a.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, api.requestPromise("/api-applications/" + app.id + "/", {
                                    method: 'DELETE',
                                })];
                        case 2:
                            _a.sent();
                            indicator_1.clearIndicators();
                            onRemove(app);
                            return [3 /*break*/, 4];
                        case 3:
                            _err_1 = _a.sent();
                            indicator_1.addErrorMessage(locale_1.t('Unable to remove application. Please try again.'));
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            }); });
        };
        return _this;
    }
    Row.prototype.render = function () {
        var app = this.props.app;
        return (<StyledPanelItem>
        <ApplicationNameWrapper>
          <ApplicationName to={ROUTE_PREFIX + "applications/" + app.id + "/"}>
            {getDynamicText_1.default({ value: app.name, fixed: 'CI_APPLICATION_NAME' })}
          </ApplicationName>
          <ClientId>
            {getDynamicText_1.default({ value: app.clientID, fixed: 'CI_CLIENT_ID' })}
          </ClientId>
        </ApplicationNameWrapper>

        <button_1.default aria-label="Remove" onClick={this.handleRemove} disabled={this.state.loading} icon={<icons_1.IconDelete />}/>
      </StyledPanelItem>);
    };
    return Row;
}(react_1.Component));
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  align-items: center;\n"], ["\n  padding: ", ";\n  align-items: center;\n"])), space_1.default(2));
var ApplicationNameWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  flex: 1;\n  margin-right: ", ";\n"])), space_1.default(1));
var ApplicationName = styled_1.default(link_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, space_1.default(0.5));
var ClientId = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.fontSizeMedium; });
exports.default = Row;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=row.jsx.map