Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var listLink_1 = tslib_1.__importDefault(require("app/components/links/listLink"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var sessionRow_1 = tslib_1.__importDefault(require("./sessionRow"));
var utils_1 = require("./utils");
var SessionHistory = /** @class */ (function (_super) {
    tslib_1.__extends(SessionHistory, _super);
    function SessionHistory() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SessionHistory.prototype.getTitle = function () {
        return locale_1.t('Session History');
    };
    SessionHistory.prototype.getEndpoints = function () {
        return [['ipList', '/users/me/ips/']];
    };
    SessionHistory.prototype.renderBody = function () {
        var ipList = this.state.ipList;
        if (!ipList) {
            return null;
        }
        var _a = this.props, routes = _a.routes, params = _a.params, location = _a.location;
        var recreateRouteProps = { routes: routes, params: params, location: location };
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Security')} tabs={<navTabs_1.default underlined>
              <listLink_1.default to={recreateRoute_1.default('', tslib_1.__assign(tslib_1.__assign({}, recreateRouteProps), { stepBack: -1 }))} index>
                {locale_1.t('Settings')}
              </listLink_1.default>
              <listLink_1.default to={recreateRoute_1.default('', recreateRouteProps)}>
                {locale_1.t('Session History')}
              </listLink_1.default>
            </navTabs_1.default>}/>

        <panels_1.Panel>
          <SessionPanelHeader>
            <div>{locale_1.t('Sessions')}</div>
            <div>{locale_1.t('First Seen')}</div>
            <div>{locale_1.t('Last Seen')}</div>
          </SessionPanelHeader>

          <panels_1.PanelBody>
            {ipList.map(function (_a) {
                var id = _a.id, ipObj = tslib_1.__rest(_a, ["id"]);
                return (<sessionRow_1.default key={id} {...ipObj}/>);
            })}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return SessionHistory;
}(asyncView_1.default));
exports.default = SessionHistory;
var SessionPanelHeader = styled_1.default(panels_1.PanelHeader)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", "\n  justify-content: initial;\n"], ["\n  ", "\n  justify-content: initial;\n"])), utils_1.tableLayout);
var templateObject_1;
//# sourceMappingURL=index.jsx.map