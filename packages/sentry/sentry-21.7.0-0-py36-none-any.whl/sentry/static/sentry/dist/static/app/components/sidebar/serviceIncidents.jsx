Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var serviceIncidents_1 = require("app/actionCreators/serviceIncidents");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var list_1 = tslib_1.__importDefault(require("../list"));
var listItem_1 = tslib_1.__importDefault(require("../list/listItem"));
var sidebarItem_1 = tslib_1.__importDefault(require("./sidebarItem"));
var sidebarPanel_1 = tslib_1.__importDefault(require("./sidebarPanel"));
var sidebarPanelEmpty_1 = tslib_1.__importDefault(require("./sidebarPanelEmpty"));
var sidebarPanelItem_1 = tslib_1.__importDefault(require("./sidebarPanelItem"));
var ServiceIncidents = /** @class */ (function (_super) {
    tslib_1.__extends(ServiceIncidents, _super);
    function ServiceIncidents() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            status: null,
        };
        return _this;
    }
    ServiceIncidents.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ServiceIncidents.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var status_1, e_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, serviceIncidents_1.loadIncidents()];
                    case 1:
                        status_1 = _a.sent();
                        this.setState({ status: status_1 });
                        return [3 /*break*/, 3];
                    case 2:
                        e_1 = _a.sent();
                        Sentry.withScope(function (scope) {
                            scope.setLevel(Sentry.Severity.Warning);
                            scope.setFingerprint(['ServiceIncidents-fetchData']);
                            Sentry.captureException(e_1);
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    ServiceIncidents.prototype.render = function () {
        var _a = this.props, currentPanel = _a.currentPanel, onShowPanel = _a.onShowPanel, hidePanel = _a.hidePanel, collapsed = _a.collapsed, orientation = _a.orientation;
        var status = this.state.status;
        if (!status) {
            return null;
        }
        var active = currentPanel === 'statusupdate';
        var isEmpty = !status.incidents || status.incidents.length === 0;
        if (isEmpty) {
            return null;
        }
        return (<react_1.Fragment>
        <sidebarItem_1.default id="statusupdate" orientation={orientation} collapsed={collapsed} active={active} icon={<icons_1.IconWarning size="md"/>} label={locale_1.t('Service status')} onClick={onShowPanel}/>
        {active && status && (<sidebarPanel_1.default orientation={orientation} title={locale_1.t('Recent service updates')} hidePanel={hidePanel} collapsed={collapsed}>
            {isEmpty && (<sidebarPanelEmpty_1.default>
                {locale_1.t('There are no incidents to report')}
              </sidebarPanelEmpty_1.default>)}
            <IncidentList className="incident-list">
              {status.incidents.map(function (incident) { return (<sidebarPanelItem_1.default title={incident.name} message={locale_1.t('Latest updates')} key={incident.id}>
                  {incident.updates ? (<list_1.default>
                      {incident.updates.map(function (update, key) { return (<listItem_1.default key={key}>{update}</listItem_1.default>); })}
                    </list_1.default>) : null}
                  <ActionBar>
                    <button_1.default href={incident.url} size="small" external>
                      {locale_1.t('Learn more')}
                    </button_1.default>
                  </ActionBar>
                </sidebarPanelItem_1.default>); })}
            </IncidentList>
          </sidebarPanel_1.default>)}
      </react_1.Fragment>);
    };
    return ServiceIncidents;
}(react_1.Component));
exports.default = ServiceIncidents;
var IncidentList = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
var ActionBar = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=serviceIncidents.jsx.map