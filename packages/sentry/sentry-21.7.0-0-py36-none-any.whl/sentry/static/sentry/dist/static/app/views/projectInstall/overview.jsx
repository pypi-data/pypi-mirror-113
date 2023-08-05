Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var autoSelectText_1 = tslib_1.__importDefault(require("app/components/autoSelectText"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var platformPicker_1 = tslib_1.__importDefault(require("app/components/platformPicker"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var ProjectInstallOverview = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectInstallOverview, _super);
    function ProjectInstallOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.redirectToDocs = function (platform) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            var installUrl = _this.isGettingStarted
                ? "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/" + platform + "/"
                : recreateRoute_1.default("install/" + platform + "/", tslib_1.__assign(tslib_1.__assign({}, _this.props), { stepBack: -3 }));
            react_router_1.browserHistory.push(installUrl);
        };
        _this.toggleDsn = function () {
            _this.setState(function (state) { return ({ showDsn: !state.showDsn }); });
        };
        return _this;
    }
    Object.defineProperty(ProjectInstallOverview.prototype, "isGettingStarted", {
        get: function () {
            return window.location.href.indexOf('getting-started') > 0;
        },
        enumerable: false,
        configurable: true
    });
    ProjectInstallOverview.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectInstallOverview.prototype.render = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var _b = this.state, keyList = _b.keyList, showDsn = _b.showDsn;
        var issueStreamLink = "/organizations/" + orgId + "/issues/#welcome";
        return (<div>
        <sentryDocumentTitle_1.default title={locale_1.t('Instrumentation')} projectSlug={projectId}/>
        <settingsPageHeader_1.default title={locale_1.t('Configure your application')}/>
        <textBlock_1.default>
          {locale_1.t('Get started by selecting the platform or language that powers your application.')}
        </textBlock_1.default>

        {showDsn ? (<DsnInfo>
            <DsnContainer>
              <strong>{locale_1.t('DSN')}</strong>
              <DsnValue>{keyList === null || keyList === void 0 ? void 0 : keyList[0].dsn.public}</DsnValue>
            </DsnContainer>

            <button_1.default priority="primary" to={issueStreamLink}>
              {locale_1.t('Got it! Take me to the Issue Stream.')}
            </button_1.default>
          </DsnInfo>) : (<p>
            <small>
              {locale_1.tct('Already have things setup? [link:Get your DSN]', {
                    link: <button_1.default priority="link" onClick={this.toggleDsn}/>,
                })}
              .
            </small>
          </p>)}
        <platformPicker_1.default setPlatform={this.redirectToDocs} showOther={false} organization={this.props.organization}/>
        <p>
          {locale_1.tct("For a complete list of client integrations, please see\n             [docLink:our in-depth documentation].", { docLink: <externalLink_1.default href="https://docs.sentry.io"/> })}
        </p>
      </div>);
    };
    return ProjectInstallOverview;
}(asyncComponent_1.default));
var DsnValue = styled_1.default(function (p) { return (<code {...p}>
    <autoSelectText_1.default>{p.children}</autoSelectText_1.default>
  </code>); })(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var DsnInfo = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
var DsnContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", " ", ";\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", " ", ";\n  align-items: center;\n  margin-bottom: ", ";\n"])), space_1.default(1.5), space_1.default(2), space_1.default(2));
exports.default = withOrganization_1.default(ProjectInstallOverview);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=overview.jsx.map